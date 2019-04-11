from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


class EsHelper:
    def __init__(self):
        self.elasticsearch = Elasticsearch(
            ['elasticsearch'],
            scheme="http",
            port=9200,
        )

        self.index = 'logstash-*'
        self.type = 'doc'

    def fetch(self, task_id):
        search = Search(using=self.elasticsearch, index=self.index, doc_type=self.type).query(
            Q("query_string", query="@fields.celery.correlation_id:{}".format(task_id))).sort({"@timestamp":{"order":"desc"}})
        count = search.count()
        res = search[0:count].execute()

        return res

    def fetchupdatedlogs(self, task_id,date_from):
        search = Search(using=self.elasticsearch, index=self.index, doc_type=self.type).query(
            Q("query_string", query="@fields.celery.correlation_id:{a} AND @timestamp:[\"{b}\" TO now]".format(a=task_id,b=date_from))).sort({"@timestamp":{"order":"desc"}})
        count = search.count()
        res = search[0:count].execute()

        return res

    def upload(self, body):
        res = self.elasticsearch.index(index=self.index, doc_type=self.type, body=body)

        return res
