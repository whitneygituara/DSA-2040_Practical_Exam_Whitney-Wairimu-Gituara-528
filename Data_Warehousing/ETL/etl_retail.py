import pandas as pd  

# Load CSV
csv_path = r"C:\Users\Admin\OneDrive\Documents\USIU\Datawarehousing\EndSemExam\DSA-2040_Practical_Exam_Whitney-Wairimu-Gituara-528\Data_Warehousing\ETL\Online Retail.csv"  
data = pd.read_csv(csv_path, encoding='latin1')  

# Preview of first few rows
print("Preview of dataset:")
print(data.head())  

# Convertion of InvoiceDate to datetime
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')  
# errors='coerce' replaces bad dates with NaT

# Count missing values before cleaning
print("\nMissing values count:")
print(data.isna().sum())  

# Drop rows where essential columns are missing
data = data.dropna(subset=['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice', 'InvoiceDate'])  

# Fill missing CustomerID with 'Unknown'
data['CustomerID'] = data['CustomerID'].fillna('Unknown')
# Fill missing Description with 'No Description'
data['Description'] = data['Description'].fillna('No Description')

# Summary after cleaning
print("\nMissing values after cleaning:")
print(data.isna().sum())  
print("\nRows remaining after extraction and cleaning:", len(data))

# Transformation Steps
# This includes removing outliers and creating new calculated fields
# Remove outliers: drop rows where Quantity is negative or UnitPrice is zero or negative
data = data[(data['Quantity'] >= 0) & (data['UnitPrice'] > 0)]

# Calculate TotalSales
data['TotalSales'] = data['Quantity'] * data['UnitPrice']

# Extract Month, Quarter, and Year for time analysis
data['Month'] = data['InvoiceDate'].dt.month
data['Quarter'] = data['InvoiceDate'].dt.quarter
data['Year'] = data['InvoiceDate'].dt.year

# Create a customer summary table
customer_summary = data.groupby('CustomerID').agg({
    'TotalSales': 'sum',
    'InvoiceNo': 'count',
    'Country': 'first'
}).rename(columns={
    'InvoiceNo': 'TotalPurchases'
}).reset_index()

# Filter for sales in the last year (from Aug 12, 2025)
end_date = data['InvoiceDate'].max()
start_date = end_date - pd.DateOffset(years=1)
recent_sales = data[(data['InvoiceDate'] >= start_date) & (data['InvoiceDate'] <= end_date)]

# Sort recent sales by InvoiceDate
recent_sales = recent_sales.sort_values('InvoiceDate')

# Preview the transformed datasets
print("Recent sales preview(last year):")
print(recent_sales.head())

print("\nCustomer summary preview:")
print(customer_summary.head())

# Load section
# This section includes saving the transformed data to new CSV files
import sqlite3 #importing sqlite3 module

# Create/connect to a SQLite database file
conn = sqlite3.connect("retail_dw.db")
cursor = conn.cursor()

# -------------------------
# Creating Dimension Tables
# -------------------------

# Customer Dimension
cursor.execute("""
CREATE TABLE IF NOT EXISTS CustomerDim (
    CustomerID TEXT PRIMARY KEY,
    Country TEXT
)
""")

# Product Dimension
cursor.execute("""
CREATE TABLE IF NOT EXISTS ProductDim (
    StockCode TEXT PRIMARY KEY,
    Description TEXT
)
""")

# Time Dimension
cursor.execute("""
CREATE TABLE IF NOT EXISTS TimeDim (
    TimeID INTEGER PRIMARY KEY AUTOINCREMENT,
    InvoiceDate DATE,
    Year INTEGER,
    Quarter INTEGER,
    Month INTEGER
)
""")

# Country Dimension
cursor.execute("""
CREATE TABLE IF NOT EXISTS CountryDim (
    Country TEXT PRIMARY KEY
)
""")

# -------------------------
# Fact Table creation

cursor.execute("""
CREATE TABLE IF NOT EXISTS SalesFact (
    InvoiceNo TEXT,
    CustomerID TEXT,
    StockCode TEXT,
    InvoiceDate DATE,
    Quantity INTEGER,
    UnitPrice REAL,
    TotalSales REAL,
    FOREIGN KEY (CustomerID) REFERENCES CustomerDim(CustomerID),
    FOREIGN KEY (StockCode) REFERENCES ProductDim(StockCode),
    FOREIGN KEY (InvoiceDate) REFERENCES TimeDim(InvoiceDate)
)
""")

# ---------------------------------------------------
# Inserting data into Dimension Tables

# Customer Dimension
customer_data = data[['CustomerID', 'Country']].drop_duplicates()
customer_data.to_sql('CustomerDim', conn, if_exists='replace', index=False)

# Product Dimension
product_data = data[['StockCode', 'Description']].drop_duplicates()
product_data.to_sql('ProductDim', conn, if_exists='replace', index=False)

# Time Dimension
time_data = data[['InvoiceDate', 'Year', 'Quarter', 'Month']].drop_duplicates()
time_data.to_sql('TimeDim', conn, if_exists='replace', index=False)

# Country Dimension
country_data = data[['Country']].drop_duplicates()
country_data.to_sql('CountryDim', conn, if_exists='replace', index=False)

# Inserting data into the Fact Table
fact_data = data[['InvoiceNo', 'CustomerID', 'StockCode', 'InvoiceDate', 'Quantity', 'UnitPrice', 'TotalSales']]
fact_data.to_sql('SalesFact', conn, if_exists='replace', index=False)

# Commit and close connection
conn.commit()
conn.close()

print("Data loaded into retail_dw.db successfully!")

# Converting the files into csv files
# Connect to your existing database
conn = sqlite3.connect("retail_dw.db")

# Get a list of all tables in the database
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

print("Exporting tables...")

for table_name in tables["name"]:
    # Read each table into a DataFrame
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    
    # Export to CSV
    csv_name = f"{table_name}.csv"
    df.to_csv(csv_name, index=False)
    
    print(f"Saved: {csv_name}")

conn.close()
print("All tables exported successfully!")


# Function that performs the full ETL process and logs the number of rows processed at each stage.
def full_etl_process(csv_path, db_name="retail_dw.db"):
    """ 
    Performs the full ETL process: Extract, Transform, Load.
    Logs the number of rows at each stage.
    
    Parameters:
        csv_path (str): Path to the CSV file
        db_name (str): Name of the SQLite database file to create
    """
    try:
        # -------------------------
        # Extract
        # -------------------------
        print("=== Extract Stage ===")
        # Read CSV into a pandas DataFrame
        # This is the first step to bring raw data into Python for processing
        data = pd.read_csv(csv_path, encoding='latin1')
        print("Rows read from CSV:", len(data))
        
        # Convert InvoiceDate to datetime
        # This allows us to easily filter, sort, and extract time attributes
        data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')
        
        # Drop rows missing essential values to avoid errors in calculations or database load
        data = data.dropna(subset=['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice', 'InvoiceDate'])
        print("Rows after dropping essential missing values:", len(data))
        
        # Fill missing CustomerID with 'Unknown' to avoid null values in dimension table
        # This ensures every transaction is linked to a customer
        data['CustomerID'] = data['CustomerID'].fillna('Unknown')
        print("Rows after filling missing CustomerID:", len(data))
        
        # -------------------------
        # Transform
        # -------------------------
        print("\n=== Transform Stage ===")
        
        # Remove outliers: negative Quantity or non-positive UnitPrice
        # Outliers could distort totals and summaries, so we filter them out
        data = data[(data['Quantity'] >= 0) & (data['UnitPrice'] > 0)]
        print("Rows after removing outliers:", len(data))
        
        # Calculate TotalSales for each transaction
        # This will be used in the fact table for sales analysis
        data['TotalSales'] = data['Quantity'] * data['UnitPrice']
        
        # Extract Month, Quarter, and Year for time dimension
        # These are used to analyze sales over different periods
        data['Month'] = data['InvoiceDate'].dt.month
        data['Quarter'] = data['InvoiceDate'].dt.quarter
        data['Year'] = data['InvoiceDate'].dt.year
        
        # Add product Category for OLAP Slice (simple keyword matching)
        # Create a cleaned description to make matching easier
        data['Description_clean'] = data['Description'].astype(str).str.lower()

        def categorize(description):
            """Assign a product category based on keywords in the description."""
            # Electronics keywords
            electronics_keywords = ['usb', 'led', 'light', 'charger', 'battery', 'cable', 'phone', 'headphone', 'adapter', 'camera']
            if any(k in description for k in electronics_keywords):
                return 'Electronics'
            # Home Decor keywords
            home_keywords = ['lantern', 'candle', 'holder', 'hanging', 'bottle', 'vase', 'heart', 'decor', 'hottie']
            if any(k in description for k in home_keywords):
                return 'Home Decor'
            # Accessories keywords
            accessory_keywords = ['bag', 'wallet', 'purse', 'keyring', 'scarf', 'bracelet', 'ring']
            if any(k in description for k in accessory_keywords):
                return 'Accessories'
            # Toys keywords
            toy_keywords = ['toy', 'game', 'puzzle', 'doll']
            if any(k in description for k in toy_keywords):
                return 'Toys'
            # Clothing keywords
            clothing_keywords = ['shirt', 'dress', 'jeans', 'skirt', 'woolly', 'coat', 'jacket']
            if any(k in description for k in clothing_keywords):
                return 'Clothing'
            # Default fallback
            return 'Other'

        # Apply the categorization
        data['Category'] = data['Description_clean'].apply(categorize)

        # Drop helper column
        data = data.drop(columns=['Description_clean'])

        # Create customer summary table for CustomerDim
        # Aggregates total sales, total purchases, and keeps country info
        customer_summary = data.groupby('CustomerID').agg({
            'TotalSales': 'sum',
            'InvoiceNo': 'count',
            'Country': 'first'
        }).rename(columns={'InvoiceNo': 'TotalPurchases'}).reset_index()
        print("Customer summary rows:", len(customer_summary))
        
        # Filter recent sales (Aug 12, 2024 → Aug 12, 2025)
        # This creates a subset for analyzing last year’s performance
        end_date = data['InvoiceDate'].max()
        start_date = end_date - pd.DateOffset(years=1)
        recent_sales = data[(data['InvoiceDate'] >= start_date) & (data['InvoiceDate'] <= end_date)]
        print("Recent sales rows (last year):", len(recent_sales))
        # -------------------------
        # Load
        # -------------------------
        print("\n=== Load Stage ===")
        try:
            # Connect to SQLite database
            # Using a database allows us to store structured data for reporting and analysis
            conn = sqlite3.connect(db_name)
            
            # Load dimension tables first
            # Dimensions contain descriptive data used to categorize and filter facts
            customer_summary.to_sql('CustomerDim', conn, if_exists='replace', index=False)
            
            # Product dimension: unique products with description
            product_data = data[['StockCode', 'Description', 'Category']].drop_duplicates()
            product_data.to_sql('ProductDim', conn, if_exists='replace', index=False)
            
            # Time dimension: unique invoice dates with extracted Year, Quarter, Month
            time_data = data[['InvoiceDate', 'Year', 'Quarter', 'Month']].drop_duplicates()
            time_data.to_sql('TimeDim', conn, if_exists='replace', index=False)
            
            # Country dimension: unique countries
            country_data = data[['Country']].drop_duplicates()
            country_data.to_sql('CountryDim', conn, if_exists='replace', index=False)
            
            # Load fact table after dimensions
            # Facts contain measurable data (sales, quantities) and link to dimensions via keys
            fact_data = data[['InvoiceNo', 'CustomerID', 'StockCode', 'InvoiceDate', 'Quantity', 'UnitPrice', 'TotalSales','Country']]
            fact_data.to_sql('SalesFact', conn, if_exists='replace', index=False)
            
            conn.commit()
            print("Data loaded into database:", db_name)
            print("Fact table rows:", len(fact_data))
        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            conn.close()
            
    except FileNotFoundError:
        print(f"Error: CSV file not found at path: {csv_path}")
    except pd.errors.ParserError:
        print("Error: Could not parse CSV file. Check file format.")
    except Exception as e:
        print("Unexpected error:", e)
        

# testing the full etl process function
full_etl_process(r"C:\Users\Admin\OneDrive\Documents\USIU\Datawarehousing\EndSemExam\DSA-2040_Practical_Exam_Whitney-Wairimu-Gituara-528\Data_Warehousing\ETL\Online Retail.csv")

# Task 3: OLAP Queries and Analysis 
# Connect to SQLite database
conn = sqlite3.connect("retail_dw.db")
# Roll-up: Total sales by country and quarter (group by country and quarter from TimeDim).
roll_up_query = """
SELECT f.Country, t.Quarter, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN TimeDim t ON f.InvoiceDate = t.InvoiceDate
GROUP BY f.Country, t.Quarter
ORDER BY f.Country, t.Quarter;
"""

# Execute query and load results into a DataFrame
roll_up_df = pd.read_sql_query(roll_up_query, conn)
print(roll_up_df)

# Drill-down: Detailed sales transactions for a specific country in a specific month.
drill_down_query = """
SELECT t.Month, SUM(f.TotalSales) AS MonthlySales
FROM SalesFact f
JOIN TimeDim t ON f.InvoiceDate = t.InvoiceDate
WHERE f.Country = 'United Kingdom'
GROUP BY t.Month
ORDER BY t.Month;
"""

# Execute query and load results into a DataFrame
drill_down_df = pd.read_sql_query(drill_down_query, conn)
print(drill_down_df)

# Slice:Total sales for electronics category (assume you categorize products; add a category column during transform or generation if needed).
slice_query = """
SELECT p.Category, SUM(f.TotalSales) AS TotalSales
FROM SalesFact f
JOIN ProductDim p ON f.StockCode = p.StockCode
WHERE p.Category = 'Electronics'
GROUP BY p.Category;
"""

# Execute query and load results into a DataFrame
slice_df = pd.read_sql_query(slice_query, conn)
print(slice_df)

# Close connection
conn.close()

#--------------------VISUALIZATION-----------------
#Visualizations for OLAP results
import matplotlib.pyplot as plt
# Aggregated Sales by Country and Quarter (Roll-up)
country_sales = roll_up_df.groupby('Country')['TotalSales'].sum().sort_values(ascending=False)
print(country_sales.head())

# Plotting the aggregated sales by country
plt.figure(figsize=(10,6))
country_sales.plot(kind='bar', color='skyblue')
plt.title('Total Sales by Country')
plt.xlabel('Country')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.savefig('sales_by_country.png')  # saves as PNG file
plt.show()  # displays the chart

