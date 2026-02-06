-- Location-wise profit
SELECT
    txn_date,
    STORE_LOCATION,
    ROUND(SUM(SP) - SUM(CP), 2) AS lc_profit
FROM clean_store_transactions
WHERE txn_date = '2019-11-26'
GROUP BY STORE_LOCATION, txn_date
ORDER BY lc_profit DESC
INTO OUTFILE '/store_files/location_wise_profit.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

-- Store-wise profit
SELECT
    txn_date,
    STORE_ID,
    ROUND(SUM(SP) - SUM(CP), 2) AS st_profit
FROM clean_store_transactions
WHERE txn_date = '2019-11-26'
GROUP BY STORE_ID, txn_date
ORDER BY st_profit DESC
INTO OUTFILE '/store_files/store_wise_profit.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';
