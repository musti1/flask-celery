from subprocess import Popen, PIPE


class WorkerATasks:
    @staticmethod
    def long_task(name, job_id):
        process = Popen(['sh jobs/job.sh ' + name], shell=True, stdout=PIPE, bufsize=0, stderr=PIPE)
        while True:
            line = process.stdout.readline()
            if not line:
                break
            string = 'Job ID: ' + job_id + ' value: ' + line.decode()
            with open('LongTaskWorkerA.log', 'ab') as file:
                file.write(string.encode())

    @staticmethod
    def fail_task():
        return ''

