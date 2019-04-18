from celery import Celery


class CeleryApi(object):
    def __init__(self):
        self.CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
        self.app = Celery(broker=self.CELERY_BROKER_URL)

    def terminate(self, task_id):
        response = self.app.control.revoke(task_id, terminate=True)
        if response:
            return True
        return False

    def list_tasks(self):
        response = self.app.control.inspect().active()
        if response:
            return response
        return []
