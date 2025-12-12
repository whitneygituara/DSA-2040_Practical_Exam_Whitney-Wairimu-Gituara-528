Classification Comparison: Decision Tree vs KNN

In this experiment, we trained two different classifiers on the preprocessed Iris dataset: a Decision Tree and a K-Nearest Neighbors (KNN) classifier with k=5. Both classifiers were evaluated on an 80/20 train-test split.

Decision Tree Performance:
The Decision Tree classifier achieved high performance across all metrics. The accuracy was 0.9333, indicating that it correctly classified approximately 93% of the test samples. Precision, recall, and F1-score were also similarly high, reflecting that the model effectively distinguished between the three species without significant misclassification. The tree visualization shows clear decision boundaries based on feature thresholds, which can be easily interpreted.

KNN Performance:
The KNN classifier achieved a slightly lower, but still competitive, performance. Accuracy was comparable to the Decision Tree, while precision, recall, and F1-score indicated that it correctly classified most samples, though it was slightly less precise in separating similar species. KNN relies on distance-based voting, so its performance can be affected by feature scaling and the choice of k.

Comparison and Analysis:
Overall, the Decision Tree performed marginally better than KNN on this dataset. Its advantage lies in its ability to model non-linear decision boundaries and provide interpretable rules for classification. KNN, on the other hand, is simpler and effective but can be sensitive to noise and feature scaling. For synthetic data, both classifiers performed very well, suggesting that the generated clusters were distinct and representative of real species patterns.

Real-World Implications:
Decision Trees are useful when interpretability is important, such as in medical diagnosis or feature-based decision making. KNN can be applied in scenarios where instance-based classification works well, like recommendation systems or anomaly detection. Selecting the right classifier depends on the dataset characteristics, interpretability needs, and computational constraints.