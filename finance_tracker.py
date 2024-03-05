from flask import Flask, render_template, request, url_for, flash, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
from password_management import create_db_connection, execute_query_data_retreieving
app=Flask(__name__)
app.secret_key = "My Secret key"

@app.route('/',methods=('GET', 'POST'))
def log_in():
    if request.method=='POST':
        Username=request.form['username_entered']
        Password=request.form['password_entered']
        see_stats_table = """
SELECT * FROM passwords;
"""
        connection=create_db_connection("localhost", "root", app.secret_key,'passwordmanagement')
        results=execute_query_data_retreieving(connection,see_stats_table)
        print(results)
        columns=['user_id','username','password']
        from_db=[]
        for result in results:
            result = list(result)
            from_db.append(result)
        df = pd.DataFrame(from_db, columns=columns)
        print(df.head())
        if Username in df.values and Password in df.values:
            return redirect(url_for('spending_display'))
        else:
            flash('Username or Password entered is wrong.')
    return render_template('login_page.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/password_creation',methods=('GET', 'POST'))
def password_creation():
    if request.method=='POST':
        Username_created=request.form['username_created']
        Password_created=request.form['password_created']
        if not Username_created:
            flash('Username is required!')
        elif not Password_created:
            flash('Work is required!')
        else:
            connection=create_db_connection("localhost", "root",app.secret_key,'passwordmanagement')
            count_query=""" SELECT COUNT(*) FROM passwords"""
            existing_count=execute_query_data_retreieving(connection,count_query)
            the_number=0
            for number in existing_count:
                the_number=the_number+int(number[0])        
            user_id= the_number+1
            add_info="""INSERT INTO passwords VALUES
            (%s, %s, %s)"""
            cursor=connection.cursor()
            cursor.execute(add_info,(user_id,Username_created,Password_created))
            connection.commit()
            flash('Account has been succesfully created.')
            return redirect(url_for('home'))
    return render_template('password_creation.html')

@app.route('/spending_display')
def spending_display():
    from_db = []
    columns = ['id',"types",'specific_type','value']
    connection = create_db_connection("localhost", "root", app.secret_key,'passwordmanagement')
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
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('spending_display.html',graphJSON=graphJSON)

@app.route('/transactions_entry',methods=('GET', 'POST'))
def spending_entry():
    if request.method=="POST":
        types=request.form['type of financial activity']
        specific_type=request.form['specific']
        amount=request.form['value']
        if types=='Expenditure':
            amount=-int(amount)
            connection=create_db_connection("localhost", "root", app.secret_key,'passwordmanagement')
            add_info="""INSERT INTO transaction(type,specifictypes,value) VALUES(%s, %s, %s)"""
            cursor=connection.cursor()
            cursor.execute(add_info,(types,specific_type,amount))
            connection.commit()
            flash("Financial Transaction has been successfully entered.")
            return redirect(url_for('spending_display'))
        else:
             connection=create_db_connection("localhost", "root", app.secret_key,'passwordmanagement')
             add_info="""INSERT INTO assets(specifictypes,value) VALUES(%s, %s)"""
             cursor=connection.cursor()
             cursor.execute(add_info,(specific_type,amount))
             connection.commit()
             flash("Financial Transaction has been successfully entered.")
             return redirect(url_for('wealth_display'))

    return render_template('spending_entry.html')

@app.route('/wealth_display')
def wealth_display():
    from_db = []
    columns = ['id','specific_type','value']
    connection = create_db_connection("localhost", "root", app.secret_key,'passwordmanagement')
    see_stats_table = """
    SELECT * FROM assets;
    """
    results=execute_query_data_retreieving(connection,see_stats_table)
    for result in results:
        result = list(result)
        from_db.append(result)
    df = pd.DataFrame(from_db, columns=columns)
    df['value']=df['value'].astype('int').abs()
    fig = px.pie(df, values='value', names='specific_type',title="Breakdown of assets",color_discrete_sequence=px.colors.sequential.RdBu)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('wealth_display.html',graphJSON=graphJSON)

@app.route('/wealth_input')
def wealth_input():
    return render_template('wealth_input.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

if __name__ == "__main__":
    app.run(debug=True)