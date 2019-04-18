import signal
import random
from time import sleep


class WorkerBJobs:
    kill_now = False
    current_counter = 1

    def __init__(self, publish):
        self.publish = publish

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

    def counter_task(self, queue):
        self.publish({'Message': {'value': 'Executing Counter Task'}}, routing_key=queue.routing_key,
                     declare=[queue])
        while True:
            value = '{}'.format(self.current_counter)
            self.publish({'Message': {'value': value, 'task_id': queue.routing_key}},
                         routing_key=queue.routing_key,
                         declare=[queue])
            sleep(1)
            self.current_counter += 1
            if self.kill_now:
                return False

    def sum_task(self, queue):
        self.publish({'Message': {'value': 'Executing Addition Task'}}, routing_key=queue.routing_key,
                     declare=[queue])
        value = self.sum_of_rand_nums()
        sleep(20)
        self.publish({'Message': {'value': value, 'task_id': queue.routing_key}},
                     routing_key=queue.routing_key,
                     declare=[queue])
        return value

    def sum_of_rand_nums(self):
        return random.randint(1, 1000) + random.randint(1, 1000)
