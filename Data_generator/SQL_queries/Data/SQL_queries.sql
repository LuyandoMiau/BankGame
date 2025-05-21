/*
    This file contains SQL queries to analyze the customers data.
    The queries are designed to extract insights from the data and are grouped by their purpose.
    Each query is preceded by a comment explaining its purpose.
*/


-- Query to analyze customer financials by working sector
-- This query groups customers by their "working sector" and calculates:
--   - the number of customers in each sector,
--   - the average monthly income,
--   - the average monthly expenditure,
--   - and the average monthly savings (income minus expenditure) for each sector.
-- The results are ordered by average monthly savings in ascending order,
-- helping to identify which sectors have the lowest or highest average savings.
SELECT "working sector", 
        COUNT("working sector") AS "number of customers",
        AVG("monthly income") AS "average monthly income", 
        AVG("monthly expenditure") AS "average monthly expenditure",
        AVG("monthly income") - AVG("monthly expenditure") AS "average monthly savings"
FROM customers_data_for_queries
GROUP BY "working sector"
ORDER BY "average monthly savings" ASC;

-- Query to analyze customer financials by number of dependents
-- This query groups customers by their "dependents" count and calculates:
--   - the number of customers in each group,
--   - the average monthly income,
--   - the average monthly expenditure,
--   - and the average monthly savings (income minus expenditure) for each group.
-- The results are ordered by average monthly savings in ascending order,
-- helping to identify how the number of dependents affects savings.
SELECT "dependents", 
        COUNT("dependents") AS "number of customers",
        AVG("monthly income") AS "average monthly income",
        AVG("monthly expenditure") AS "average monthly expenditure",
        AVG("monthly income") - AVG("monthly expenditure") AS "average monthly savings"
FROM customers_data_for_queries
GROUP BY "dependents"
ORDER BY "average monthly savings" ASC;
 
-- Query to analyze customer financials by profession and credit history
-- This query groups customers by their "profession" and "number of not paid past credits" and calculates:
--   - the number of customers in each group,
--   - the average monthly income,
--   - the average monthly expenditure,
--   - and the average monthly savings (income minus expenditure) for each group.
-- The results are ordered by number of customers in ascending order.
SELECT "profession",
        "number of not paid past credits",
        COUNT("profession") AS "number of customers",
        AVG("monthly income") AS "average monthly income",
        AVG("monthly expenditure") AS "average monthly expenditure",
        AVG("monthly income") - AVG("monthly expenditure") AS "average monthly savings"
FROM customers_data_for_queries
GROUP BY "profession", "number of not paid past credits"
ORDER BY "number of customers" ASC;

-- Query to analyze savings (debt) distribution by working sector using percentiles
-- This query groups customers by their "working sector" and calculates:
--   - the number of customers in each sector,
--   - the average, maximum, and minimum "savings (debt)" for each sector,
--   - and approximate 25th, 50th, and 75th percentile values of "savings (debt)" within each sector using quartiles.
-- The results are ordered by the number of customers in ascending order,
-- allowing comparison of savings (debt) distribution and spread across different working sectors.
WITH ranked_data_1 AS (
    SELECT
        "working sector",
        "savings (debt)",
        NTILE(4) OVER (PARTITION BY "working sector" ORDER BY "savings (debt)") AS quartile
    FROM customers_data_for_queries
)
SELECT "working sector",
        COUNT(*) AS "number of customers",
        AVG("savings (debt)") AS "average monthly savings/debt",
        MAX("savings (debt)") AS "maximum savings/debt",
        MIN("savings (debt)") AS "minimum savings/debt",
        -- Get approximate 25th, 50th, 75th percentile values
        MAX(CASE WHEN quartile = 1 THEN "savings (debt)" END) AS "25th percentile approx",
        MAX(CASE WHEN quartile = 2 THEN "savings (debt)" END) AS "50th percentile approx",
        MAX(CASE WHEN quartile = 3 THEN "savings (debt)" END) AS "75th percentile approx"
FROM ranked_data_1
GROUP BY "working sector"
ORDER BY "number of customers" ASC;

-- Query to analyze collateral value distribution by working sector using percentiles
-- This query groups customers by their "working sector" and calculates:
--   - the number of customers in each sector,
--   - the average, maximum, and minimum "collateral value" for each sector,
--   - and approximate 25th, 50th, and 75th percentile values of "collateral" within each sector using quartiles.
-- The results are ordered by the number of customers in ascending order,
-- allowing comparison of collateral value distribution and spread across different working sectors.
WITH ranked_data_2 AS (
    SELECT
        "working sector",
        "collateral",
        NTILE(4) OVER (PARTITION BY "working sector" ORDER BY "collateral") AS quartile
    FROM customers_data_for_queries
)
SELECT
    "working sector",
    COUNT(*) AS "number of customers",
    AVG("collateral") AS "average collateral value",
    MAX("collateral") AS "maximum collateral value",
    MIN("collateral") AS "minimum collateral value",
    -- Get approximate 25th, 50th, 75th percentile values
    MAX(CASE WHEN quartile = 1 THEN "collateral" END) AS "25th percentile approx",
    MAX(CASE WHEN quartile = 2 THEN "collateral" END) AS "50th percentile approx",
    MAX(CASE WHEN quartile = 3 THEN "collateral" END) AS "75th percentile approx"
FROM ranked_data_2
GROUP BY "working sector"
ORDER BY "number of customers" ASC;


