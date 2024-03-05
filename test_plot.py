from flask import Flask, render_template, request, url_for, flash, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
secret_key = "My Secret key"
from password_management import create_db_connection, execute_query_data_retreieving
from_db = []
columns = ['id',"types",'specific_type','value']
connection = create_db_connection("localhost", "root",secret_key,'passwordmanagement')
see_stats_table = """
SELECT * FROM transaction;
"""
results=execute_query_data_retreieving(connection,see_stats_table)
for result in results:
    result = list(result)
    from_db.append(result)
df = pd.DataFrame(from_db, columns=columns)
df['value']=df['value'].astype('int').abs()
fig = px.pie(df, values='value', names='specific_type',title="Breakdown of Spending",color_discrete_sequence=px.colors.sequential.RdBu)
fig.show()