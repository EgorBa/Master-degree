from database import DataBase
from kafka import KafkaConsumer
from json import loads

from logger import Logger

SHOW_LOG = True
TAG = "KafkaConsumer"
TOPIC = 'data'


class Consumer:

    def __init__(self) -> None:
        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)
        self.consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8')))
        self.data = DataBase().get_data_as_dataframe()
        self.max_size = len(self.data)
        self.log.info(f"Kafka consumer was created")

    def observe_data(self):
        for message in self.consumer:
            self.log.info(f"Kafka get message = {message}")
            count_lines = int(message.value["count_lines"])
            self.data = self.data[:min(count_lines, self.max_size)]

    def get_data(self):
        while len(self.data) == 0:
            continue
        return self.data
