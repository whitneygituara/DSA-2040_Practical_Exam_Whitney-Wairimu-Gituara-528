# ----------------------------
# 1. Import Libraries
# ----------------------------
import random
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# ----------------------------
# 2. Generate Synthetic Transactional Data
# ----------------------------
items_pool = ['milk', 'bread', 'beer', 'diapers', 'eggs', 
              'rice','juice','banana','chocolate','onion',
              'cheese', 'butter', 'apple', 'banana', 'chicken',
              'rice', 'cereal', 'yogurt', 'juice', 'coffee',
              'tea', 'cookies', 'chocolate', 'tomato', 'onion']

num_transactions = 30  # adjust between 20-50
transactions = []

for _ in range(num_transactions):
    basket_size = random.randint(3, 8)  # 3-8 items per basket
    basket = random.choices(items_pool, k=basket_size)
    transactions.append(list(set(basket)))  # remove duplicates in a basket

# Save generated transactions
pd.DataFrame({'Transaction': transactions}).to_csv('synthetic_transactions.csv', index=False)
print("--- Synthetic Transactions Generated and Saved as 'synthetic_transactions.csv' ---")
print("\nSample Transactions:\n", pd.DataFrame({'Transaction': transactions}).head())

# ----------------------------
# 3. One-Hot Encode Transactions
# ----------------------------
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_onehot = pd.DataFrame(te_ary, columns=te.columns_)

# ----------------------------
# 4. Apply Apriori Algorithm
# ----------------------------
frequent_itemsets = apriori(df_onehot, min_support=0.1, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

# Sort rules by lift
rules_sorted = rules.sort_values(by='lift', ascending=False)
print("\nTop 5 Association Rules by Lift:")
print(rules_sorted.head(5))

# ----------------------------
# 5. Analyze Top Rule
# ----------------------------
if not rules_sorted.empty:
    top_rule = rules_sorted.iloc[0]

    analysis_text = f"""
Top Rule Analysis:

Rule: {list(top_rule['antecedents'])} -> {list(top_rule['consequents'])}
Support: {top_rule['support']:.2f}
Confidence: {top_rule['confidence']:.2f}
Lift: {top_rule['lift']:.2f}

Implications: This rule suggests that customers who buy {list(top_rule['antecedents'])} are 
likely to also buy {list(top_rule['consequents'])}. Retailers can use this information for 
cross-selling strategies, product placement, and targeted promotions to increase sales.
"""
    print(analysis_text)

    # Save analysis to text file
    with open("association_rule_analysis.txt", "w") as f:
        f.write(analysis_text)
    print("\nAnalysis saved to 'association_rule_analysis.txt'.")
else:
    print("No association rules were found with the given support and confidence thresholds.")
    

# Prepare labels for top 5 rules
top5_rules = rules_sorted.head(5)
rule_labels = [f"{list(a)} -> {list(c)}" for a, c in zip(top5_rules['antecedents'], top5_rules['consequents'])]
lifts = top5_rules['lift']

# ----------------------------
# 6. Visualize Top 5 Rules by Lift
# ----------------------------
import matplotlib.pyplot as plt
# Create bar chart
plt.figure(figsize=(10,6))
plt.barh(rule_labels, lifts, color='skyblue')
plt.xlabel('Lift')
plt.title('Top 5 Association Rules by Lift')
plt.gca().invert_yaxis()  # highest lift on top
plt.tight_layout()
plt.savefig("top5_rules_lift.png")
plt.show()
