const express = require("express");
const axios = require("axios");
const hateoasLinker = require("express-hateoas-links");
const soapRequest = require("easy-soap-request");
const swaggerUi = require("swagger-ui-express");
const swaggerDocument = require("./swaggerconfig.json");

const app = express();
app.use(express.json());
app.use(hateoasLinker);
app.use(require("cors")());
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

const SOAP_API_URL = "http://localhost:8000/times/";
const REST_API_URL = "http://localhost:8081/";

app.get("/times/", async (req, res) => {
    try {

        const response = await axios.get(`${REST_API_URL}times/`);
        const times = response.data.map(time => ({
            ...time,
            links: [
                { rel: "self", method: "GET", href: `${REST_API_URL}/times/${time.id}` },
                { rel: "delete", method: "DELETE", href: `${REST_API_URL}/times/${time.id}` },
                { rel: "put", method: "PUT", href: `${REST_API_URL}/times/${time.id}` }
            ]
        }));
        res.json(times);
    } catch (error) {
        console.log(error)
        res.status(500).json("Erro ao buscar tiumes");
    }
});

// Rota para a API SOAP (conversão de REST para SOAP)
app.post("/times/", async (req, res) => {
    const { nome, cidade, estado } = req.body;
    const xml = `
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:web="http://tempuri.org/">
            <soapenv:Header/>
            <soapenv:Body>
                <web:Authenticate>
                    <web:nome>${nome}</web:nome>
                    <web:cidade>${cidade}</web:cidade>
                    <web:estado>${estado}</web:estado>
                </web:Authenticate>
            </soapenv:Body>
        </soapenv:Envelope>`;
    const headers = { "Content-Type": "text/xml" };
    try {
        const { response } = await soapRequest({ url: SOAP_API_URL, headers, xml });
        
        res.send(response.body);
    } catch (error) {
        console.log(error)
        res.status(500).json({ error: "Erro ao criar time" });
    }
});

app.listen(3001, () => console.log("Gateway rodando na porta 3001"));