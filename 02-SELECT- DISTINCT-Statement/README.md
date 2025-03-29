# Usando o comando `DISTINCT` para retornar dados.

## Listar todos os paises únicos.

```sql
SELECT DISTINCT Country FROM COVID_Data LIMIT 15;
```
|Country|
|-------|
|Afghanistan|
|Albania|
|Algeria|
|Andorra|
|Angola|
|Antigua and Barbuda|
|Argentina|
|Armenia|
|Australia|
|Austria|
|Azerbaijan|
|Bahamas|
|Bahrain|
|Bangladesh|
|Barbados|
---

## Encontrar paises e o tipo de lockdown únicos.

```sql
SELECT DISTINCT Country, Lockdown_Type FROM COVID_Data LIMIT 15;
```

|Country|Lockdown_Type|
|-------|-------------|
|Afghanistan|Full|
|Albania|Full|
|Algeria|Full|
|Andorra|Full|
|Angola||
|Antigua and Barbuda||
|Argentina|Full|
|Armenia|Full|
|Australia|Partial|
|Austria|Full|
|Azerbaijan|Full|
|Bahamas|Full|
|Bahrain|Full|
|Bangladesh|Full|
|Barbados|Full|
---

## Contar quantos paises únicos existem.
```sql
SELECT DISTINCT COUNT(Country) AS count_country FROM COVID_Data; 
```
|count_country|
|-------------|
|173|

---

## Combinar SELECT DISTINCT com ORDER BY para listar numeros de casos e mortes por pais.
```sql
SELECT DISTINCT Country, Population_Size, Cases, Deaths 
FROM COVID_Data
ORDER BY Deaths DESC, Cases LIMIT 15;
```

|Country|Population_Size|Cases|Deaths|
|-------|---------------|-----|------|
|US|326687501|77707349|919255|
|Brazil|209469333|27434286|638346|
|India|1352617328|42631421|508665|
|Russia|144478050|13728138|332727|
|Mexico|126190788|5283852|312697|
|Peru|31989256|3435753|208120|
|United Kingdom|66460344|18266015|159518|
|Italy|60421760|12053330|150824|
|Indonesia|267663435|4708043|144958|
|Colombia|49648685|6014563|136953|
|Iran|81800269|6780453|133570|
|France|66977107|21075675|131833|
|Argentina|44494502|8728262|123987|
|Germany|82905782|12391463|119939|
|Ukraine|44622516|4708604|109483|
