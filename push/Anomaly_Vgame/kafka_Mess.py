from kafka import KafkaProducer 

class Kafka_Mess:
    def __init__(self, ip=None , port = None):
        self.ip = ip
        self.port = port
        
    def connect_kafka_producer(self):
        _producer = None
        try:
            host = self.ip + ":" + self.port
            _producer = KafkaProducer(bootstrap_servers=[host], api_version=(0, 10, 1))
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
        finally:
            return _producer

    def publish_message(self,topic_name, key, value):
        try:
            kafka_producer = self.connect_kafka_producer()
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            kafka_producer.send(topic_name, key=key_bytes, value=value_bytes)
            kafka_producer.flush()
        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))