/*
    This file contains SQL queries to analyze the customers data.
    The queries are designed to extract insights from the data and are grouped by their purpose.
    Each query is preceded by a comment explaining its purpose.
*/

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

-- Query to analyze customer income by age group
-- This query groups customers by their "age" and calculates:
--   - the number of customers in each age group,
--   - the average monthly income
SELECT "age", 
        COUNT("age") AS "number of customers",
        AVG("monthly income") AS "average monthly income"
FROM customers_data_for_queries
GROUP BY "age"
ORDER BY "age" ASC;
 
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
ORDER BY "average monthly savings" ASC;