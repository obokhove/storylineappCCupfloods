"""
Created by OB 14-03 vv
"""
import numpy as np
import matplotlib.pyplot as plt
import os.path
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from scipy.optimize import minimize_scalar

# Define the trio of data points to plot
nscenario = 3
if nscenario==3:
    points_x = [1.23, 1.31, 1.51]
    points_y = [0.5, 0.7, 0.95]
elif nscenario==2:
    points_x = [1.13, 1.18, 1.31]
    points_y = [0.5, 0.7, 0.95]
elif nscenario==1:
    points_x = [1.11, 1.15, 1.24]
    points_y = [0.5, 0.7, 0.95]


# Parameters for the trial normal distribution
mu = points_x[0]  # Mean (derived from the point where CDF = 0.5)
trial_sigma = (points_x[2]-points_x[0])/1.64
sigma = trial_sigma  # Standard deviation (approximate, derived from the points)
# Create the plot
plt.figure(figsize=(10, 6))

# Create x values for plotting the CDF
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 1000)
# Calculate CDF values
cdf_values = norm.cdf(x, loc=mu, scale=sigma)
# Plot the CDF curve
plt.plot(x, cdf_values, 'b-', linewidth=2, label=f'Normal CDF (μ={mu}, σ={sigma:.2f})')


# Plot the points
for i, (px, py) in enumerate(zip(points_x, points_y)):
    plt.scatter(px, py, s=100, zorder=5, 
                label=f'Point {i+1}: ({px}, {py})' if i == 0 else "")
    # Add annotation for each point
    plt.annotate(f'({px}, {py})', 
                 xy=(px, py), 
                 xytext=(px + 0.05, py + 0.03),
                 fontsize=10,
                 arrowprops=dict(arrowstyle='->', color='gray'))

# Add labels and title
plt.xlabel('F', fontsize=12)
plt.ylabel('CDF(F)', fontsize=12)
if nscenario==3:
    plt.title('CDF Normal Distribution with Marked Points, 2070-2125', fontsize=14)
elif nscenario==2:
    plt.title('CDF Normal Distribution with Marked Points, 2040-2069', fontsize=14)
elif nscenario==1:
    plt.title('CDF Normal Distribution with Marked Points, 2015-2039', fontsize=14)


# Add grid and Set axis limits
plt.grid(True, alpha=0.3)
plt.xlim(mu - 3*sigma, mu + 3*sigma)
plt.ylim(0, 1.05)

# Add legend
plt.legend()

# Show horizontal reference lines at CDF values for y_val in [0.5, 0.7, 0.95]:
for y_val in points_y:
    plt.axhline(y=y_val, color='gray', linestyle='--', alpha=0.5)
# Add vertical reference lines at F values
for x_val in points_x: # [1.23, 1.31, 1.51]:
    plt.axvline(x=x_val, color='gray', linestyle=':', alpha=0.5)

#    
# Find best-fit sigma using least squares
#
def error_function(sigma):
    total_error = 0
    for px, py in zip(points_x, points_y):
        predicted_cdf = norm.cdf(px, loc=mu, scale=sigma)
        total_error += (predicted_cdf - py) ** 2
    return total_error

result = minimize_scalar(error_function, bounds=(0.01, 1.0), method='bounded')
optimal_sigma = result.x
print(f"Optimal sigma: {optimal_sigma:.8f}")
# Update sigma for the rest of the code
ls_sigma =  optimal_sigma
sigma = optimal_sigma

# Create x values for plotting the CDF
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 1000)
# Calculate CDF values
cdf_values = norm.cdf(x, loc=mu, scale=sigma)
# Plot the CDF curve
plt.plot(x, cdf_values, 'r-', linewidth=2, label=f'LS Normal CDF fitted (μ={mu}, σ={sigma:.8f})')
plt.legend()
ppf_valuep05 = norm.ppf(0.05, loc=mu, scale=sigma) # 
print(f"CDF(0.05) {ppf_valuep05:.8f}")
plt.plot(ppf_valuep05, 0.05, 'kx', linewidth=2, label=f'({ppf_valuep05:.8f},0.05)')
ppf_valuep30 = norm.ppf(0.30, loc=mu, scale=sigma) # 
print(f"CDF(0.30) {ppf_valuep30:.8f}")
plt.plot(ppf_valuep30, 0.30, 'kx', linewidth=2, label=f'({ppf_valuep30:.8f},0.30)')




#
# MLE approach for fitting sigma to CDF observations
#
def negative_log_likelihood(sigma):
    """
    Negative log-likelihood for CDF observations.
    Assumes CDF values have Gaussian measurement error.
    """
    nll = 0
    for px, py in zip(points_x, points_y):
        predicted_cdf = norm.cdf(px, loc=mu, scale=sigma)
        # Log-likelihood contribution (assuming small Gaussian noise on CDF values)
        # Using a small epsilon to avoid log(0)
        epsilon = 1e-10
        py_clipped = np.clip(py, epsilon, 1 - epsilon)
        predicted_clipped = np.clip(predicted_cdf, epsilon, 1 - epsilon)
        
        # Gaussian likelihood on the CDF values
        residual = py - predicted_cdf
        nll += 0.5 * (residual / 0.01) ** 2  # Assuming ~0.01 std dev on CDF measurements
    
    return nll

# Find MLE estimate for sigma
result_mle = minimize_scalar(negative_log_likelihood, bounds=(0.01, 1.0), method='bounded')
mle_sigma = result_mle.x
print(f"MLE sigma: {mle_sigma:.8f}")

# Compare with least squares approach Not used?
# def least_squares_error(sigma):
#     total_error = 0
#     for px, py in zip(points_x, points_y):
#         predicted_cdf = norm.cdf(px, loc=mu, scale=sigma)

# Create x values for plotting the CDF
sigma = mle_sigma
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 1000)
# Calculate CDF values
cdf_values = norm.cdf(x, loc=mu, scale=sigma)
# Plot the CDF curve
plt.plot(x, cdf_values, 'r-', linewidth=2, label=f'MLE Normal CDF fitted (μ={mu}, σ={sigma:.8f})')
plt.legend()

# Given CDF(F): delta CDF = dCDF/dF delta F so  delta F = delta CDF* dF/dCDF
# delta CDF is rms square of difference between mean of prediction and actual values \
# actual values are the percentiles but the 50th percentile does not count since mu, so n-1 is used in mean
F = 1.51
print(f"F: {F:.6f} and sigma: {sigma:.6f}")
rms_residual = np.sqrt(np.sum((norm.cdf(points_x, loc=mu, scale=sigma) - points_y) ** 2) / (len(points_y) - 1))
pdf_at_F = norm.pdf(F, loc=mu, scale=sigma) # dF/dCDF(F) = 1/PDF(F)
newerror  = rms_residual/pdf_at_F # Given CDF(F): delta CDF = dCDF/dF delta F so  delta F = delta CDF* dF/dCDF
print(f"PDF at F={F}: {pdf_at_F:.6f}")
print(f"Scaling factor (1/PDF): {1/pdf_at_F:.8f}")
print(f" error in F: {newerror:.8f}")
delQoQ = 0.16
toterror = np.sqrt(delQoQ**2+newerror**2)
print(f" Partial errors: {delQoQ} and {newerror}, Total error in uplifted Q: {toterror:.8f}")


# Graphing
plt.tight_layout()
save_figure=True
figure_name= f"CDFFAire.png"

data_path = 'data/'
if save_figure:
    save_path=os.path.join(data_path, figure_name)

if save_figure:
    plt.savefig(save_path,dpi=300)
else:
    plt.show()
