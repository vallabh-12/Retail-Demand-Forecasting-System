-- CREATE OR REPLACE TABLE daily_demand AS
-- SELECT
--     DATE(invoice_timestamp) AS date,
--     stock_code,
--     country,
--     SUM(quantity) AS daily_quantity,
--     SUM(revenue) AS daily_revenue,
--     AVG(unit_price) AS avg_unit_price,
--     CASE
--         WHEN EXTRACT(ISODOW FROM DATE(invoice_timestamp)) IN (6, 7) THEN 1
--         ELSE 0
--     END AS is_weekend
-- FROM cleaned_retail
-- GROUP BY 1, 2, 3;

-- CREATE OR REPLACE TABLE model_features AS
-- WITH base AS (
--     SELECT
--         date,
--         stock_code,
--         country,
--         daily_quantity,
--         daily_revenue,
--         avg_unit_price,
--         is_weekend,
--         EXTRACT(DOW FROM date) AS day_of_week,
--         EXTRACT(MONTH FROM date) AS month,
--         EXTRACT(WEEK FROM date) AS week_of_year,
--         LAG(daily_quantity, 1) OVER (
--             PARTITION BY stock_code, country
--             ORDER BY date
--         ) AS lag_1,
--         LAG(daily_quantity, 7) OVER (
--             PARTITION BY stock_code, country
--             ORDER BY date
--         ) AS lag_7,
--         AVG(daily_quantity) OVER (
--             PARTITION BY stock_code, country
--             ORDER BY date
--             ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
--         ) AS rolling_mean_7,
--         SUM(daily_quantity) OVER (
--             PARTITION BY stock_code, country
--             ORDER BY date
--             ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
--         ) AS rolling_sum_7
--     FROM daily_demand
-- )
-- SELECT *
-- FROM base
-- WHERE lag_1 IS NOT NULL
--   AND lag_7 IS NOT NULL;

-- COPY model_features
-- TO 'data/processed/model_features.parquet'
-- (FORMAT PARQUET);



CREATE OR REPLACE TABLE daily_demand AS
SELECT
    DATE(invoice_timestamp) AS date,
    stock_code,
    country,
    SUM(quantity) AS daily_quantity,
    SUM(revenue) AS daily_revenue,
    AVG(unit_price) AS avg_unit_price,
    CASE
        WHEN date_part('isodow', DATE(invoice_timestamp)) IN (6, 7) THEN 1
        ELSE 0
    END AS is_weekend
FROM cleaned_retail
GROUP BY 1, 2, 3;

CREATE OR REPLACE TABLE model_features AS
WITH base AS (
    SELECT
        date,
        stock_code,
        country,
        daily_quantity,
        daily_revenue,
        avg_unit_price,
        is_weekend,
        date_part('dow', date) AS day_of_week,
        date_part('month', date) AS month,
        date_part('week', date) AS week_of_year,
        LAG(daily_quantity, 1) OVER (
            PARTITION BY stock_code, country
            ORDER BY date
        ) AS lag_1,
        LAG(daily_quantity, 7) OVER (
            PARTITION BY stock_code, country
            ORDER BY date
        ) AS lag_7,
        AVG(daily_quantity) OVER (
            PARTITION BY stock_code, country
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_mean_7,
        SUM(daily_quantity) OVER (
            PARTITION BY stock_code, country
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_sum_7
    FROM daily_demand
)
SELECT *
FROM base
WHERE lag_1 IS NOT NULL
  AND lag_7 IS NOT NULL;

COPY (
    SELECT * FROM model_features
) TO 'data/processed/model_features.parquet'
(FORMAT PARQUET);