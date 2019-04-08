from subprocess import Popen, PIPE


class WorkerATasks:
    def long_task(self, name, job_id):
        process = Popen(['sh job.sh ' + name], shell=True, stdout=PIPE, bufsize=0, stderr=PIPE)
        while True:
            line = process.stdout.readline()
            if not line:
                break
            string = 'Job ID: ' + job_id + ' value: ' + line.decode()
            with open('tests.log', 'ab') as file:
                file.write(string.encode())

    def failTask(self):
        return ''

    def execute(self, name, job_id):
        try:
            return self.long_task(name, job_id)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    c = WorkerATasks()
    c.execute('testing')
