import torch.nn as nn
import pennylane as qml
import torch
import numpy as np


class Discriminator(nn.Module):
    """Fully connected classical discriminator"""

    def __init__(self, input_shape, layers):
        super().__init__()

        self.input_shape = input_shape
        self.layers = layers
        self.model = self.set_model()
    
    def set_model(self):
        input = self.input_shape
        modules = []
        for layer in self.layers:
            modules.append(nn.Linear(input, layer))
            modules.append(nn.LeakyReLU())
            input = layer
        
        modules.append(nn.Linear(input, 1))
        modules.append(nn.Sigmoid())
        
        return nn.Sequential(*modules)

    def forward(self, x):
        x = x.reshape(x.size(0), -1)
        
        return self.model(x)
    
    
    
class QuantumAnsatz:
    def __init__(self, n_qubits, q_depth) -> None:
        
        self.n_qubits = n_qubits
        self.q_depth = q_depth
        self.dev = qml.device("default.qubit", wires=n_qubits)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


    def circuit(self):

        @qml.qnode(self.dev, diff_method="backprop")
        def quantum_circuit(weights):

            weights = weights.reshape(self.q_depth, self.n_qubits)

            # Initialise latent vectors
            for i in range(self.n_qubits):
                qml.Hadamard(wires=i)

            # Repeated layer
            for i in range(self.q_depth):
                # Parameterised layer
                for y in range(self.n_qubits):
                    qml.RY(weights[i][y], wires=y)

                # Control Z gates
                for y in range(self.n_qubits - 1):
                    qml.CZ(wires=[y, y + 1])

                #qml.CZ(wires=[5, 0])

                qml.Barrier(wires=list(range(self.n_qubits)), only_visual=True)

            return qml.probs(wires=list(range(self.n_qubits)))

        return quantum_circuit
    
    
class QuantumGenerator(nn.Module):
    """Quantum generator class for the patch method"""

    def __init__(self, n_qubits, q_depth, quantum_circuit):
        """
        Args:
            n_generators (int): Number of sub-generators to be used in the patch method.
            q_delta (float, optional): Spread of the random distribution for parameter initialisation.
        """

        super().__init__()

        self.n_qubits = n_qubits
        self.q_depth = q_depth
        self.q_params = nn.ParameterList(
            [
                nn.Parameter(torch.rand(q_depth * n_qubits), requires_grad=True)
            ]
        )

        self.ansatz = quantum_circuit

    def forward(self):

        qc_out = self.ansatz(self.q_params[0]).float().unsqueeze(0)
        
        return qc_out
    
    
    def trained_circuit(self, shots: int):
        dev = qml.device("default.qubit", wires=self.n_qubits, shots=shots)

        @qml.qnode(dev)
        def quantum_circuit():

            weights = self.q_params[0].reshape(self.q_depth, self.n_qubits).detach()

            # Initialise latent vectors
            for i in range(self.n_qubits):
                qml.Hadamard(wires=i)

            # Repeated layer
            for i in range(self.q_depth):
                # Parameterised layer
                for y in range(self.n_qubits):
                    qml.RY(weights[i][y], wires=y)

                # Control Z gates
                for y in range(self.n_qubits - 1):
                    qml.CZ(wires=[y, y + 1])

                #qml.CZ(wires=[5, 0])

                qml.Barrier(wires=list(range(self.n_qubits)), only_visual=True)

            return qml.probs(wires=list(range(self.n_qubits)))
    
        return quantum_circuit
    

    def filtered_distribution(self, shots: int, excluded_states: list[int]):

        generated_dist = self.trained_circuit(shots=shots)()
        # Filter out the unwanted states by setting their probabilities to zero
        filtered_probs = np.copy(generated_dist)
        for state in excluded_states:
            filtered_probs[state] = 0

        # Normalize the probabilities to ensure they sum to 1
        total_prob = np.sum(filtered_probs)
        normalized_probs = filtered_probs / total_prob

        return normalized_probs


