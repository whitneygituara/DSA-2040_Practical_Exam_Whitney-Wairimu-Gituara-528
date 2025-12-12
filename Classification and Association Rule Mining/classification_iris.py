# ----------------------------
# 1. Import Libraries
# ----------------------------
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# 2. Load Preprocessed Data
# ----------------------------
df = pd.read_csv(r'C:\Users\Admin\OneDrive\Documents\USIU\Datawarehousing\EndSemExam\DSA-2040_Practical_Exam_Whitney-Wairimu-Gituara-528\Data_Mining\data\Formed_data\preprocessed_synthetic_iris.csv')

# Separate features and labels
X = df.iloc[:, :-1]
y = df.iloc[:, -1]  # species

# Encode labels for classifiers
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Convert class labels to strings for target_names
target_names = [str(c) for c in le.classes_]

# ----------------------------
# 3. Split Train/Test Set
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# ----------------------------
# 4. Decision Tree Classifier
# ----------------------------
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)

# Evaluate Decision Tree
accuracy_dt = accuracy_score(y_test, y_pred_dt)
precision_dt = precision_score(y_test, y_pred_dt, average='weighted')
recall_dt = recall_score(y_test, y_pred_dt, average='weighted')
f1_dt = f1_score(y_test, y_pred_dt, average='weighted')

print("Decision Tree Metrics:")
print(f"Accuracy: {accuracy_dt:.4f}")
print(f"Precision: {precision_dt:.4f}")
print(f"Recall: {recall_dt:.4f}")
print(f"F1-score: {f1_dt:.4f}\n")

# Fixed classification report
print("Decision Tree Classification Report:\n", classification_report(
    y_test,
    y_pred_dt,
    labels=np.arange(len(le.classes_)),
    target_names=target_names
))

# Visualize the Decision Tree
plt.figure(figsize=(12,8))
plot_tree(dt, feature_names=X.columns, class_names=target_names, filled=True, rounded=True)
plt.title("Decision Tree Visualization")
plt.savefig("decision_tree_iris.png")
plt.close()

# ----------------------------
# 5. K-Nearest Neighbors (k=5)
# ----------------------------
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

# Evaluate KNN
accuracy_knn = accuracy_score(y_test, y_pred_knn)
precision_knn = precision_score(y_test, y_pred_knn, average='weighted')
recall_knn = recall_score(y_test, y_pred_knn, average='weighted')
f1_knn = f1_score(y_test, y_pred_knn, average='weighted')

print("\nKNN (k=5) Metrics:")
print(f"Accuracy: {accuracy_knn:.4f}")
print(f"Precision: {precision_knn:.4f}")
print(f"Recall: {recall_knn:.4f}")
print(f"F1-score: {f1_knn:.4f}\n")

print("KNN Classification Report:\n", classification_report(
    y_test,
    y_pred_knn,
    labels=np.arange(len(le.classes_)),
    target_names=target_names
))

#-----------------------------
# 6. Compare Classifiers
# ----------------------------
if accuracy_dt > accuracy_knn:
    print(f"Decision Tree performed better (Accuracy: {accuracy_dt:.4f} vs KNN: {accuracy_knn:.4f})")
elif accuracy_knn > accuracy_dt:
    print(f"KNN performed better (Accuracy: {accuracy_knn:.4f} vs Decision Tree: {accuracy_dt:.4f})")
else:
    print(f"Both classifiers performed equally (Accuracy: {accuracy_dt:.4f})")