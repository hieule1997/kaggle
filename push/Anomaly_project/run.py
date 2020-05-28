import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf,pacf,acovf,pacf_yw,pacf_ols
from pmdarima import AutoARIMA,auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import datetime
from kafka_Mess import Kafka_Mess
import logging
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(filename='./log/test_1.log',
                    format='[%(asctime)s] [%(levelname)s] :%(message)s',
                    level=logging.DEBUG)
def check_anomaly(perdict,valid):
    if valid*0.7 > perdict or valid*1.3 < perdict:
        return True
    return False 

def main():
    kafka_client = Kafka_Mess(ip="10.84.86.123",port = "9092")
    dataset = pd.read_csv("data/kenhGD.csv")
    dataset.columns = ["date","kenh","code","revenue"]
    dataset["date"] = pd.to_datetime(dataset["date"], format = "%Y%m%d %H:%M:%S" , utc = True)
    dataset["datetime"] = pd.to_datetime(dataset['date'].dt.strftime('%m/%d/%Y'))
    data_SMS = dataset[dataset["kenh"] == "SMS"]
    df = data_SMS.groupby("datetime").mean().loc["2019-02-01":]
    df = df["revenue"]
    data_train = df.loc["2019-02-01":"2019-07-01"]
    data_test = df.loc["2019-07-02":]
    history = data_train.copy()
    perdiction_data = data_test["2019-07-02":"2019-07-02"]
    anomaly = data_test["2019-07-02":"2019-07-02"]

    for t in range(len(data_test)):
        model = SARIMAX(history, order=(1, 1, 1))
        model_fit = model.fit(disp=False)
        yhat = model_fit.predict(len(history),len(history),typ='levels')
        perdiction_data.loc[perdiction_data.index.max() + datetime.timedelta(days=1)] = yhat[0]
        obs = data_test[t]
        if check_anomaly(perdiction_data[perdiction_data.index.max()],obs):
            anomaly.loc[perdiction_data.index.max() - datetime.timedelta(days=1) ] = obs
            mess = {
                "Date": perdiction_data.index.max() - datetime.timedelta(days=1),
                "Revenue" : obs,
                "Perdiction": perdiction_data[perdiction_data.index.max()]
            }
            kafka_client.publish_message('anomaly_notify', 'raw',str(mess))
        history.loc[history.index.max()+ datetime.timedelta(days=1)] = obs
        plt.figure(figsize=(15,5))
        start = perdiction_data.index.max()
        end = perdiction_data.index.max() - datetime.timedelta(days=10)
        plt.plot(history.loc[end:start],label='Thực tế',color = "green")
        plt.plot(perdiction_data.loc[end:start], label='Dự đoán',color = "red")
        plt.scatter(anomaly.loc[end:start].index,anomaly.loc[end:start],marker = "v", color = "red",s=100,label = "Bất thường")
        plt.xlabel('Thời gian')
        plt.xticks(rotation=15)
        plt.ylabel('Doanh thu')
        plt.title("Dự đoán doanh thu")
        plt.legend(loc='best')
        file = "img/"+ str(history.index.max().date()) +".svg"
        plt.savefig(file, format="svg")
        # plt.show()
if __name__ == "__main__":
    main()
    print("done")
    