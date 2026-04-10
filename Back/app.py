from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from logger import logger
from schemas import *
from flask_cors import CORS

# Importa função que configura tudo
from endpoints import configure_all_endpoints

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo a tag
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

configure_all_endpoints(app)

# Bloco de execução
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




