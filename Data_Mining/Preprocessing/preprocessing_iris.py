# preprocessing_iris_synthetic.py

# ----------------------------
# 1. Import libraries
# ----------------------------
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------
# 2. Load your generated synthetic dataset
# ----------------------------
df = pd.read_csv(r'C:\Users\Admin\OneDrive\Documents\USIU\Datawarehousing\EndSemExam\DSA-2040_Practical_Exam_Whitney-Wairimu-Gituara-528\Data_Mining\data\synthetic_iris.csv')  

print("First 5 rows of the dataset:")
print(df.head())

# ----------------------------
# 3. Preprocessing
# ----------------------------

# Check for missing values
print("\nMissing values per column:\n", df.isnull().sum())

# Separate features and labels
X = df.iloc[:, :-1]  # all columns except the last (assumes last column is 'species')
y = df.iloc[:, -1]   # last column as class label

# Normalize features
scaler = MinMaxScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Encode class labels (necessary for some ML models)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Combine scaled features with original species for exploration
df_scaled = X_scaled.copy()
df_scaled['species'] = y

# ----------------------------
# 4. Exploration
# ----------------------------

# Summary statistics
print("\nSummary statistics:\n", df_scaled.describe())

# Pairplot
sns.pairplot(df_scaled, hue='species')
plt.savefig("pairplot_synthetic_iris.png")
plt.close()

# Correlation heatmap
plt.figure(figsize=(8,6))
sns.heatmap(X_scaled.corr(), annot=True, cmap='coolwarm')
plt.title("Feature Correlation Heatmap")
plt.savefig("correlation_heatmap_synthetic_iris.png")
plt.close()

# Boxplots for potential outliers
plt.figure(figsize=(12,6))
sns.boxplot(data=X_scaled)
plt.title("Feature Boxplots for Outlier Detection")
plt.savefig("boxplots_synthetic_iris.png")
plt.close()

# ----------------------------
# 5. Train/Test Split Function
# ----------------------------
def split_data(X, y, test_size=0.2, random_state=42):
    """
    Splits features and labels into train/test sets
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

X_train, X_test, y_train, y_test = split_data(X_scaled, y_encoded)
print(f"\nTrain set size: {X_train.shape}, Test set size: {X_test.shape}")

# ----------------------------
# 6. Save preprocessed data
# ----------------------------
df_scaled.to_csv("preprocessed_synthetic_iris.csv", index=False)
print("\nPreprocessed synthetic data saved as 'preprocessed_synthetic_iris.csv'.")
