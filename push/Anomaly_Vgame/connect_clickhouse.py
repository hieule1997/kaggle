from clickhouse_driver import Client
import pandas as pd
import datetime
import time
def connect_clickhouse():
    return Client('10.3.3.160')

def load_all_data( ip= None):
    client = Client(ip)
    query_all = 'select report_date,sum(revenues_daily) from vgame.report_revenues_daily where type in (0) group by report_date order by report_date ASC;'
    data = client.execute(query_all)
    return pd.DataFrame(data, columns = ["report_date","revenues_daily"])
    
def load_day_data(ip = None):
    client = Client(ip)
    query = "select report_date,sum(revenues_daily) from vgame.report_revenues_daily where type in (0) and toDate(report_revenues_daily.report_date) = toDate('" + str(datetime.date.today()) + "') group by report_date"
    # query = "select report_date,sum(revenues_daily) from vgame.report_revenues_daily where type in (0) and toDate(report_revenues_daily.report_date) = toDate('2020-03-14') group by report_date"
    data = client.execute(query)
    if len(data) == 0:
        return None
    else:
        df = pd.DataFrame(data, columns = ["report_date","revenues_daily"])
        df_data = df["revenues_daily"][0]
        return df_data

def insert_data(ip = None,date = None,perdiction = None,revenue = None,anomaly = None):
    client = Client(ip)
    query = "INSERT INTO vgame.anomaly (CreateDate, perdiction, revenue,anomaly) VALUES (toDate('"+ str(date) +"'), '" + str(perdiction) + "', '" + str(revenue) + "','" + str(anomaly) + "')"
    client.execute(query)


def create_table(ip= None):
    client = Client(ip)
    query = """CREATE TABLE IF NOT EXISTS vgame.anomaly
                (
                    `CreateDate` DateTime('Asia/Ho_Chi_Minh'),
                    `perdiction` Nullable(Float64),
                    `revenue` Nullable(Float64),
                    `anomaly` Nullable(Float64)
                )
                ENGINE = Log();"""
    client.execute(query)

def drop_tables_exist(ip = None):
    client = Client(ip)
    query = """DROP TABLE IF EXISTS vgame.anomaly;"""
    client.execute(query)


if __name__ == "__main__":
    ip = "10.3.3.160"
    data = load_day_data(ip)
    while True :
        obs = load_day_data(ip)
        if obs != None:
            print(obs)
        else:
            print("No Data")
        time.sleep(10)
    