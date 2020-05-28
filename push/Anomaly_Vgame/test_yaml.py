import yaml
import json
with open(r'config.yaml') as file:
    doc = yaml.load(file, Loader=yaml.FullLoader)
    print(doc['clickhouse']["ip"])
