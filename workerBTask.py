from jobs.workerBJob import sum_of_rand_nums, counter_value
from time import sleep


class WorkerBTasks:
    @staticmethod
    def counter_task(logger):
        logger.info(f'Executing counter task')
        counter = 1
        while True:
            value = counter_value(counter)
            logger.info(f'The current value is {value}')
            sleep(1)
            counter += 1

    @staticmethod
    def sum_task(logger):
        logger.info(f'Executing addition task')
        value = sum_of_rand_nums()
        sleep(20)
        logger.info(f'Sum of random number is {value}')
        return value
