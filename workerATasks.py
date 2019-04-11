from subprocess import Popen, PIPE
import time

class WorkerATasks:
    @staticmethod
    def long_task(logger,name, job_id):
        process = Popen(['sh jobs/job.sh' + name],shell= True, executable='/bin/bash',stdout=PIPE, bufsize=0, stderr=PIPE)
        while True:
            output = process.stdout.readline()
            #if output == '' and process.poll() is not None:
           #     break
           # if output:
              #  log = output.strip()
            logger.info(f'{name}')
            time.sleep(3)


    @staticmethod
    def fail_task():
        return ''

