import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("retail_dw.db")

# Roll-up query
rollup_query = """
SELECT c.Country, t.Quarter, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerID = c.CustomerID
JOIN TimeDim t ON f.InvoiceDate = t.InvoiceDate
GROUP BY c.Country, t.Quarter
ORDER BY c.Country, t.Quarter;
"""
rollup_df = pd.read_sql_query(rollup_query, conn)
print(rollup_df.head())

# Drill-down query (example for United Kingdom)
drill_query = """
SELECT t.Year, t.Month, SUM(f.TotalSales) AS MonthlySales
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerID = c.CustomerID
JOIN TimeDim t ON f.InvoiceDate = t.InvoiceDate
WHERE c.Country = 'United Kingdom'
GROUP BY t.Year, t.Month
ORDER BY t.Year, t.Month;
"""
drill_df = pd.read_sql_query(drill_query, conn)
print(drill_df.head())

# Slice query (Electronics)
slice_query = """
SELECT p.Category, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN ProductDim p ON f.StockCode = p.StockCode
WHERE p.Category = 'Electronics'
GROUP BY p.Category;
"""
slice_df = pd.read_sql_query(slice_query, conn)
print(slice_df)

# Close connection
conn.close()


