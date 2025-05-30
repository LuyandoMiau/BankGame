/*
    This file contains SQL queries to analyze the customers data.
    The queries are designed to extract insights from the data and are grouped by their purpose.
    Each query is preceded by a comment explaining its purpose.
*/

-- BY TYPE OF CREDIT QUERIES ------------------------------------------------------------------------

-- Query to analyze customer financials by type of credit
-- This query groups customers by their "type of credit" and calculates:
--   - the number of customers in each type,
--   - the average monthly income,
--   - the average monthly expenditure,
--   - and the average monthly savings (income minus expenditure) for each type.
-- The results are ordered by average monthly savings in ascending order,
-- helping to identify which types have the lowest or highest average savings.
SELECT "type of credit", 
    COUNT("type of credit") AS "number of customers",
    AVG("monthly income") AS "average monthly income", 
    AVG("monthly expenditure") AS "average monthly expenditure",
    AVG("monthly income") - AVG("monthly expenditure") AS "average monthly savings"
FROM customers_data_for_queries
GROUP BY "type of credit"
ORDER BY "average monthly savings" ASC;

-- Query to analyze savings (debt) distribution by type of credit using percentiles
-- This query groups customers by their "type of credit" and calculates:
--   - the number of customers in each type,
--   - the average, maximum, and minimum "savings (debt)" for each type,
--   - and approximate 25th, 50th, and 75th percentile values of "savings (debt)" within each type using quartiles.
-- The results are ordered by the average monthly savings/debt in ascending order,
-- allowing comparison of savings (debt) distribution and spread across different types of credit.
WITH ranked_data_1 AS (
    SELECT
    "type of credit",
    "savings (debt)",
    NTILE(4) OVER (PARTITION BY "type of credit" ORDER BY "savings (debt)") AS quartile
    FROM customers_data_for_queries
)
SELECT "type of credit",
    COUNT(*) AS "number of customers",
    AVG("savings (debt)") AS "average monthly savings/debt",
    MAX("savings (debt)") AS "maximum savings/debt",
    MIN("savings (debt)") AS "minimum savings/debt",
    -- Get approximate 25th, 50th, 75th percentile values
    MAX(CASE WHEN quartile = 1 THEN "savings (debt)" END) AS "25th percentile approx",
    MAX(CASE WHEN quartile = 2 THEN "savings (debt)" END) AS "50th percentile approx",
    MAX(CASE WHEN quartile = 3 THEN "savings (debt)" END) AS "75th percentile approx"
FROM ranked_data_1
GROUP BY "type of credit"
ORDER BY "average monthly savings/debt" ASC;

-- Query to analyze collateral and estimated seizable assets distribution by type of credit using percentiles
-- This enhanced query groups customers by their "type of credit" and calculates:
--   - the number of customers in each type,
--   - the average, maximum, and minimum values for both "collateral" and "estimated seizable assets" in each type,
--   - and approximate 25th, 50th, and 75th percentile values for both "collateral" and "estimated seizable assets" within each type using quartiles.
-- The results are ordered by the average collateral value in ascending order,
-- providing a comprehensive comparison of collateral and asset value distributions across different types of credit.
WITH ranked_collateral AS (
    SELECT
    "type of credit",
    "collateral",
    NTILE(4) OVER (PARTITION BY "type of credit" ORDER BY "collateral") AS collateral_quartile
    FROM customers_data_for_queries
),
ranked_assets AS (
    SELECT
    "type of credit",
    "estimated seizable assets",
    NTILE(4) OVER (PARTITION BY "type of credit" ORDER BY "estimated seizable assets") AS assets_quartile
    FROM customers_data_for_queries
)
SELECT
    c."type of credit",
    COUNT(*) AS "number of customers",
    -- Collateral statistics
    AVG(c."collateral") AS "average collateral value",
    MAX(c."collateral") AS "maximum collateral value",
    MIN(c."collateral") AS "minimum collateral value",
    MAX(CASE WHEN c.collateral_quartile = 1 THEN c."collateral" END) AS "25th percentile collateral approx",
    MAX(CASE WHEN c.collateral_quartile = 2 THEN c."collateral" END) AS "50th percentile collateral approx",
    MAX(CASE WHEN c.collateral_quartile = 3 THEN c."collateral" END) AS "75th percentile collateral approx",
    -- Estimated seizable assets statistics
    AVG(a."estimated seizable assets") AS "average estimated seizable assets",
    MAX(a."estimated seizable assets") AS "maximum estimated seizable assets",
    MIN(a."estimated seizable assets") AS "minimum estimated seizable assets",
    MAX(CASE WHEN a.assets_quartile = 1 THEN a."estimated seizable assets" END) AS "25th percentile assets approx",
    MAX(CASE WHEN a.assets_quartile = 2 THEN a."estimated seizable assets" END) AS "50th percentile assets approx",
    MAX(CASE WHEN a.assets_quartile = 3 THEN a."estimated seizable assets" END) AS "75th percentile assets approx"
FROM ranked_collateral c
JOIN ranked_assets a
    ON c."type of credit" = a."type of credit"
GROUP BY c."type of credit"
ORDER BY "average estimated seizable assets" ASC;

-- Query to analyze the distribution of unpaid past credits by type of credit using percentiles
-- This query groups customers by their "type of credit" and calculates:
--   - the number of customers in each type,
--   - the average, maximum, and minimum "number of not paid past credits" for each type,
--   - and approximate 25th, 50th, and 75th percentile values of "number of not paid past credits" within each type using quartiles.
-- The results are ordered by the average number of not paid past credits in ascending order,
-- allowing comparison of credit repayment issues across different types of credit.
WITH ranked_data_3 AS (
    SELECT
    "type of credit",
    "number of not paid past credits",
    NTILE(4) OVER (PARTITION BY "type of credit" ORDER BY "number of not paid past credits") AS quartile
    FROM customers_data_for_queries
)
SELECT
    "type of credit",
    COUNT(*) AS "number of customers",
    AVG("number of not paid past credits") AS "average number of not paid past credits",
    MAX("number of not paid past credits") AS "maximum number of not paid past credits",
    MIN("number of not paid past credits") AS "minimum number of not paid past credits",
    -- Get approximate 25th, 50th, 75th percentile values
    MAX(CASE WHEN quartile = 1 THEN "number of not paid past credits" END) AS "25th percentile approx",
    MAX(CASE WHEN quartile = 2 THEN "number of not paid past credits" END) AS "50th percentile approx",
    MAX(CASE WHEN quartile = 3 THEN "number of not paid past credits" END) AS "75th percentile approx"
FROM ranked_data_3
GROUP BY "type of credit"
ORDER BY "average number of not paid past credits" ASC;

-- Query to analyze credit monthly amount and loan duration by type of credit using percentiles
-- This query groups customers by their "type of credit" and calculates:
--   - the number of customers in each type,
--   - the average, maximum, and minimum "credit: monthly amount" for each type,
--   - the average "requested_loan_duration" for each type,
--   - and approximate 25th, 50th, and 75th percentile values of "credit: monthly amount" within each type using quartiles.
-- The results are ordered by the average credit monthly amount in ascending order,
-- allowing comparison of credit and loan duration distribution across different types of credit.
WITH ranked_data_4 AS (
    SELECT
    "type of credit",
    "credit: monthly amount",
    "requested_loan_duration",
    NTILE(4) OVER (PARTITION BY "type of credit" ORDER BY "credit: monthly amount", "requested_loan_duration") AS quartile
    FROM customers_data_for_queries
)   
SELECT
    "type of credit",
    COUNT(*) AS "number of customers",
    AVG("requested_loan_duration") AS "average requested_loan_duration",
    AVG("credit: monthly amount") AS "average credit: monthly amount",
    MAX("credit: monthly amount") AS "maximum credit: monthly amount",
    MIN("credit: monthly amount") AS "minimum credit: monthly amount",
    -- Get approximate 25th, 50th, 75th percentile values
    MAX(CASE WHEN quartile = 1 THEN "credit: monthly amount" END) AS "25th percentile approx",
    MAX(CASE WHEN quartile = 2 THEN "credit: monthly amount" END) AS "50th percentile approx",
    MAX(CASE WHEN quartile = 3 THEN "credit: monthly amount" END) AS "75th percentile approx"
FROM ranked_data_4
GROUP BY "type of credit"
ORDER BY "credit: monthly amount" ASC;

-- Query to analyze the credit-to-income ratio by type of credit using percentiles
-- This query groups customers by their "type of credit" and calculates:
--   - the number of customers in each type,
--   - the average, maximum, and minimum "credit-to-income ratio" for each type,
--   - and approximate 25th, 50th, and 75th percentile values of "credit-to-income ratio" within each type using quartiles.
-- The results are ordered by the average credit-to-income ratio in ascending order,
-- allowing comparison of credit burden relative to income across different types of credit.
WITH ranked_data_5 AS (
    SELECT
    "type of credit",
    "credit-to-income ratio",
    NTILE(4) OVER (PARTITION BY "type of credit" ORDER BY "credit-to-income ratio") AS quartile
    FROM customers_data_for_queries
)
SELECT
    "type of credit",
    COUNT(*) AS "number of customers",
    AVG("credit-to-income ratio") AS "average credit-to-income ratio",
    MAX("credit-to-income ratio") AS "maximum credit-to-income ratio",
    MIN("credit-to-income ratio") AS "minimum credit-to-income ratio",
    -- Get approximate 25th, 50th, 75th percentile values
    MAX(CASE WHEN quartile = 1 THEN "credit-to-income ratio" END) AS "25th percentile approx",
    MAX(CASE WHEN quartile = 2 THEN "credit-to-income ratio" END) AS "50th percentile approx",
    MAX(CASE WHEN quartile = 3 THEN "credit-to-income ratio" END) AS "75th percentile approx"
FROM ranked_data_5
GROUP BY "type of credit"
ORDER BY "average credit-to-income ratio" ASC;

-- Query to analyze and rank debt-to-income ratios before and after credit by type of credit
-- This query groups customers by their "type of credit" and calculates:
--   - the number of customers in each type,
--   - the average, maximum, and minimum "debt-to-income ratio before credit" and "debt-to-income ratio after credit" for each type,
--   - approximate 25th, 50th, and 75th percentile values for both ratios using quartiles,
--   - the rank of each type by average debt-to-income ratio before credit,
--   - the rank of each type by average debt-to-income ratio after credit,
--   - and the change in rank after credit (positive means the type moved up, negative means it moved down).
-- The results are ordered by the before and after credit ranks.

WITH type_averages AS (
    SELECT
    "type of credit",
    COUNT(*) AS "number of customers",
    AVG("debt-to-income ratio before credit") AS "average debt-to-income ratio before credit",
    AVG("debt-to-income ratio after credit") AS "average debt-to-income ratio after credit"
    FROM customers_data_for_queries
    GROUP BY "type of credit"
),
ranked_before AS (
    SELECT
    "type of credit",
    "average debt-to-income ratio before credit",
    RANK() OVER (ORDER BY "average debt-to-income ratio before credit" ASC) AS "rank before credit"
    FROM type_averages
),
ranked_after AS (
    SELECT
    "type of credit",
    "average debt-to-income ratio after credit",
    RANK() OVER (ORDER BY "average debt-to-income ratio after credit" ASC) AS "rank after credit"
    FROM type_averages
),
percentiles AS (
    SELECT
    "type of credit",
    MAX(CASE WHEN quartile = 1 THEN "debt-to-income ratio before credit" END) AS "25th percentile approx before credit",
    MAX(CASE WHEN quartile = 2 THEN "debt-to-income ratio before credit" END) AS "50th percentile approx before credit",
    MAX(CASE WHEN quartile = 3 THEN "debt-to-income ratio before credit" END) AS "75th percentile approx before credit",
    MAX(CASE WHEN quartile = 1 THEN "debt-to-income ratio after credit" END) AS "25th percentile approx after credit",
    MAX(CASE WHEN quartile = 2 THEN "debt-to-income ratio after credit" END) AS "50th percentile approx after credit",
    MAX(CASE WHEN quartile = 3 THEN "debt-to-income ratio after credit" END) AS "75th percentile approx after credit"
    FROM (
    SELECT
        "type of credit",
        "debt-to-income ratio before credit",
        "debt-to-income ratio after credit",
        NTILE(4) OVER (PARTITION BY "type of credit" ORDER BY "debt-to-income ratio before credit") AS quartile
    FROM customers_data_for_queries
    ) q
    GROUP BY "type of credit"
)
SELECT
    ta."type of credit",
    ta."number of customers",
    ta."average debt-to-income ratio before credit",
    rb."rank before credit",
    ta."average debt-to-income ratio after credit",
    ra."rank after credit",
    (rb."rank before credit" - ra."rank after credit") AS "rank change after credit",
    -- Percentiles for before and after credit
    p."25th percentile approx before credit",
    p."25th percentile approx after credit",
    p."50th percentile approx before credit",
    p."50th percentile approx after credit",
    p."75th percentile approx before credit",
    p."75th percentile approx after credit"
FROM type_averages ta
JOIN ranked_before rb ON ta."type of credit" = rb."type of credit"
JOIN ranked_after ra ON ta."type of credit" = ra."type of credit"
JOIN percentiles p ON ta."type of credit" = p."type of credit"
ORDER BY rb."rank before credit" ASC, ra."rank after credit" ASC;
