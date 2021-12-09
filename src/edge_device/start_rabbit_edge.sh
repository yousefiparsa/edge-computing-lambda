docker run -d --hostname my-rabbit --name rabbit_daemon rabbitmq:3
docker run -d --hostname my-rabbit --name rabbit_manager -p 8080:15672 -p 5672:5672 rabbitmq:3-management

