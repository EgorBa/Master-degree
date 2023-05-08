from kafka import KafkaProducer
from json import dumps
from logger import Logger

SHOW_LOG = True
TAG = "KafkaProducer"
TOPIC = 'data'


class Producer:

    def __init__(self) -> None:
        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))
        self.log.info(f"Kafka producer was created")

    def update_data(self, count_lines):
        data = {'count_lines': count_lines}
        self.log.info(f"Kafka send data = {data}")
        self.producer.send(TOPIC, value=data)