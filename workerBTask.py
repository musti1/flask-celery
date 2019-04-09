from jobs.workerBJob import sum_of_rand_nums, counter_value
from time import sleep


class WorkerBTasks:
    @staticmethod
    def counter_task():
        counter = 1
        while True:
            value = counter_value(counter)
            with open('counterTaskWorkerB.log', 'ab') as file:
                file.write(value.encode())
            sleep(1)
            counter += 1

    @staticmethod
    def sum_task():
        value = sum_of_rand_nums()
        sleep(20)
        with open('sumTaskWorkerB.log', 'ab') as file:
            file.write(value.encode())
        return value
