SELECT "working sector", AVG("monthly income") 
FROM customers_data_for_queries
GROUP BY "working sector"
ORDER BY AVG("monthly income") DESC;-- Write your own SQL object definition here, and it'll be included in your package.
