import pandas as pd
import mysql.connector
import os
import plotly.express as px 
import plotly.graph_objects as go
import decimal
import dotenv as en


#################### Location and Branch Analysiss ####################
en.load_dotenv()
passw = os.getenv("PASS")

# What is the sales performance by branch and city each month?
def sales_performance():
    command = """SELECT 
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

    """

    mysql_config = {
        'host': 'localhost', 
        'user': 'root',
        'password': passw,
        'database': 'gamessales'
        }

    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute("USE gamessales;")

    df = pd.read_sql_query(command, conn)

    months = df["month"]
    citys = df["City"]
    branchs = df["Branch"]
    total = df["total"]


    conn.close()

    fig = px.histogram(df, x=months, y=total, color=citys, facet_col=citys)
    fig.update_traces(texttemplate='TOTAL: $%{y}', textposition='inside', insidetextanchor='middle')

    image_path = f'reports/location_and_branch/report_image1.png'
    fig.write_image(image_path, width=1200, height=700)


    def cityMonth():
    
        monthly_sales_by_city = df.groupby(['month', 'City'])['total'].sum().reset_index()

        
        monthly_sales_by_city = monthly_sales_by_city.sort_values(['month', 'total'], ascending=[False, False]).reset_index()
        top_city_per_month = monthly_sales_by_city.groupby('month').head(1)

        month_order = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

        
        top_city_per_month['month_num'] = top_city_per_month['month'].map(month_order)
    
        top_city_per_month = top_city_per_month.sort_values(by='month_num').drop(columns=['month_num']).reset_index(drop=True)


        fig_top_city = px.histogram(top_city_per_month, x="month", y="total", color="City")
        fig_top_city.update_traces(texttemplate='TOTAL: $%{y}', textposition='inside', insidetextanchor='middle')

        image_path = f'reports/location_and_branch/report_image2.png'
        fig_top_city.write_image(image_path, width=1200, height=700)

    def branchMonth():
    
        monthly_sales_by_branch = df.groupby(['month', 'Branch'])['total'].sum().reset_index()

        
        monthly_sales_by_city = monthly_sales_by_branch.sort_values(['month', 'total'], ascending=[False, False]).reset_index()

    
        top_branch_per_city = monthly_sales_by_city.groupby('month').head(1)
        month_order = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

        top_branch_per_city['month_num'] = top_branch_per_city['month'].map(month_order)

        top_branch_per_city = top_branch_per_city.sort_values(by='month_num').drop(columns=['month_num']).reset_index(drop=True)


        fig_top_city = px.histogram(top_branch_per_city, x="month", y="total", color="Branch")
        fig_top_city.update_traces(texttemplate='TOTAL: $%{y}', textposition='inside', insidetextanchor='middle')

        image_path = f'reports/location_and_branch/report_image3.png'
        fig_top_city.write_image(image_path, width=1200, height=700)

    cityMonth()
    branchMonth()

# Which branches have the highest average ticket size?
def branch_ticket():
    command = """SELECT 
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

    """

    mysql_config = {
        'host': 'localhost', 
        'user': 'root',
        'password': passw,
        'database': 'gamessales'
        }

    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute("USE gamessales;")

    df = pd.read_sql_query(command, conn)

    month_ticket = df.groupby(['month', 'Branch'])['ticket'].sum().reset_index()
    month_ticket = month_ticket.sort_values(['month', 'ticket'], ascending=[True, False]).reset_index()
    month_ticket = month_ticket.groupby('month').head(1)


    conn.close()
    t = month_ticket['ticket']
    fig = px.bar(month_ticket, x='month', y="ticket", color="Branch")
    fig.update_traces(text=t,  texttemplate='TOTAL: $%{text}', textposition='inside', insidetextanchor='middle')

    image_path = f'reports/location_and_branch/report_image4.png'
    fig.write_image(image_path, width=1200, height=700)

# Is there a correlation between location and customer type that purchases the most?
def location_and_customer():
    command = """SELECT City, 
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

    """

    mysql_config = {
        'host': 'localhost', 
        'user': 'root',
        'password': passw,
        'database': 'gamessales'
        }

    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute("USE gamessales;")

    df = pd.read_sql_query(command, conn)

   
   
    location_x_customer = df.groupby(["City", "cus"]).sum().reset_index()
    location_x_customer = location_x_customer.sort_values("total_cus", ascending=False).reset_index()
    location_x_customer  = location_x_customer .groupby(["City"]).head(1)
    
    conn.close()
    location_x_customer['text'] = location_x_customer.apply(lambda row: f"{row['total_cus']} {row['cus']} customers", axis=1)
    
    tex = location_x_customer["text"].tolist()
    title_text = f"Correlation between location and customer type that purchases the most \n {'\n'.join(tex)}"
    
    fig = px.bar(location_x_customer, x='City', y="total_cus", color="cus",
                labels={"total_cus": "Total"},
                title="Test", #title_text,
                text="text"
                )
    
    fig.update_traces(texttemplate='%{text}', textposition='inside', insidetextanchor='middle')

    image_path = f'reports/location_and_branch/report_image5.png'
    fig.write_image(image_path, width=1200, height=700)






sales_performance()
branch_ticket()
location_and_customer()

print("Finish")
