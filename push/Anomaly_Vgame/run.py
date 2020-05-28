import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf,pacf,acovf,pacf_yw,pacf_ols
from pmdarima import AutoARIMA,auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import datetime
import time

from kafka_Mess import Kafka_Mess
import connect_clickhouse as ckl


import logging
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(filename='./log/test_1.log',
                    format='[%(asctime)s] [%(levelname)s] :%(message)s',
                    level=logging.DEBUG)

# ip = "10.3.3.160"
ip = "10.84.86.95"

def check_anomaly(perdict,valid):
    if valid*0.9 > perdict or valid*1.1 < perdict:
        return True
    return False 

def main():
    kafka_client = Kafka_Mess(ip="10.84.86.123",port = "9092")
    df = ckl.load_all_data(ip)
    df["date"] = pd.to_datetime(df["report_date"], format = "%Y%m%d")
    df = df.set_index("date")
    df_data = df["revenues_daily"]
    data_train = df_data.loc[:"2020-01-01"]
    data_test = df_data.loc["2020-01-02":]
    history = data_train.copy()
    perdiction_data = data_test["2020-01-02":"2020-01-02"]
    anomaly = data_test["2020-01-02":"2020-01-02"]

    for t in range(len(data_test)):
        
        model = SARIMAX(history, order=(1, 1, 1),seasonal_order = (1, 0, 0, 12))
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
            ckl.insert_data(ip,(perdiction_data.index.max() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),perdiction_data[perdiction_data.index.max()],obs,obs)
        else:
            ckl.insert_data(ip,(perdiction_data.index.max() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),perdiction_data[perdiction_data.index.max()],obs)
        print(perdiction_data.index.max())
        history.loc[history.index.max()+ datetime.timedelta(days=1)] = obs
        # plt.figure(figsize=(15,5))
        # start = perdiction_data.index.max()
        # end = perdiction_data.index.max() - datetime.timedelta(days=10)
        # plt.plot(history.loc[end:start],label='Thực tế',color = "green")
        # plt.plot(perdiction_data.loc[end:start], label='Dự đoán',color = "red")
        # plt.scatter(anomaly.loc[end:start].index,anomaly.loc[end:start],marker = "v", color = "red",s=100,label = "Bất thường")
        # plt.xlabel('Thời gian')
        # plt.xticks(rotation=15)
        # plt.ylabel('Doanh thu')
        # plt.title("Dự đoán doanh thu")
        # plt.legend(loc='best')
        # file = "img/"+ str(history.index.max().date()) +".svg"
        # plt.savefig(file, format="svg")
        # plt.show()
    while True :
        try:
            obs = ckl.load_day_data(ip)
            if obs != None:
                print(obs)
                history.loc[history.index.max() + datetime.timedelta(days=1)] = obs
                model = SARIMAX(history, order=(1, 1, 1),seasonal_order = (1, 0, 0, 12))
                model_fit = model.fit(disp=False)
                yhat = model_fit.predict(len(history),len(history),typ='levels')
                perdiction_data.loc[perdiction_data.index.max() + datetime.timedelta(days=1)] = yhat[0]
                if check_anomaly(perdiction_data[perdiction_data.index.max()],obs):
                    anomaly.loc[perdiction_data.index.max() - datetime.timedelta(days=1) ] = obs
                    mess = {
                        "Date": perdiction_data.index.max() - datetime.timedelta(days=1),
                        "Revenue" : obs,
                        "Perdiction": perdiction_data[perdiction_data.index.max()]
                    }
                    kafka_client.publish_message('anomaly_notify', 'raw',str(mess))
                    ckl.insert_data(ip,(perdiction_data.index.max() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),perdiction_data[perdiction_data.index.max()],obs,obs)
                else:
                    ckl.insert_data(ip,(perdiction_data.index.max() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),perdiction_data[perdiction_data.index.max()],obs)
            # else :
            #     print(obs)
            time.sleep(10)
        except NameError:
            print(NameError)

if __name__ == "__main__":
    main()
    print("done")
    