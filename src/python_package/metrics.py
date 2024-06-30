import numpy as np
from scipy.stats import wasserstein_distance, entropy
from scipy.special import rel_entr


def frechet_distance(real_data, generated_data):
    mu_r = np.mean(real_data)
    mu_g = np.mean(generated_data)
    var_r = np.var(real_data)
    var_g = np.var(generated_data)

    mean_diff = mu_r - mu_g
    cov_mean = np.sqrt(var_r * var_g)

    distance = mean_diff**2 + var_r + var_g - 2 * cov_mean
    return distance

