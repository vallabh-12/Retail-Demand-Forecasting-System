CREATE OR REPLACE TABLE raw_retail AS
SELECT *
FROM read_csv_auto('data/raw/online_retail_raw.csv', HEADER=TRUE);

CREATE OR REPLACE TABLE cleaned_retail AS
SELECT
    CAST(InvoiceNo AS VARCHAR) AS invoice_no,
    CAST(StockCode AS VARCHAR) AS stock_code,
    CAST(Description AS VARCHAR) AS description,
    CAST(Quantity AS INTEGER) AS quantity,
    try_strptime(CAST(InvoiceDate AS VARCHAR), '%m/%d/%Y %H:%M') AS invoice_timestamp,
    CAST(UnitPrice AS DOUBLE) AS unit_price,
    CAST(CustomerID AS VARCHAR) AS customer_id,
    CAST(Country AS VARCHAR) AS country,
    CAST(Quantity AS DOUBLE) * CAST(UnitPrice AS DOUBLE) AS revenue
FROM raw_retail
WHERE Quantity IS NOT NULL
  AND UnitPrice IS NOT NULL
  AND InvoiceDate IS NOT NULL
  AND StockCode IS NOT NULL
  AND Quantity > 0
  AND UnitPrice > 0
  AND InvoiceNo NOT LIKE 'C%'
  AND try_strptime(CAST(InvoiceDate AS VARCHAR), '%m/%d/%Y %H:%M') IS NOT NULL;