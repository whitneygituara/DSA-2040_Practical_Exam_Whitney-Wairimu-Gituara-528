import numpy as np
import pandas as pd

# Set a random seed for reproducible results
np.random.seed(42)

# Define parameters for 3 Gaussian clusters (mimicking species)
# Features: [sepal length, sepal width, petal length, petal width]
feature_names = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']

# --- Cluster 1 (Species 0: Small features) ---
# Mean values for the four features (center of the cluster)
mean_0 = [5.0, 3.4, 1.4, 0.2]
# Covariance matrix controls the spread of the data (set to be tighter)
cov_0 = np.diag([0.2, 0.2, 0.1, 0.1]) * 0.5 
samples_0 = np.random.multivariate_normal(mean_0, cov_0, 50)
labels_0 = np.zeros(50, dtype=int)

# --- Cluster 2 (Species 1: Medium features) ---
mean_1 = [5.9, 2.8, 4.3, 1.3]
cov_1 = np.diag([0.3, 0.1, 0.4, 0.3]) * 0.5
samples_1 = np.random.multivariate_normal(mean_1, cov_1, 50)
labels_1 = np.ones(50, dtype=int)

# --- Cluster 3 (Species 2: Large features) ---
mean_2 = [6.5, 3.0, 5.5, 2.0]
cov_2 = np.diag([0.5, 0.2, 0.5, 0.4]) * 0.5
samples_2 = np.random.multivariate_normal(mean_2, cov_2, 50)
labels_2 = np.full(50, 2, dtype=int)

# Combine all data
X = np.concatenate([samples_0, samples_1, samples_2])
y = np.concatenate([labels_0, labels_1, labels_2])

# Create the final DataFrame
df = pd.DataFrame(X, columns=feature_names)
df['species'] = y

print("--- Synthetic Data Generated and Loaded into DataFrame (df) ---")
print(f"Total Samples: {len(df)}")
print(df.head())

# The variable 'df' now holds the 150 samples with 4 features and the species label.