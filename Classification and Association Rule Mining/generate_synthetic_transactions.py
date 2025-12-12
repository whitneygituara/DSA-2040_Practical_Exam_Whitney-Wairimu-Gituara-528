import random
import pandas as pd

# Define the pool of items
items_pool = ['milk', 'bread', 'beer', 'diapers', 'eggs', 
              'cheese', 'butter', 'apple', 'banana', 'chicken',
              'rice', 'cereal', 'yogurt', 'juice', 'coffee',
              'tea', 'cookies', 'chocolate', 'tomato', 'onion']

# Number of transactions
num_transactions = 30  # you can adjust between 20-50

# Generate transactions
transactions = []
for _ in range(num_transactions):
    basket_size = random.randint(3, 8)  # each basket has 3-8 items
    basket = random.choices(items_pool, k=basket_size)
    transactions.append(list(set(basket)))  # remove duplicates within basket

# Save transactions to CSV
synthetic_transactions = pd.DataFrame({'Transaction': transactions})
synthetic_transactions.to_csv('synthetic_transactions.csv', index=False)
print("Synthetic Transactions Generated and Saved as 'synthetic_transactions.csv' ")

print("Sample Transactions:")
print(synthetic_transactions.head())
