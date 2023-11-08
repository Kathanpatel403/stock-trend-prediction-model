import base64
from io import BytesIO
from flask import Flask, url_for, render_template, request, Response
from yahoo_fin.stock_info import get_data
import matplotlib.pyplot as plt
import math, datetime
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    company = request.form['company']
    start_date = request.form['start']
    end_date = request.form['end']
    
    df = get_data(company, start_date=start_date, end_date=end_date, index_as_date = True, interval="1d")

    # Perform stock trend prediction using your machine learning model
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df['hl_pct'] = (df['high'] - df['close']) / df['close'] * 100
    df['pct_change'] = (df['close'] - df['open']) / df['open'] * 100
    df = df[['close', 'hl_pct', 'pct_change', 'volume']]
    new_df = df.describe()
    

    forcast_col = 'close'
    df.fillna(-99999, inplace=True)
    forcast_out = int(math.ceil(0.015*len(df)))
    df['label'] = df[forcast_col].shift(-forcast_out) 


    # Splliting data into features and labels: 
    X = np.array(df.drop(['label'], axis=1))
    X = preprocessing.scale(X)
    X = X[:-forcast_out]
    X_lately = X[-forcast_out:]
    df.dropna(inplace=True)
    y = np.array(df['label'])
    df.dropna(inplace=True)

    # Splliting data into training and testing part: 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Training model: 
    model = LinearRegression(n_jobs=-1)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    # Making predictions: 
    forcast_set = model.predict(X_lately)

    df['Forecast'] = np.nan

    last_date = df.iloc[-1].name
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day 

    for i in forcast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

    # Plotting data: 
    df['close'].plot()
    df['Forecast'].plot()
    plt.legend(loc=4)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Future prediction Trend')

    # Save the plot to a bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()

    # Previous plot will be cleared and new will be ploted.
    plt.clf()

    # Return the predicted result to display on a new page
    return render_template('result.html',
                            company=company, 
                            start_date=start_date, 
                            end_date=end_date, 
                            tables=[new_df.to_html(classes='data', header="true")],
                            accuracy=accuracy, 
                            plot_data=plot_data, 
                            forcast_out=forcast_out
                            )


if __name__ == '__main__':
    app.run(debug=True)