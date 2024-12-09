from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import asyncio

from app.services.message_consumer_service import RabbitmqConsumer


load_dotenv()


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    sms_consumer = RabbitmqConsumer(queue="sms_queue")
    email_consumer = RabbitmqConsumer(queue="email_queue")

    asyncio.create_task(sms_consumer.consume_messages())
    asyncio.create_task(email_consumer.consume_messages())

    print("Consumidores iniciados para SMS e e-mail.")

    yield

    print("Finalizando o consumo de mensagens e limpeza.")

app = FastAPI(
    title="API de Consumo de Mensagens",
    description="""API responsável pelo consumo das mensagens (SMS ou E-MAIL) presentes nas filas do RabbitMQ.""",
    version="1.0",
    lifespan=lifespan,
)

@app.get("/")
async def raiz():
    return {"message": "O serviço está consumindo mensagens."}


if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='debug', reload=True)
