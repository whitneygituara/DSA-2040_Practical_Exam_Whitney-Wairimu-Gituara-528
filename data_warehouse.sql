-- Dimension Tables:
-- 1. Customer Dimension
CREATE TABLE Customer (
    CustomerID INTEGER PRIMARY KEY,
    Country TEXT
);

-- 2. Product Dimension
CREATE TABLE Product (
    StockCode TEXT PRIMARY KEY,
    Description TEXT
);

-- 3. Time Dimension
CREATE TABLE Time (
    TimeID INTEGER PRIMARY KEY,
    InvoiceDate TEXT,
    Month INTEGER,
    Quarter INTEGER,
    Year INTEGER
);

-- Fact Table

-- Sales Fact Table
CREATE TABLE Sales (
    InvoiceNo TEXT PRIMARY KEY,
    CustomerID INTEGER,
    StockCode TEXT,
    TimeID INTEGER,
    Quantity INTEGER,
    UnitPrice REAL,
    TotalAmount REAL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (StockCode) REFERENCES Product(StockCode),
    FOREIGN KEY (TimeID) REFERENCES Time(TimeID)
);
