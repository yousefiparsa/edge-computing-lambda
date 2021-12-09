from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import mysql.connector
import MySQLdb
import yaml
from database import connection
import numpy as np
import time

# Read config parameters for mysql
with open('config.yaml') as f:
    config = yaml.safe_load(f)
    host = config['cloud_mysql_hostname']
    username = config['cloud_mysql_username']
    password = config['cloud_mysql_password']
    database = config['cloud_mysql_database']
    port = config['cloud_mysql_port']

# Connect to mysql database and get cursor
mydb = mysql.connector.connect(
    host=host,
    user=username,
    passwd=password,
    database=database,
    port=port
)
mycursor = mydb.cursor()
mydb.commit()

while(1):
    query = "SELECT temp_id, temp FROM temps_found ORDER BY time_stamp ASC LIMIT 1000"
    mycursor.execute(query)
    temps_found = np.array(mycursor.fetchall())
    X = temps_found[:, 1]
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        # Save temp into mysql
        sql = "INSERT INTO temps_predicted(temp, sensor_type,  time_stamp) VALUES (%s, %s, %s)"
        val = (float(yhat[0]), 4, time.strftime('%Y-%m-%d %H:%M:%S'))
        mycursor.execute(sql, val)
        mydb.commit()
        # print('predicted=%f, expected=%f' % (yhat, obs))
    # error = mean_squared_error(test, predictions)
    # print('Test MSE: %.3f' % error)

    # Plotting the test/prediction results
    # pyplot.plot(test, color='blue')
    # pyplot.plot(predictions, color='red')
    # pyplot.show()
