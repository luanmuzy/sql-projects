import pandas as pd
import mysql.connector
import os
import plotly.express as px 
import decimal
import dotenv as en

#################### Sales and Revenue Analysis ####################

csv_path = "database/supermarket_sales.csv"
en.load_dotenv()
passw = os.getenv("PASS")

def edit_file(csvPath, fileName):         
       
    df = pd.read_csv(csvPath, encoding='latin1')
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].apply(lambda x: x.date())
    except:
        pass
    df.dropna()
    path = f"database/{fileName}.csv"

    if not os.path.exists(path):
        df.to_csv(path, if_exists="replace", index=False)

        print("File edit successfully!")
        return path
    else:
        return path

editFile = edit_file(csv_path,"editDB")

# What is the total monthly sales?
def total_monthly_sales():
    mysql_config = {
    'host': 'localhost', 
    'user': 'root',
    'password': passw,
    'database': 'gamessales'
    }

    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute("USE gamessales;")


    command = '''SELECT MONTH(report.Date) AS month, SUM(Quantity) AS total_quantity
                FROM report
                GROUP BY month
                ORDER BY month desc;
                '''
    
    #c.execute(command)
    df = pd.read_sql_query(command, conn)
    month_mapping = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    
   
    df['month'] = df['month'].map(month_mapping)

    df_sorted = df.sort_values(by="total_quantity", ascending=True)
  
    fig = px.bar(df_sorted, x='total_quantity', y='month', orientation='h', color="total_quantity",
                 labels={'month': 'Month', 'total_quantity': 'Total Quantity'},
                 title='Total Monthly Sales')

    
    fig.update_traces(text=df_sorted['total_quantity'], textposition='inside', insidetextanchor='middle')
   
    conn.close()
    image_path = f'reports/Sales_and_Revenue/report_image1.png'
    fig.write_image(image_path, width=1200, height=700)    
    
# What is the average sales amount per month?
def month_average_sales():
    mysql_config = {
    'host': 'localhost', 
    'user': 'root',
    'password': passw,
    'database': 'gamessales'
    }

    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute("USE gamessales;")

    command = '''SELECT MONTH(report.Date) as month, AVG(Quantity) AS month_avg
                FROM report
                GROUP BY month
                ORDER BY month desc;
    '''
    df = pd.read_sql_query(command, conn)

    month_mapping = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    df["month"] = df["month"].map(month_mapping)
    df_sorted = df.sort_values(by="month_avg", ascending=True)
    

    fig = px.bar(df_sorted, x="month", y="month_avg", color="month_avg",
                 labels={"month": "Month", "month_avg": "AVG" },
                 title="Month AVG")
    
    fig.update_traces(text=df_sorted['month_avg'], textposition='inside', insidetextanchor='middle')

    conn.close()
    #fig.show()
    image_path = f'reports/Sales_and_Revenue/report_image2.png'
    fig.write_image(image_path, width=1200, height=700)    

# Which months have the highest and lowest sales?
def months_highest_and_lowest():
    mysql_config = {
    'host': 'localhost', 
    'user': 'root',
    'password': passw,
    'database': 'gamessales'
    }

    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute("USE gamessales;")

    highest = '''SELECT MONTH(report.Date) AS month, SUM(Quantity) AS total_quantity
                FROM report
                GROUP BY month
                ORDER BY SUM(Quantity) desc
                LIMIT 1;
    '''
    lowest = '''SELECT MONTH(report.Date) AS month, SUM(Quantity) AS total_quantity
                FROM report
                GROUP BY month
                ORDER BY SUM(Quantity) asc
                LIMIT 1;
    '''
    month_mapping = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    df_highest = pd.read_sql_query(highest, conn)
    df_lowest = pd.read_sql_query(lowest, conn)

    df_highest['month'] = df_highest['month'].map(month_mapping)
    df_lowest['month'] = df_lowest['month'].map(month_mapping)

    df_combined = pd.concat([df_highest, df_lowest], ignore_index=True)

    fig = px.bar(df_combined, x="month", y="total_quantity", color="total_quantity",
                 labels={"month": "Month", "total_quantity": "Total Quantity" },
                 title="Highest and Lowest Sales Months")
    
    fig.update_traces(text=df_combined['total_quantity'], textposition='inside', insidetextanchor='middle')

    conn.close()

    image_path = f'reports/Sales_and_Revenue/report_image3.png'
    fig.write_image(image_path, width=1200, height=700)    
    
    
    conn.close()

# What is the total tax expense (Tax 5%) over the months?
def total_tax_expense():
    mysql_config = {
    'host': 'localhost', 
    'user': 'root',
    'password': passw,
    'database': 'gamessales'
    }

    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute("USE gamessales;")

    command = '''SELECT 
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
    ROUND(SUM(`Tax 5%`), 2) AS tax
FROM report
GROUP BY month
ORDER BY tax desc;

'''

    df_tax= pd.read_sql_query(command, conn)

    fig = px.bar(df_tax, x="month", y="tax", color="tax",
                 labels={"month": "Month", "tax": "Total Tax 5%" },
                 title="Total Tax Expense")
    
    fig.update_traces(text=df_tax['tax'], texttemplate='$%{text}', textposition='inside', insidetextanchor='middle')

    conn.close()

    image_path = f'reports/Sales_and_Revenue/report_image4.png'
    fig.write_image(image_path, width=1200, height=700)    
    
    
    conn.close()

# What is the gross profit per month?
def gross_profit():
    mysql_config = {
    'host': 'localhost', 
    'user': 'root',
    'password': passw,
    'database': 'gamessales'
    }

    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute("USE gamessales;")

    command = '''SELECT 
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
            ROUND(SUM(Total), 2) AS total,
            ROUND(SUM(cogs), 2) AS total_cogs,
            ROUND(SUM(`gross income`), 2) AS total_gross_income
        FROM report
        GROUP BY month
        ORDER BY month;
        '''

    df_profit= pd.read_sql_query(command, conn)

    total_gross = df_profit['total_gross_income']
    df_total = df_profit['total']
    total_cogs = df_profit['total_cogs']
   
    fig = px.bar(df_profit, x='month', y='total_gross_income', color='total_gross_income',                 
                labels={"month": "Month", "total_gross_income": "Total Gross Income"},
                title=f"Monthly Totals, COGS, and Gross Income")

    
    fig.update_traces(text=total_gross, texttemplate='Gross Income: $%{text}', textposition='inside', insidetextanchor='middle')
    

    fig.update_layout(
    title={
        'text': "Monthly Totals, COGS, and Gross Income",
        'y':0.95,  
        'x':0.5,   
        'xanchor': 'center',
        'yanchor': 'top'
    },
    annotations=[
        dict(
            x=0.4,
            y=1.05,
            showarrow=False,
            text=f"Total: ${df_total.sum()}",
            xref="paper",
            yref="paper",
            font=dict(size=16, color="black")
        ),
        dict(
            x=0.8,
            y=1.05,
            showarrow=False,
            text=f"Total Cogs: ${total_cogs.sum()}<br>",
            xref="paper",
            yref="paper",
            font=dict(size=16, color="black")
        )
    ]
)
    conn.close()

    image_path = f'reports/Sales_and_Revenue/report_image5.png'
    fig.write_image(image_path, width=1200, height=700)    

total_monthly_sales()
month_average_sales()
months_highest_and_lowest()
total_tax_expense()
gross_profit()
