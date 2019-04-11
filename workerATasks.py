from subprocess import Popen, PIPE
from EsHelper import upload


class WorkerATasks:
    @staticmethod
    def long_task(name, job_id):
        process = Popen(['sh jobs/job.sh' + name],shell= True, executable='/bin/bash',stdout=PIPE, bufsize=0, stderr=PIPE)
        while True:
            line = process.stdout.readline()
            if line !='':
                string = 'Job ID: ' + job_id + ' value: ' + name
                upload_obj = {
                            "task_id":job_id,
                            "name":name,
                            "age": 27,
                            "about": "Love to play cricket",
                            "interests": ['sports','music'],
                            }
                upload(upload_obj)
            sleep(1)

    @staticmethod
    def fail_task():
        return ''

