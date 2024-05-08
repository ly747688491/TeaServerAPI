"""
@Project        ：tea_server_api 
@File           ：rabbitmq.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/7 下午5:57 
@Description    ：
"""
import pika

from config.setting import setting


class RabbitMQService:
    def __init__(self):
        self.host = setting.RABBITMQ_HOST
        self.port = setting.RABBITMQ_PORT
        self.user = setting.RABBITMQ_USERNAME
        self.password = setting.RABBITMQ_PASSWORD
        self.exchange = setting.RABBITMQ_EXCHANGE

    def send_message(self, queue_name, message):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=pika.PlainCredentials(self.user, self.password),
            )
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type="direct", durable=True)
        # 声明队列
        channel.queue_declare(queue=queue_name, durable=True)

        # 将队列绑定到交换机
        channel.queue_bind(queue=queue_name, exchange=self.exchange, routing_key=queue_name)

        # 开启确认模式
        channel.confirm_delivery()

        # 定义一个回调函数来处理未被路由的消息
        def handle_returned_message(method_frame, properties, body):
            print(f"Message was returned: {body}")

        # 发送持久化消息
        try:
            channel.basic_publish(
                exchange=self.exchange,
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # 使消息持久化
                ),
                mandatory=True,  # 如果消息不能被路由，将返回给生产者
            )
            print(f" [x] Sent '{message}'")
        except pika.exceptions.UnroutableError:
            print(f"Message was not delivered: {message}")
        # 关闭连接
        connection.close()

