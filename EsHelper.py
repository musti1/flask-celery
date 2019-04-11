from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


class EsHelper:
    def __init__(self):
        self.elasticsearch = Elasticsearch(
            ['elasticsearch'],
            scheme="http",
            port=9200,
        )

        self.index = 'workers'
        self.type = 'tasks'

    def fetch(self, task_id):
        search = Search(using=self.elasticsearch, index=self.index, doc_type=self.type).query(
            Q("query_string", query="task_id:{}".format(task_id)))
        count = search.count()
        res = search[0:count].execute()

        return res

    def upload(self, body):
        res = self.elasticsearch.index(index=self.index, doc_type=self.type, body=body)

        return res
