from subprocess import Popen, PIPE , STDOUT
import sys
import shlex
import time

class WorkerATasks:
    @staticmethod
    def long_task(logger,name, job_id):
        logger.info(f'Executing long task')
        cmd = "sh jobs/longTaskjob.sh {}".format(name)
        process = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=0)
        while True:
            line = process.stdout.readline()
            if not line:
                break
            logger.info(f'{line.decode()}')


    @staticmethod
    def fail_task(logger):
        cmd = "sh jobs/failTaskjob.sh"
        logger.info(f'Executing fail task')
        process = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=0)
        line = process.stdout.readline()
        logger.info(f'Returned Result : {line.decode()}')
        raise Exception(F'Task is failing')

