import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta 
import plotly.express as px 
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.drawing.image import Image

db_path = "database/retrun.db"
excel_path = "database/retrun.xlsx"




if not os.path.exists(db_path):
    df = pd.read_excel(excel_path, sheet_name="Retorno SVC São Carlos ")
    df = df[["DATA (OBRIGATORIO)", "ID", "MOTIVO","Devolvido", "Status Deixado ", "Contador", "Status", "Rota",  "Transportadora"]]
    cols = ["MOTIVO", "Devolvido", "Status Deixado ", "Status", "Rota", "Transportadora"]

    df[cols] = df[cols].apply(lambda col: col.str.upper() if col.dtype == 'object' else col)
    df.loc[df["Rota"] == "-", "Rota"] = "ROTA BRANCA"

    
    
    
    df = df.dropna()
    df["MOTIVO"] = df["MOTIVO"].apply(lambda x: x.split("|")[0])

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    df.to_sql("returns", conn, if_exists="replace", index=False)

    conn.close()

# Função para validar a data
def validar_data(date_str):
    try:
        # Tenta converter a string para um objeto datetime
        date = datetime.strptime(date_str, "%d/%m/%Y")
        date = date.strftime("%Y-%m-%d")
        return date
        
    except ValueError:
       
        return print("Invalid date! Please enter in DD/MM/YYYY format.")

#input_date = input("Date (DD/MM/YYYY): ")

#date_convert = validar_data(input_date)

def analyzes(date):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    command = f'''
    SELECT MOTIVO, COUNT(*) as cat_count
    FROM returns
    WHERE DATE("DATA (OBRIGATORIO)") = '{date}'
    GROUP BY MOTIVO
    ORDER BY cat_count DESC 
    '''

    c.execute(command)

    rows = c.fetchall()

    motivos = [row[0] for row in rows]
    contagens = [row[1] for row in rows]              
       

    newDate = datetime.strptime(date, "%Y-%m-%d")        
    newDate = newDate.strftime("%d.%m.%Y")
    

    output_file = f'graphics_motivos_{newDate}.xlsx'

    try:
        workbook = openpyxl.load_workbook(output_file)
    except FileNotFoundError:
        workbook = openpyxl.Workbook()

    
    worksheet = workbook.active
    worksheet.title = "Report"

    worksheet.append(["Motivo", "Quantidade"])
    for motivo, contagem in zip(motivos, contagens):
        worksheet.append([motivo, contagem])
    try: 
        fig = px.funnel(x=motivos, y=contagens,  color=contagens,
                    labels={'x': 'Motivo', 'y': 'Contagem'},
                    title=f'Motivos de Retorno para a Data {newDate}',
                    text=contagens
                    )
    
        image_path = f'graphics/images/report image- {newDate}.png'
        # Atualizar o layout do gráfico
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig.write_html(f'graphics/graphic/Report graphic - {newDate}.html')       
        fig.write_image(image_path, width=1200, height=700)       
       
        img = Image(image_path)
        worksheet.add_image(img, 'D1')  # Inserir a imagem na célula A1
     
        workbook.save(output_file)
        print(f"Arquivo Excel '{output_file}' criado com sucesso!")     
    except ValueError as e:
        print("Empy date!")
        print(e)
    
    conn.close()
    
    #fig.show()


today = datetime.today() - timedelta(days=60)
today = today.strftime("%Y-%m-%d") 

print(today)
#analyzes(date_convert)
analyzes(today)
