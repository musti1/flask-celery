import requests


class FlowerApi:
    @staticmethod
    def terminate(task_id):
        response = requests.post('http://flower:5555/api/task/revoke/{}?terminate=true'.format(task_id))
        if response.status_code == 200:
            return True
        return False

    @staticmethod
    def list_tasks():
        response = requests.get('http://flower:5555/api/tasks')
        if response.status_code == 200:
            return response.text
        return []

    @staticmethod
    def list_workers():
        response = requests.get('http://flower:5555/api/workers?refresh=1')
        if response.status_code == 200:
            return response.text
        return []

    @staticmethod
    def task_info(task_id):
        response = requests.get('http://flower:5555/api/task/info/' + task_id)
        if response.status_code == 200:
            return response.json()
        return False
