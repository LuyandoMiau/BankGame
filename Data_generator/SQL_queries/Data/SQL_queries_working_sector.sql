/*
    This file contains SQL queries to analyze the customers data.
    The queries are designed to extract insights from the data and are grouped by their purpose.
    Each query is preceded by a comment explaining its purpose.
*/

-- BY WORKING SECTOR QUERIES ------------------------------------------------------------------------

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

-- Query to analyze savings (debt) distribution by working sector using percentiles
-- This query groups customers by their "working sector" and calculates:
--   - the number of customers in each sector,
--   - the average, maximum, and minimum "savings (debt)" for each sector,
--   - and approximate 25th, 50th, and 75th percentile values of "savings (debt)" within each sector using quartiles.
-- The results are ordered by the average monthly savings/debt in ascending order,
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
ORDER BY "average monthly savings/debt" ASC;

-- Query to analyze collateral and estimated seizable assets distribution by working sector using percentiles
-- This enhanced query groups customers by their "working sector" and calculates:
--   - the number of customers in each sector,
--   - the average, maximum, and minimum values for both "collateral" and "estimated seizable assets" in each sector,
--   - and approximate 25th, 50th, and 75th percentile values for both "collateral" and "estimated seizable assets" within each sector using quartiles.
-- The results are ordered by the average collateral value in ascending order,
-- providing a comprehensive comparison of collateral and asset value distributions across different working sectors.
WITH ranked_collateral AS (
    SELECT
        "working sector",
        "collateral",
        NTILE(4) OVER (PARTITION BY "working sector" ORDER BY "collateral") AS collateral_quartile
    FROM customers_data_for_queries
),
ranked_assets AS (
    SELECT
        "working sector",
        "estimated seizable assets",
        NTILE(4) OVER (PARTITION BY "working sector" ORDER BY "estimated seizable assets") AS assets_quartile
    FROM customers_data_for_queries
)
SELECT
    c."working sector",
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
    ON c."working sector" = a."working sector"
GROUP BY c."working sector"
ORDER BY "average estimated seizable assets" ASC;

-- Query to analyze the distribution of unpaid past credits by working sector using percentiles
-- This query groups customers by their "working sector" and calculates:
--   - the number of customers in each sector,
--   - the average, maximum, and minimum "number of not paid past credits" for each sector,
--   - and approximate 25th, 50th, and 75th percentile values of "number of not paid past credits" within each sector using quartiles.
-- The results are ordered by the average number of not paid past credits in ascending order,
-- allowing comparison of credit repayment issues across different working sectors.
WITH ranked_data_3 AS (
    SELECT
        "working sector",
        "number of not paid past credits",
        NTILE(4) OVER (PARTITION BY "working sector" ORDER BY "number of not paid past credits") AS quartile
    FROM customers_data_for_queries
)
SELECT
    "working sector",
    COUNT(*) AS "number of customers",
    AVG("number of not paid past credits") AS "average number of not paid past credits",
    MAX("number of not paid past credits") AS "maximum number of not paid past credits",
    MIN("number of not paid past credits") AS "minimum number of not paid past credits",
    -- Get approximate 25th, 50th, 75th percentile values
    MAX(CASE WHEN quartile = 1 THEN "number of not paid past credits" END) AS "25th percentile approx",
    MAX(CASE WHEN quartile = 2 THEN "number of not paid past credits" END) AS "50th percentile approx",
    MAX(CASE WHEN quartile = 3 THEN "number of not paid past credits" END) AS "75th percentile approx"
FROM ranked_data_3
GROUP BY "working sector"
ORDER BY "average number of not paid past credits" ASC;

-- Query to analyze credit monthly amount and loan duration by working sector using percentiles
-- This query groups customers by their "working sector" and calculates:
--   - the number of customers in each sector,
--   - the average, maximum, and minimum "credit: monthly amount" for each sector,
--   - the average "requested_loan_duration" for each sector,
--   - and approximate 25th, 50th, and 75th percentile values of "credit: monthly amount" within each sector using quartiles.
-- The results are ordered by the average credit monthly amount in ascending order,
-- allowing comparison of credit and loan duration distribution across different working sectors.
WITH ranked_data_4 AS (
    SELECT
        "working sector",
        "credit: monthly amount",
        "requested_loan_duration",
        NTILE(4) OVER (PARTITION BY "working sector" ORDER BY "credit: monthly amouunt", "requested_loan_duration") AS quartile
    FROM customers_data_for_queries
)   
SELECT
    "working sector",
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
GROUP BY "working sector"
ORDER BY "credit: monthly amount" ASC;

-- Query to analzze the credit-to-income ratio by working sector using percentiles
-- This query groups customers by their "working sector" and calculates:
--   - the number of customers in each sector,
--   - the average, maximum, and minimum "credit-to-income ratio" for each sector,
--   - and approximate 25th, 50th, and 75th percentile values of "credit-to-income ratio" within each sector using quartiles.
-- The results are ordered by the average credit-to-income ratio in ascending order,
-- allowing comparison of credit burden relative to income across different working sectors.
WITH ranked_data_5 AS (
    SELECT
        "working sector",
        "credit-to-income ratio",
        NTILE(4) OVER (PARTITION BY "working sector" ORDER BY "credit-to-income ratio") AS quartile
    FROM customers_data_for_queries
)
SELECT
    "working sector",
    COUNT(*) AS "number of customers",
    AVG("credit-to-income ratio") AS "average credit-to-income ratio",
    MAX("credit-to-income ratio") AS "maximum credit-to-income ratio",
    MIN("credit-to-income ratio") AS "minimum credit-to-income ratio",
    -- Get approximate 25th, 50th, 75th percentile values
    MAX(CASE WHEN quartile = 1 THEN "credit-to-income ratio" END) AS "25th percentile approx",
    MAX(CASE WHEN quartile = 2 THEN "credit-to-income ratio" END) AS "50th percentile approx",
    MAX(CASE WHEN quartile = 3 THEN "credit-to-income ratio" END) AS "75th percentile approx"
FROM ranked_data_5
GROUP BY "working sector"
ORDER BY "average credit-to-income ratio" ASC;

-- Query to analyze and rank debt-to-income ratios before and after credit by working sector
-- This query groups customers by their "working sector" and calculates:
--   - the number of customers in each sector,
--   - the average, maximum, and minimum "debt-to-income ratio before credit" and "debt-to-income ratio after credit" for each sector,
--   - approximate 25th, 50th, and 75th percentile values for both ratios using quartiles,
--   - the rank of each sector by average debt-to-income ratio before credit,
--   - the rank of each sector by average debt-to-income ratio after credit,
--   - and the change in rank after credit (positive means the sector moved up, negative means it moved down).
-- The results are ordered by the before and after credit ranks.

WITH sector_averages AS (
    SELECT
        "working sector",
        COUNT(*) AS "number of customers",
        AVG("debt-to-income ratio before credit") AS "average debt-to-income ratio before credit",
        AVG("debt-to-income ratio after credit") AS "average debt-to-income ratio after credit"
    FROM customers_data_for_queries
    GROUP BY "working sector"
),
ranked_before AS (
    SELECT
        "working sector",
        "average debt-to-income ratio before credit",
        RANK() OVER (ORDER BY "average debt-to-income ratio before credit" ASC) AS "rank before credit"
    FROM sector_averages
),
ranked_after AS (
    SELECT
        "working sector",
        "average debt-to-income ratio after credit",
        RANK() OVER (ORDER BY "average debt-to-income ratio after credit" ASC) AS "rank after credit"
    FROM sector_averages
),
percentiles AS (
    SELECT
        "working sector",
        MAX(CASE WHEN quartile = 1 THEN "debt-to-income ratio before credit" END) AS "25th percentile approx before credit",
        MAX(CASE WHEN quartile = 2 THEN "debt-to-income ratio before credit" END) AS "50th percentile approx before credit",
        MAX(CASE WHEN quartile = 3 THEN "debt-to-income ratio before credit" END) AS "75th percentile approx before credit",
        MAX(CASE WHEN quartile = 1 THEN "debt-to-income ratio after credit" END) AS "25th percentile approx after credit",
        MAX(CASE WHEN quartile = 2 THEN "debt-to-income ratio after credit" END) AS "50th percentile approx after credit",
        MAX(CASE WHEN quartile = 3 THEN "debt-to-income ratio after credit" END) AS "75th percentile approx after credit"
    FROM (
        SELECT
            "working sector",
            "debt-to-income ratio before credit",
            "debt-to-income ratio after credit",
            NTILE(4) OVER (PARTITION BY "working sector" ORDER BY "debt-to-income ratio before credit") AS quartile
        FROM customers_data_for_queries
    ) q
    GROUP BY "working sector"
)
SELECT
    sa."working sector",
    sa."number of customers",
    sa."average debt-to-income ratio before credit",
    rb."rank before credit",
    sa."average debt-to-income ratio after credit",
    ra."rank after credit",
    (rb."rank before credit" - ra."rank after credit") AS "rank change after credit",
    -- Percentiles for before and after credit
    p."25th percentile approx before credit",
    p."25th percentile approx after credit",
    p."50th percentile approx before credit",
    p."50th percentile approx after credit",
    p."75th percentile approx before credit",
    p."75th percentile approx after credit"
FROM sector_averages sa
JOIN ranked_before rb ON sa."working sector" = rb."working sector"
JOIN ranked_after ra ON sa."working sector" = ra."working sector"
JOIN percentiles p ON sa."working sector" = p."working sector"
ORDER BY rb."rank before credit" ASC, ra."rank after credit" ASC;





