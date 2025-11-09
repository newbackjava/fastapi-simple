CREATE TABLE daily_sales_metrics (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  sale_date  DATE        NOT NULL,
  orders     INT         NOT NULL,
  revenue    DECIMAL(12,2) NOT NULL,
  customers  INT         NOT NULL
);

delete from daily_sales_metrics;

INSERT INTO daily_sales_metrics (sale_date, orders, revenue, customers) VALUES
('2025-10-20', 40, 520000.00, 35),
('2025-10-21', 44, 575000.00, 39),
('2025-10-22', 38, 500000.00, 33),
('2025-10-23', 47, 615000.00, 41),
('2025-10-24', 52, 680000.00, 39),
('2025-10-25', 60, 820000.00, 35),
('2025-10-26', 58, 790000.00, 48),
('2025-10-27', 43, 560000.00, 37),
('2025-10-28', 45, 590000.00, 35),
('2025-10-29', 49, 640000.00, 39),
('2025-10-30', 55, 720000.00, 47),
('2025-10-31', 62, 880000.00, 35),
('2025-11-01', 57, 760000.00, 49),
('2025-11-02', 63, 900000.00, 39),
('2025-11-03', 50, 680000.00, 35),
('2025-11-04', 48, 650000.00, 42),
('2025-11-05', 52, 700000.00, 46),
('2025-11-06', 54, 730000.00, 47),
('2025-11-07', 59, 820000.00, 39),
('2025-11-08', 61, 860000.00, 39);

SELECT sale_date, revenue, orders
FROM daily_sales_metrics
ORDER BY sale_date;

select * from daily_sales_metrics;

select count(*) from daily_sales_metrics;

SELECT customers, avg(orders)
FROM daily_sales_metrics
group by customers;

select count(distinct customers) from daily_sales_metrics;
select count(*) from daily_sales_metrics where customers = 35;

-- char_db.py

SELECT count(distinct customers) as count
FROM daily_sales_metrics;


SELECT customers, avg(orders) as avg
FROM daily_sales_metrics
group by customers
ORDER BY avg(orders) DESC;


SELECT revenue, customers
FROM daily_sales_metrics
order by revenue desc
limit 3;

			