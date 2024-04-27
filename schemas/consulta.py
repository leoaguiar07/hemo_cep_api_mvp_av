from pydantic import BaseModel

class ListagemConsultaSchema(BaseModel):
    
    bairro: str = "Sé"
    cep: str = "01001000"
    cidade: str = "São Paulo"
    logradouro: str = "Praça da Sé"
    uf: str = "SP"

class ConsultaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da consulta.
    """

    cep: str = "cep"