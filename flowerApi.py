import requests


class FlowerApi:
    @staticmethod
    def terminate(task_id):
        response = requests.post('http://localhost:5555/api/task/revoke/{}?terminate=true'.format(task_id))
        if response.status_code == 200:
            return True
        return False

    @staticmethod
    def list_tasks():
        response = requests.get('http://localhost:5555/api/tasks')
        if response.status_code == 200:
            return response.json()
        return False
