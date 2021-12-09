import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from database import connection

# Importing data from the SQL server
c, conn = connection()

query = "SELECT * FROM temps_found;"
c.execute(query)
data = c.fetchall()
df = pd.DataFrame.from_records(data)
conn.close()

# Creating train and test set
train = df[0:8000]
test = df[8000:]

print(train.head())
print(test.head())

# Aggregating the dataset at daily level
df.Timestamp = pd.to_datetime(df.Date, format='%d-%m-%Y %H:%M')
df.index = df.Timestamp
df = df.resample('D').mean()
train.Timestamp = pd.to_datetime(train.Date, format='%d-%m-%Y %H:%M')
train.index = train.Timestamp
train = train.resample('D').mean()
test.Timestamp = pd.to_datetime(test.Date, format='%d-%m-%Y %H:%M')
test.index = test.Timestamp
test = test.resample('D').mean()

y_hat_avg = test.copy()
fit1 = sm.tsa.statespace.SARIMAX(train.Temp, order=(2, 1, 4),
                                 seasonal_order=(0, 1, 1, 7)).fit()
y_hat_avg['SARIMA'] = fit1.predict(start="2018-11-1",
                                   end="2018-11-31", dynamic=True)
plt.figure(figsize=(16, 8))
plt.plot(train['Temp'], label='Train')
plt.plot(test['Temp'], label='Test')
plt.plot(y_hat_avg['SARIMA'], label='SARIMA')
plt.legend(loc='best')
plt.show()
