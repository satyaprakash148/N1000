-- 1. Total companies
SELECT COUNT(*) 
FROM companies;


-- 2. Year coverage
SELECT 
company_id,
COUNT(DISTINCT year)
FROM profitandloss
GROUP BY company_id;


-- 3. Highest sales companies
SELECT 
company_id,
MAX(sales)
FROM profitandloss
GROUP BY company_id;


-- 4. Highest ROE companies
SELECT 
company_id,
MAX(roe)
FROM financial_ratios
GROUP BY company_id;


-- 5. Negative cashflow companies
SELECT *
FROM cashflow
WHERE net_cash < 0;


-- 6. Average PE ratio
SELECT AVG(pe_ratio)
FROM financial_ratios;


-- 7. Stock price range
SELECT 
MAX(close_price),
MIN(close_price)
FROM stock_prices;


-- 8. Companies with less than 5 years
SELECT
company_id,
COUNT(year)
FROM profitandloss
GROUP BY company_id
HAVING COUNT(year)<5;


-- 9. Revenue growth
SELECT
company_id,
year,
sales
FROM profitandloss
ORDER BY company_id,year;


-- 10. Company sectors
SELECT
company_name,
sector
FROM companies;