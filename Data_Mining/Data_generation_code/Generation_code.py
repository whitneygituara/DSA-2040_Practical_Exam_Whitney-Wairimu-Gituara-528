# -----------------------------
# Task 1: Save Synthetic Data
# -----------------------------
import numpy as np
import pandas as pd

# Set a random seed for reproducibility
np.random.seed(42)

# Feature names
feature_names = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']

# Generate synthetic clusters (same as your previous code)
mean_0, cov_0 = [5.0, 3.4, 1.4, 0.2], np.diag([0.2,0.2,0.1,0.1])*0.5
mean_1, cov_1 = [5.9, 2.8, 4.3, 1.3], np.diag([0.3,0.1,0.4,0.3])*0.5
mean_2, cov_2 = [6.5, 3.0, 5.5, 2.0], np.diag([0.5,0.2,0.5,0.4])*0.5

samples_0 = np.random.multivariate_normal(mean_0, cov_0, 50)
samples_1 = np.random.multivariate_normal(mean_1, cov_1, 50)
samples_2 = np.random.multivariate_normal(mean_2, cov_2, 50)

labels_0 = np.zeros(50, dtype=int)
labels_1 = np.ones(50, dtype=int)
labels_2 = np.full(50, 2, dtype=int)

# Combine
X = np.concatenate([samples_0, samples_1, samples_2])
y = np.concatenate([labels_0, labels_1, labels_2])

# Create DataFrame
df = pd.DataFrame(X, columns=feature_names)
df['species'] = y

# Save to CSV
df.to_csv('synthetic_iris.csv', index=False)

print("--- Synthetic Data Saved as 'synthetic_iris.csv' ---")


