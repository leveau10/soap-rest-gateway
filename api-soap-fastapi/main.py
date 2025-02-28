from fastapi import FastAPI, Depends, Request, Response
import pika
import xmltodict
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Time, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

RABBITMQ_URL = "amqp://guest:guest@localhost"
QUEUE_NAME = "fila_do_pao"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_times(db: Session = Depends(get_db)):
     return db.query(Time).all()


def create_time(xml_data):
   
    try:
        converted_xml = xmltodict.parse(xml_data)

        body = converted_xml.get("soapenv:Envelope", {}).get("soapenv:Body", {})
        timeInfos = body.get("web:Authenticate", {})

        nome = timeInfos.get("web:nome", "Unknown")
        cidade = timeInfos.get("web:cidade", "Unknown")
        estado = timeInfos.get("web:estado", "Unknown")

        db = SessionLocal()
        db_time = Time(nome=nome, cidade=cidade, estado=estado)
        db.add(db_time)
        db.commit()
        db.close()

        print("Time registrado!", nome)
    except Exception as e:
        print("deu erro")

def consume_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    
    def callback(ch, method, properties, body):
        print("Mensagem recebida!")
        create_time(body.decode("utf-8"))

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print("Aguardando mensagens...")
    channel.start_consuming() 

if __name__ == "__main__":
    consume_queue()