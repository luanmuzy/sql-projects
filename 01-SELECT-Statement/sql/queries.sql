-- Selecionar todas as colunas da tabela principal.
select * from salaries;

-- Listar apenas valores únicos de uma coluna específica.
SELECT DISTINCT JobTitle FROM salaries;

-- Ordenar os resultados por uma coluna numérica, tanto de forma crescente quanto decrescente.
SELECT EmployeeName, TotalPay   FROM salaries	
ORDER BY ROUND(TotalPay,2) DESC;

SELECT EmployeeName, TotalPay   FROM salaries	
ORDER BY ROUND(TotalPay,2) ASC;

-- Filtrar os dados usando a cláusula WHERE com diferentes condições.
SELECT JobTitle, TotalPay FROM salaries 
WHERE TotalPay >= 300000
ORDER BY TotalPay DESC;

-- Limitar os resultados para exibir apenas um número específico de registros.
SELECT JobTitle, TotalPay FROM salaries 
WHERE TotalPay >= 300000
ORDER BY TotalPay DESC
LIMIT 10;




