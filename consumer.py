from kombu import Connection, Queue


class Consumer:
    def __init__(self, queue):
        self.conn = Connection('amqp://rabbitmq:rabbitmq@rabbit:5672//')
        self.task_queue = Queue(queue, routing_key=queue)

    def start_consumer(self):
        consumer = Consumer(self.conn, [self.task_queue], callbacks=[self.process_message])
        consumer.consume()

        self.conn.drain_events()

    @staticmethod
    def process_message(body, message):
        print(body['message']['Value'], flush=True)
        message.ack()
