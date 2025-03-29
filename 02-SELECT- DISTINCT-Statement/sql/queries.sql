-- Listar todos os valores únicos de uma coluna categórica (exemplo: categorias de produtos, departamentos, países).
SELECT DISTINCT Country FROM COVID_Data LIMIT 15;
-- Encontrar paises e o tipo de lockdown únicos.
SELECT DISTINCT Country, Lockdown_Type FROM COVID_Data LIMIT 15;
-- Contar quantos paises únicos existem.
SELECT DISTINCT COUNT(Country) AS count_country FROM COVID_Data; 
-- Combinar SELECT DISTINCT com ORDER BY para listar numeros de casos e mortes por pais.
SELECT DISTINCT Country, Population_Size, Cases, Deaths 
FROM COVID_Data
ORDER BY Deaths DESC, Cases LIMIT 15;


