
<div align="center">

# **Summary of ECAL Channel Test Results**
---

<div align="justify">

This README file includes a summary of test results for the various parameters explored in my experiments.
Each entry in the table represents a specific configuration and its outcomes. The model used in the training is the proposed by 
[He-Liang et.al.](https://arxiv.org/abs/2010.06201), this model consist in a set of feature qubits which will represent the distribution
and a set of auxiliar qubits which gives the model more freedom, a post-processing is performed over the circuit output, first is divided by
a number $y \in [0, 1]$ which allows the circuit output to take values larger than 1 and fix the limitation of the maximum sum of the output 
probabilities.

<div align="center">

<img src="/home/reyguadarrama/GSoC/images/Quantum_generator-2.png" alt="PQC architecture" width="400" height="200"/>

<div align="justify">


- The first 5 test show that a smaller generator lr produces a better convergence, range tested: $gen\,\,lr \in [0.005, 0.4]$.


| id | qubits | auxiliar qubits | circuit depth | generators | rotations | lr gen | lr disc | batch size | resolution | optimizer | samples | epochs | y | FID | RMSE | disc loss | gen loss | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 00 | 7 | 2 | 10 | 2 | ['Y'] | 0.005 | 0.1 | 1 | 8x8 | SGD | 512 | 20 | 0.3 | 1.60e-04 | 5.43e-03 | 1.58e+00 | 7.35e-01 | it seems a small gen lr is better |
| 01 | 7 | 2 | 10 | 2 | ['Y'] | 0.01 | 0.1 | 1 | 8x8 | SGD | 512 | 20 | 0.3 | 1.71e-04 | 8.09e-03 | 1.48e+00 | 8.93e-01 | worse performance with larger gen lr |
| 02 | 7 | 2 | 10 | 2 | ['Y'] | 0.02 | 0.1 | 1 | 8x8 | SGD | 512 | 20 | 0.3 | 1.22e-03 | 1.18e-02 | 1.14e+00 | 8.08e-01 | worse performance with larger gen lr |
| 03 | 7 | 2 | 10 | 2 | ['Y'] | 0.03 | 0.1 | 1 | 8x8 | SGD | 512 | 20 | 0.3 | 4.16e-04 | 7.67e-03 | 1.48e+00 | 8.86e-01 | worse performance with larger gen lr |
| 04 | 7 | 2 | 10 | 2 | ['Y'] | 0.04 | 0.1 | 1 | 8x8 | SGD | 512 | 20 | 0.3 | 1.21e-03 | 1.26e-02 | 1.21e+00 | 7.59e-01 | worse performance with larger gen lr |
