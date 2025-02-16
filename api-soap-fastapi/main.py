from fastapi import FastAPI, Depends, Request, Response
import xmltodict
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Time, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_times(db: Session = Depends(get_db)):
     return db.query(Time).all()


@app.post("/times/")
async def read_item(request: Request):
   
    try:
        xml_data = await request.body()
        print(xml_data)
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

        soap_response = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Body>
                <web:Response>
                    <web:message>Success! Time {nome} registered.</web:message>
                </web:Response>
            </soapenv:Body>
        </soapenv:Envelope>
        """
        return Response(content=soap_response, media_type="text/xml")
    except Exception as e:
        return Response(content="Error processing SOAP request", status_code=500)