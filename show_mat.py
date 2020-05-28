import argparse
import datetime
import calendar
import matplotlib.pyplot as plt
import yaml
import pandas as pd
def save_img(history_data, predict_data, anomaly_data):
    start = predict_data.index.max()
    end = predict_data.index.max() - datetime.timedelta(days=10)

    plt.figure(figsize=(15, 5))
    plt.title("Dự đoán doanh thu")
    plt.xlabel('Thời gian')
    plt.ylabel('Doanh thu')
    plt.xticks(rotation=15)

    plt.plot(history_data.loc[end:start], label='Thực tế', color="green")
    plt.plot(predict_data.loc[end:start], label='Dự đoán', color="red")
    plt.scatter(anomaly_data.loc[end:start].index, anomaly_data.loc[end:start], marker="v", color="red", s=100,
                label="Bất thường")
    plt.annotate(anomaly_data,anomaly_data.loc[end:start].index, anomaly_data.loc[end:start])
    plt.legend(loc='best')
    plt.savefig('test.png', format="png")

if __name__ == "__main__":
    data = pd.read_csv('asd.csv')

    print(data.head())