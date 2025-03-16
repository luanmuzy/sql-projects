USE gamessales;

SELECT * FROM report LIMIT 15;

SELECT 
    month,
    Branch,
    quant,
    total,
    ROUND((total / quant),2) AS ticket 
FROM (
    SELECT 
        MONTH(report.Date) AS month, 
        Branch, 
        SUM(Quantity) AS quant, 
        ROUND(SUM(Total),2) AS total
    FROM report
    GROUP BY month, Branch
    ORDER BY month asc
) AS subquery;


SELECT 
    CASE MONTH(report.Date)
        WHEN 1 THEN 'January'
        WHEN 2 THEN 'February'
        WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'
        WHEN 5 THEN 'May'
        WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'
        WHEN 8 THEN 'August'
        WHEN 9 THEN 'September'
        WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'
        WHEN 12 THEN 'December'
    END AS month, 
    City, 
    Branch,
    ROUND(SUM(Total), 2) AS total,
    MONTH(report.Date) AS month_number
FROM report
GROUP BY month ,Branch, City, month_number
ORDER BY month_number asc, total desc;

-- Existe uma correlação entre a localização e o tipo de cliente (Customer type) que mais compra?
SELECT * FROM report LIMIT 15;

SELECT City, 
	cus, 
	total_cus
FROM (
	SELECT City, 
	`Customer Type` as cus, 
    COUNT(`Customer Type`) as total_cus
    FROM report
	GROUP BY City, cus
    ORDER BY City

) AS tot;

SELECT * FROM report LIMIT 15;

--  produtos (Product line) mais vendidas a cada mês
SELECT MONTH(report.Date) as month1, 
`Product line` as prod, 
COUNT(`Product line`) as prod_count
FROM report
GROUP BY month1, `Product line`
ORDER BY month1, prod_count desc;

-- Qual é o perfil dos clientes (Customer type e Gender) que mais compram ao longo dos meses?
SELECT * FROM report LIMIT 15;

SELECT MONTH(report.Date) as month, 
	`Customer type` as cust,
    COUNT(`Customer type`) as cust_total,
    `Gender` as  gender,
    COUNT( `Gender`) as  gender_total
FROM report
GROUP BY month, cust,  gender
ORDER BY month asc, cust_total desc;



-- Qual é o item com o maior número de vendas totais?

SELECT `Product line` as prod,
COUNT(Quantity) as quan,
ROUND(SUM(Total),2) as total
FROM report
GROUP BY prod
ORDER BY total desc;

-- Análise de Comportamento de Compra e Pagamento

-- Quais métodos de pagamento (Payment) são mais utilizados a cada mês?
-- 		Analisa a preferência dos clientes por métodos de pagamento.
SELECT * FROM report LIMIT 15;
SELECT MONTH(report.Date) as month, Payment as pay, COUNT(Payment) as con
FROM report
GROUP BY month, pay
ORDER BY month asc, con desc;

-- Qual é o horário (Time) com mais vendas ao longo dos meses?
-- 		Ajuda a identificar picos de vendas durante o dia.

SELECT MONTH(report.Date) as month, 
report.Time as time,
COUNT(report.Time) as time_cont
FROM report
GROUP BY month, time
ORDER BY month asc, time_cont desc;

WITH MonthlyTopTime AS (
    SELECT 
        MONTH(report.Date) AS month, 
        report.Time AS time,
        COUNT(report.Time) AS time_cont,
        ROW_NUMBER() OVER (PARTITION BY MONTH(report.Date) ORDER BY COUNT(report.Time) DESC) AS rn
    FROM report
    GROUP BY month, time
)

SELECT month, time, time_cont
FROM MonthlyTopTime
WHERE rn = 1
ORDER BY month ASC;

-- Qual é a relação entre Rating (avaliação) e volume de vendas?
-- 		Analisa se produtos com melhor avaliação estão associados a vendas mais altas



-- Análise Financeira

-- Qual é a margem de lucro bruta mensalmente?
-- 		Calcula a margem com base nas colunas cogs e gross income para entender a lucratividade.


-- Como os impostos (Tax 5%) impactam o lucro bruto em cada mês?
-- 		Avalia o efeito dos impostos sobre o lucro ao longo dos meses.


-- Qual foi a evolução das despesas (Total) em relação ao lucro bruto ao longo dos meses?
-- 		Analisa o balanço entre despesas e lucro para avaliar a sustentabilidade financeira


