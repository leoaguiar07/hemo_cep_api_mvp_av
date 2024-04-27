from flask import Flask,redirect , request
from flask_openapi3 import OpenAPI, Info, Tag
import requests
import json


from schemas.consulta import ConsultaBuscaSchema, ListagemConsultaSchema
from schemas.error import ErrorSchema 
from flask_cors import CORS

info = Info(title="API CEP", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
consulta_tag = Tag(
    name="Consulta",
    description="Adição, visualização e remoção de Consultas à base")


VIA_CEP_URL = "http://www.viacep.com.br/ws/{}/json"

def consulta_cep(cep):
    response = requests.get(VIA_CEP_URL.format(cep))
    if response.ok:
        address = json.loads(response.text)
        if address.get("erro"):
            raise ValueError("CEP inválido")
        return {
            "bairro": address.get("bairro", ""),
            "cep": address.get("cep", ""),
            "localidade": address.get("localidade", ""),
            "logradouro": address.get("logradouro", ""),
            "uf": address.get("uf", "")
        }
    elif response.status_code == 400:
        raise ValueError("Erro na chamada da API")

@app.get('/', tags=[home_tag])
def home():

    return redirect('/openapi')
    

@app.get('/consulta-cep', tags=[consulta_tag],
         responses={"200": ListagemConsultaSchema, "404": ErrorSchema})
def consulta(query: ConsultaBuscaSchema):

    cep = request.args.get('cep', '')  # Obter o CEP dos parâmetros da URL

    address = consulta_cep(cep)
    
    return address #render_template('index.html', error=str(e))
    

if __name__ == '__main__':
    app.run(debug=True)
