import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# =================================================================
# Task 1.1: Data Generation and Loading (6 Marks)
# =================================================================

# Set a random seed for reproducible results
np.random.seed(42)

# Define parameters for 3 Gaussian clusters
# Features: [sepal length, sepal width, petal length, petal width]
feature_names = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']

# Cluster 1 (Species 0: Small features)
mean_0 = [5.0, 3.4, 1.4, 0.2]
cov_0 = np.diag([0.2, 0.2, 0.1, 0.1]) * 0.5  # Controls spread
samples_0 = np.random.multivariate_normal(mean_0, cov_0, 50)
labels_0 = np.zeros(50, dtype=int)

# Cluster 2 (Species 1: Medium features)
mean_1 = [5.9, 2.8, 4.3, 1.3]
cov_1 = np.diag([0.3, 0.1, 0.4, 0.3]) * 0.5
samples_1 = np.random.multivariate_normal(mean_1, cov_1, 50)
labels_1 = np.ones(50, dtype=int)

# Cluster 3 (Species 2: Large features)
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

# Fix: Reset index after concatenation
df.reset_index(drop=True, inplace=True)

print("--- Data Generation Complete ---")
print(f"Total Samples: {len(df)}")
print("First 5 rows of the synthetic dataset:")
print(df.head())
print("-" * 30)

# =================================================================
# Task 1.b): Preprocessing
# =================================================================

# i) Handle Missing Values (Demonstrate Check)
print("\n--- Missing Values Check ---")
print(df.isnull().sum())
# Separating features and target
X_data = df.drop('species', axis=1)
y_target = df['species']

# 2. Normalize Features using Min-Max Scaling
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_data)
X_scaled_df = pd.DataFrame(X_scaled, columns=feature_names)

print("\n--- Min-Max Scaling Complete ---")
print("First 5 rows of Scaled Features:")
print(X_scaled_df.head())

# 3. Encode the class label (Integer encoding is sufficient, One-Hot demonstrated if needed)
print("-" * 30)

# =================================================================
# Task 1.c): Exploration and Visualizations 
# =================================================================

# 1. Compute Summary Statistics (Using unscaled data for realistic view)
print("\n--- Summary Statistics (Raw Data) ---")
print(X_data.describe())
print("-" * 30)

# 2. Visualize: Pairplot
df_viz = X_scaled_df.copy()
df_viz['species'] = y_target
plt.figure(figsize=(10, 10))
sns.pairplot(df_viz, hue='species', diag_kind='kde')
plt.suptitle('Pairplot of Scaled Features by Species', y=1.02)
plt.show() # 

# 3. Visualize: Correlation Heatmap
plt.figure(figsize=(8, 6))
correlation_matrix = X_data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Feature Correlation Heatmap (Raw Data)')
plt.show()

# 4. Identify Potential Outliers (Boxplots)
plt.figure(figsize=(12, 5))
X_data.boxplot(column=feature_names)
plt.title('Boxplots to Identify Outliers')
plt.ylabel('Feature Value (cm)')
plt.show() # 

# =================================================================
# Task 1.d): Train/Test Split Function
# =================================================================

def split_data_80_20(features, target, random_state=42):
    """
    Splits the feature and target data into 80% training and 20% testing sets.
    """
    # Note: Using stratify=target ensures that all three species are represented 
    # proportionally in both the training and testing sets.
    X_train, X_test, y_train, y_test = train_test_split(
        features, 
        target, 
        test_size=0.20,  # 20% for testing (150 * 0.2 = 30 samples)
        random_state=random_state,
        stratify=target 
    )
    print("\n--- Data Split Complete ---")
    print(f"Total Samples: {len(features)}")
    print(f"Training Samples (80%): {len(X_train)}")
    print(f"Testing Samples (20%): {len(X_test)}")
    return X_train, X_test, y_train, y_test

# Execute the split function using the SCALED features
X_train, X_test, y_train, y_test = split_data_80_20(X_scaled_df, y_target)

# Store results for the next task (Model Training)
print("\nVariables ready for Task 2:")
print(f"X_train shape: {X_train.shape}")
print(f"y_test shape: {y_test.shape}")