import base64
from io import BytesIO
from flask import Flask, url_for, render_template, request, Response
from yahoo_fin.stock_info import get_data
import matplotlib.pyplot as plt
import math, datetime
from sklearn import preprocessing
import numpy as np
import joblib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    company = request.form['company']
    start_date = request.form['start']
    end_date = request.form['end']
    
    # Fetching the stock data
    df = get_data(company, start_date=start_date, end_date=end_date, index_as_date=True, interval="1d")

    # Feature engineering
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df['hl_pct'] = (df['high'] - df['close']) / df['close'] * 100
    df['pct_change'] = (df['close'] - df['open']) / df['open'] * 100
    df = df[['close', 'hl_pct', 'pct_change', 'volume']]
    new_df = df.describe()

    # Forecast column and shift the labels
    forecast_col = 'close'
    df.fillna(-99999, inplace=True)
    forecast_out = int(math.ceil(0.015 * len(df)))  # Predicting 1.5% future data
    df['label'] = df[forecast_col].shift(-forecast_out)

    # Splitting data into features and labels
    X = np.array(df.drop(['label'], axis=1))
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]  # Data to predict future
    X = X[:-forecast_out]  # Remove last forecast_out rows used for future prediction
    df.dropna(inplace=True)
    y = np.array(df['label'])

    # Load the trained model
    model = joblib.load('Model.pkl')

    # Make predictions
    forecast_set = model.predict(X_lately)
    
    # Prepare the DataFrame for plotting
    df['Forecast'] = np.nan
    last_date = df.iloc[-1].name
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day

    for prediction in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [prediction]

    # Plotting the data
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

    # Clear the plot for next time
    plt.clf()

    # Return the predicted result to display on a new page
    return render_template('result.html',
                            company=company,
                            start_date=start_date,
                            end_date=end_date,
                            tables=[new_df.to_html(classes='data', header="true")],
                            plot_data=plot_data, 
                            forecast_out=forecast_out
                            )

if __name__ == '__main__':
    app.run(debug=True)