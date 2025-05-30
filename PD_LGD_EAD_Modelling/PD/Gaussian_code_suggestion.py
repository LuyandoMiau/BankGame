from sklearn.preprocessing import StandardScaler
from scipy.stats import norm, multivariate_normal
from scipy.optimize import minimize

""" SECOND STEP:
now we will define the Gaussian factor copula model.
This model will use the combined data to estimate the joint distribution of default probabilities and LGD.
We will use the Gaussian copula to model the dependence structure between the default probabilities and LGD.
The Gaussian copula allows us to model the joint distribution of multiple variables while capturing their dependence structure.
The Gaussian copula is defined as follows:
    C(u_1, u_2, ..., u_n) = Φ_n(Φ^{-1}(u_1), Φ^{-1}(u_2), ..., Φ^{-1}(u_n))
    
where C is the copula function, u_i are the marginal distributions of the variables, and Φ_n is the multivariate normal cumulative distribution function.
We will use the Gaussian copula to model the joint distribution of default probabilities and LGD.
"""
class GaussianFactorCopula:
    def __init__(self, data):
        """
        Initialize the Gaussian Factor Copula model with the provided data.
        
        Parameters:
        - data: pandas DataFrame containing the combined data with default probabilities and LGD.
        """
        self.data = data
        self.scaler = StandardScaler()
        self.copula_params = None

    def fit(self):
        """
        Fit the Gaussian factor copula model to the data.
        This involves estimating the parameters of the copula based on the empirical distribution of the data.
        """
        # Scale the data
        scaled_data = self.scaler.fit_transform(self.data)
        
        # Estimate copula parameters (mean and covariance)
        mean = np.mean(scaled_data, axis=0)
        cov = np.cov(scaled_data, rowvar=False)
        
        self.copula_params = {'mean': mean, 'cov': cov}
    
    def sample(self, n_samples=1000):
        """
        Generate samples from the fitted Gaussian factor copula model.
        
        Parameters:
        - n_samples: Number of samples to generate.
        
        Returns:
        - samples: Generated samples from the copula.
        """
        if self.copula_params is None:
            raise ValueError("Model has not been fitted yet. Call fit() before sampling.")
        
        mean = self.copula_params['mean']
        cov = self.copula_params['cov']
        
        # Generate samples from multivariate normal distribution
        samples = multivariate_normal.rvs(mean=mean, cov=cov, size=n_samples)
        
        # Transform samples back to original scale
        return self.scaler.inverse_transform(samples)
    def evaluate(self, u):
        """
        Evaluate the copula at given points u.
        Parameters:
        - u: Points at which to evaluate the copula (should be in the range [0, 1]).
        Returns:
        - copula_value: Value of the copula at the given points.
        """ 
        if self.copula_params is None:
            raise ValueError("Model has not been fitted yet. Call fit() before evaluating.")
        
        # Transform u to standard normal quantiles
        z = norm.ppf(u)
        
        # Evaluate the multivariate normal cumulative distribution function
        copula_value = multivariate_normal.cdf(z, mean=self.copula_params['mean'], cov=self.copula_params['cov'])
        
        return copula_value
    def log_likelihood(self, u):
        """
        Compute the log-likelihood of the copula given the data.
        Parameters:
        - u: Points at which to compute the log-likelihood (should be in the range [0, 1]).
        Returns:
        - log_likelihood: Log-likelihood of the copula at the given points.
        """ 
        if self.copula_params is None:
            raise ValueError("Model has not been fitted yet. Call fit() before computing log-likelihood.")
        
        # Evaluate the copula at points u
        copula_value = self.evaluate(u)
        
        # Compute log-likelihood
        log_likelihood = np.sum(np.log(copula_value))
        
        return log_likelihood
    def fit_and_sample(self, n_samples=1000):
        """
        Fit the model and generate samples in one step.
        Parameters:
        - n_samples: Number of samples to generate.
        Returns:
        - samples: Generated samples from the copula.
        """
        self.fit()
        return self.sample(n_samples)
# Example usage
if __name__ == "__main__":
    # Load the combined data
    combined_data = pd.read_csv(combined_data_path)
    
    # Initialize the Gaussian Factor Copula model
    copula_model = GaussianFactorCopula(data=combined_data[['PD', 'LGD']])
    
    # Fit the model
    copula_model.fit()
    
    # Generate samples
    samples = copula_model.sample(n_samples=1000)
    
    # Print the first few samples
    print(samples[:5])
    
    # Evaluate the copula at some points
    u = np.random.uniform(0, 1, size=(10, 2))  # Random points in [0, 1]^2
    copula_values = copula_model.evaluate(u)
    
    print("Copula values at random points:", copula_values)
    
    # Compute log-likelihood at the same points
    log_likelihood = copula_model.log_likelihood(u)
    
    print("Log-likelihood:", log_likelihood)
# Save the fitted model parameters
copula_params_path = '/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/PD_LGD_EAD_Modelling/PD/copula_params.json'
import json
with open(copula_params_path, 'w') as f:
    json.dump(copula_model.copula_params, f)
# Save the samples to a CSV file
samples_df = pd.DataFrame(samples, columns=['PD_sample', 'LGD_sample'])
samples_df.to_csv('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator/Generated_data/copula_samples.csv', index=False)
# Save the combined data with samples
combined_data_with_samples = pd.concat([combined_data, samples_df], axis=1)
combined_data_with_samples.to_csv('/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/Data_generator/Generated_data/combined_data_with_samples.csv', index=False)
# Save the fitted model to a file
import joblib
model_path = '/Users/bonjour/Documents/AI/Projects/GitHub/BankGame/PD_LGD_EAD_Modelling/PD/copula_model.pkl'
joblib.dump(copula_model, model_path)

