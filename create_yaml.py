import yaml
from datetime import datetime

with open("mail.yml", 'r') as stream:
    doc = yaml.load(stream, Loader=yaml.FullLoader)
    time_send = doc["time_send"]["ibox"]["DAILY_REVENUE"]
    time_send = datetime.strptime(time_send, "%Y-%m-%d")
    print(time_send)
    datenow = datetime.now()
    print(datenow)
    if time_send < datenow:
        time_send = datenow.strftime("%Y-%m-%d")
    doc["time_send"]["ibox"]["DAILY_REVENUE"] = time_send
    sort_file = yaml.dump(doc, sort_keys=True)
    print(sort_file)

with open('mail.yml', 'w') as file:
    yaml.dump(sort_file, file, default_flow_style=False)
