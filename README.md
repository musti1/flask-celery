# PYTHON FLASK CELERY + ELK (Realtime Logging System)
This project is build in Python framework flask to handle logging in a python celery environment with ELK stack.

Clone repository and follow the following steps to setup the app.

# Creating Build

```docker-compose build```

# Starting Services

```docker-compose up -d```

-d flag instruct docker compose to run services as daemon.

After starting the services. We can access our python flask app server on.

```http://localhost:5000```

And rabbitmq server on.

```http://localhost:15672```

Elasticsearch will be available on localhost port `9200` and logstash on port `9999`.


# Inspecting Services

```docker-compose ps```

# Inspecting Logs

```docker-compose logs```

We will now cover how we can inspect individual services logs.

```docker-compose logs [service_name] -f --tail=10```

In above command we use -f flag to follow logs and --tail to fetch last 10 lines you can always increase this number to your liking.

# Interacting with Python flask container

```docker-compose exec -it web /bin/bash```

# Stopping containers

```docker-compose down```