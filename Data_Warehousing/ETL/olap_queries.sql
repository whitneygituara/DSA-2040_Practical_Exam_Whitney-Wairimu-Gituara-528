-- Roll-up Query: Total sales by Country and Quarter
SELECT 
    c.Country,
    t.Quarter,
    SUM(f.TotalSales) AS TotalSales
FROM SalesFact AS f
JOIN CountryDim AS c ON f.Country = c.Country
JOIN TimeDim AS t ON f.InvoiceDate = t.InvoiceDate
GROUP BY c.Country, t.Quarter
ORDER BY c.Country, t.Quarter;

-- Drill-down Query: Detailed sales transactions for a specific Country in a specific Month
-- DRILL-DOWN: Monthly sales for United Kingdom
SELECT 
    t.Year,
    t.Month,
    SUM(f.TotalSales) AS MonthlySales
FROM SalesFact AS f
JOIN TimeDim AS t 
    ON f.InvoiceDate = t.InvoiceDate
JOIN CountryDim AS c 
    ON f.Country = c.Country
WHERE c.Country = 'United Kingdom'
GROUP BY t.Year, t.Month
ORDER BY t.Year, t.Month;

-- 3. SLICE: Total sales for Electronics category
SELECT 
    SUM(f.TotalSales) AS ElectronicsSales
FROM SalesFact AS f
JOIN ProductDim AS p
    ON f.StockCode = p.StockCode
WHERE p.Category = 'Electronics';
-- Note: Ensure that the ProductDim table has a 'Category' column for this query to work.