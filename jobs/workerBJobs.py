import signal
import random
from time import sleep


class WorkerBJobs:
    logger = False
    kill_now = False
    current_counter = 1

    def __init__(self, logger):
        self.logger = logger

    def exit_gracefully(self, signum, frame):
        self.logger.info(f'Breaking out of the loop')
        self.logger.info(f'Current state before exit {self.current_counter}')
        self.logger.info(f'Gracefully exiting')
        self.kill_now = True

    def counter_task(self, publisher, queue):
        publisher({'Message': 'Executing Counter Task'}, routing_key=queue.routing_key,
                  declare=[queue])
        while True:
            value = '{}'.format(self.current_counter)
            publisher({'Message': {'Current_value': value, 'task_id': queue.routing_key}}, routing_key=queue.routing_key,
                      declare=[queue])
            self.logger.info(value)
            sleep(1)
            self.current_counter += 1
            if self.kill_now:
                return False

    def sum_task(self):
        self.logger.info(f'Executing addition task')
        value = self.sum_of_rand_nums()
        sleep(20)
        self.logger.info(f'Sum of random number is {value}')
        return value

    def sum_of_rand_nums(self):
        return random.randint(1, 1000) + random.randint(1, 1000)
