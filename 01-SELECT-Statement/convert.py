import csv
import sqlite3

def csv_para_db(csv_file, db_file, tabela_nome):
    # Conectar ao banco de dados (será criado se não existir)
    conexao = sqlite3.connect(db_file)
    cursor = conexao.cursor()
    
    # Ler o arquivo CSV
    with open(csv_file, 'r', encoding='utf-8') as arquivo:
        leitor_csv = csv.reader(arquivo)
        cabecalho = next(leitor_csv)  # Lê a primeira linha como cabeçalho
        
        # Criar tabela no banco de dados
        colunas = ', '.join([f'"{col}" TEXT' for col in cabecalho])
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {tabela_nome} ({colunas})')
        
        # Inserir dados
        marcadores = ', '.join(['?'] * len(cabecalho))
        for linha in leitor_csv:
            cursor.execute(f'INSERT INTO {tabela_nome} VALUES ({marcadores})', linha)
    
    # Salvar alterações e fechar conexão
    conexao.commit()
    conexao.close()

# Uso do código
csv_para_db(
    csv_file = './db/Walmart_Sales.csv',
    db_file = './db/Walmart_Sales.db',
    tabela_nome = 'sales'
)