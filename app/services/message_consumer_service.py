import json
from os import environ
from email.message import EmailMessage

import asyncio
from aio_pika.exceptions import QueueEmpty
from twilio.rest import Client
import aiosmtplib
import aio_pika
from pydantic import EmailStr


class RabbitmqConsumer:
    def __init__(self, queue: str):
        self.__host = environ.get('RABBITMQ_HOST')
        self.__port = int(environ.get('RABBITMQ_PORT'))
        self.__username = environ.get('RABBITMQ_DEFAULT_USER')
        self.__password = environ.get('RABBITMQ_DEFAULT_PASS')
        self.__queue = queue
        self.__connection = None
        self.__channel = None

    async def __connect(self):
        url = f"amqp://{self.__username}:{self.__password}@{self.__host}:{self.__port}/"
        print(f"Conectando ao RabbitMQ: {url}")
        self.__connection = await aio_pika.connect_robust(url)
        self.__channel = await self.__connection.channel()
        print(f"Conexão estabelecida e canal criado para a fila '{self.__queue}'.")

    async def consume_messages(self):
        if not self.__connection or self.__connection.is_closed:
            await self.__connect()

        queue = await self.__channel.declare_queue(self.__queue, durable=True)
        print(f"Consumindo mensagens da fila '{self.__queue}'...")

        while True:
            try:
                message = await queue.get(timeout=5)
                if message is None:
                    continue

                message_body = message.body.decode()
                print(f"Mensagem recebida: {message_body}")
                data = json.loads(message_body)

                if self.__queue == "sms_queue":
                    await self.__process_sms(data)
                elif self.__queue == "email_queue":
                    await self.__process_email(data)

                await message.ack()
                print(f"Mensagem reconhecida e marcada como processada: {message_body}")
            except QueueEmpty:
                print("Fila vazia, aguardando novas mensagens...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Erro ao consumir mensagem: {e}")
                await asyncio.sleep(5)

    async def __process_email(self, data: dict):
        try:
            print(f"Processando Email com dados: {data}")
            if data["action"] == "EMAIL sent":
                to_address = data["content"]["to_address"]
                subject = data["content"]["subject"]
                message = data["content"]["message"]

                await self.__send_email(to_address, subject, message)
                print(f"Email enviado com sucesso para {to_address}.")
            else:
                print(f"Ação inválida para Email: {data['action']}")
        except KeyError as e:
            print(f"Erro ao processar Email, chave ausente: {e}")

    async def __process_sms(self, data: dict):
        try:
            print(f"Processando SMS com dados: {data}")
            if data["action"] == "SMS sent":
                to_number = data["content"]["to_number"]
                message = data["content"]["message"]

                await self.__send_sms(to_number, message)
                print(f"SMS enviado com sucesso para {to_number}.")
            else:
                print(f"Ação inválida para SMS: {data['action']}")
        except KeyError as e:
            print(f"Erro ao processar SMS, chave ausente: {e}")

    @staticmethod
    async def __send_sms(to_number: EmailStr, message: str):
        twilio_sid = environ.get("TWILIO_SID")
        twilio_auth_token = environ.get("TWILIO_AUTH_TOKEN")
        twilio_phone_number = environ.get("TWILIO_PHONE_NUMBER")

        client = Client(twilio_sid, twilio_auth_token)

        try:
            message_sent = client.messages.create(
                body=message,
                from_=twilio_phone_number,
                to=to_number
            )
            print(f"SMS enviado com sucesso para {to_number}. SID: {message_sent.sid}")
        except Exception as e:
            print(f"Erro ao enviar SMS para {to_number}: {e}")

    @staticmethod
    async def __send_email(to_address: str, subject: str, message_body: str):
        smtp_user = environ.get("SMTP_USER")
        smtp_password = environ.get("SMTP_PASSWORD")
        smtp_host = environ.get("SMTP_HOST")
        smtp_port = int(environ.get("SMTP_PORT"))

        message = EmailMessage()
        message["From"] = smtp_user
        message["To"] = to_address
        message["Subject"] = subject
        message.set_content(message_body)

        max_retries = 3
        attempt = 1

        while attempt <= max_retries:
            try:
                print(f"Tentando enviar o e-mail... Tentativa {attempt}/{max_retries}")
                async with aiosmtplib.SMTP(hostname=smtp_host, port=smtp_port, timeout=10) as client:
                    await client.login(smtp_user, smtp_password)
                    await client.send_message(message)
                    break
            except aiosmtplib.SMTPException as e:
                print(f"Falha ao enviar e-mail (Tentativa {attempt}/{max_retries}): {e}")
            except Exception as e:
                print(f"Ocorreu um erro inesperado (Tentativa {attempt}/{max_retries}): {e}")

            attempt += 1

        if attempt > max_retries:
            print(f"Máximo de tentativas alcançado. Falha ao enviar e-mail para {to_address}.")
