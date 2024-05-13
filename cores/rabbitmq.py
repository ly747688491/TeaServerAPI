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
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(queue=queue_name, exchange=self.exchange, routing_key=queue_name)
        channel.confirm_delivery()

        # 定义一个回调函数来处理未被路由的消息
        def handle_returned_message(channel, method_frame, header_frame, body):
            print(f"Message was returned: {body.decode()}")
            raise pika.exceptions.UnroutableError(f"Message was returned: {body.decode()}")

        # 捕获返回的消息
        channel.add_on_return_callback(handle_returned_message)

        # 发送消息并检查确认
        try:
            is_delivered = channel.basic_publish(
                exchange=self.exchange,
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # 使消息持久化
                ),
                mandatory=True,
            )
            if is_delivered:
                print(f" [x] Sent '{message}'")
                return True, "Message sent successfully"
            else:
                return False, "Failed to deliver message"
        except pika.exceptions.UnroutableError as e:
            print(str(e))
            return False, str(e)
        finally:
            # 关闭连接
            connection.close()
