#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pika
import json
from time import sleep

queue = 'oss.url_test'  # 队列名
routing_key = 'url_test'
exchange = 'oss_test'

# 新建连接，rabbitmq安装在本地则hostname为'localhost'
hostname = '10.96.22.142'
username = "dCVrbGR3NpDibk5fi9csK9y1XZo6X6uk"
password = "K3qqeNKP4tymXwyua7oPfgOvqJ"
port = 5672

credentials = pika.PlainCredentials(username=username, password=password)
parameters = pika.ConnectionParameters(host=hostname, port=port, credentials=credentials)
connection = pika.BlockingConnection(parameters=parameters)

# 创建通道
channel = connection.channel()
# 创建broker
channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
# 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
channel.queue_declare(queue=queue, durable=True)
# 把队列和中间人绑定
channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
# 交换机; 队列名,写明将消息发往哪个队列; 消息内容
# routing_key在使用匿名交换机的时候才需要指定，表示发送到哪个队列,注意当未定义exchange时，routing_key需和queue的值保持一致
data = {"abcasdasdasdasdasdasdasd": "tesasdasdasdasdasdasdasdasdasdasdt1"}
a = 0
while a < 1000:
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(data))
    sleep(3)
    a += 3
# 关闭连接
connection.close()
