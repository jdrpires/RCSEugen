# RCS API

API RESTful para envio e rastreamento de mensagens RCS (Rich Communication Services).

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alto desempenho para construção de APIs com Python
- **PostgreSQL**: Banco de dados relacional robusto
- **SQLAlchemy**: ORM (Object Relational Mapper) para interação com o banco de dados
- **Alembic**: Ferramenta para migrações de banco de dados
- **Pydantic**: Validação de dados e serialização
- **JWT**: Autenticação baseada em tokens
- **Docker**: Containerização da aplicação

## Estrutura do Projeto

```
RCSEugen/
├── alembic/                  # Configurações e scripts de migração
├── app/
│   ├── routers/              # Rotas da API
│   │   ├── __init__.py
│   │   └── rcs.py            # Endpoints RCS
│   ├── __init__.py
│   ├── auth.py               # Autenticação e autorização
│   ├── database.py           # Configuração do banco de dados
│   ├── main.py               # Aplicação principal
│   ├── models.py             # Modelos SQLAlchemy
│   └── schemas.py            # Esquemas Pydantic
├── .env                      # Variáveis de ambiente
├── alembic.ini               # Configuração do Alembic
├── Dockerfile                # Configuração do Docker
├── docker-compose.yml        # Configuração do Docker Compose
├── init_db.py                # Script para inicialização do banco de dados
├── README.md                 # Documentação do projeto
├── requirements.txt          # Dependências do projeto
├── run.py                    # Script para iniciar a aplicação
├── start.sh                  # Script para iniciar os serviços Docker
└── stop.sh                   # Script para parar os serviços Docker
```

## Instalação e Configuração

### Usando Docker (Recomendado)

1. Clone o repositório:
   ```
   git clone <url-do-repositorio>
   cd RCSEugen
   ```

2. Inicie os serviços com Docker:
   ```
   ./start.sh
   ```

3. Acesse a documentação da API:
   ```
   http://localhost:8000/docs
   ```

4. Para parar os serviços:
   ```
   ./stop.sh
   ```

### Instalação Manual

1. Clone o repositório:
   ```
   git clone <url-do-repositorio>
   cd RCSEugen
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o banco de dados PostgreSQL:
   ```
   # Crie um banco de dados chamado rcs_db
   createdb rcs_db
   ```

5. Configure as variáveis de ambiente no arquivo `.env`

6. Execute as migrações:
   ```
   alembic upgrade head
   ```

7. Inicialize o banco de dados com dados de exemplo:
   ```
   python init_db.py
   ```

8. Inicie a aplicação:
   ```
   python run.py
   ```

9. Acesse a documentação da API:
   ```
   http://localhost:8000/docs
   ```

## Endpoints da API

### Envio de RCS

- **URL**: `/v1/rcs/send/`
- **Método**: `POST`
- **Descrição**: Envia mensagens RCS usando um template específico

### Consulta de Eventos

- **URL**: `/v1/rcs/events/`
- **Método**: `GET`
- **Descrição**: Consulta eventos de mensagens RCS com opções de filtragem e paginação

### Consulta de Eventos por ID

- **URL**: `/v1/rcs/events/{callback_message_id}`
- **Método**: `GET`
- **Descrição**: Consulta eventos de uma mensagem RCS específica pelo ID de callback

## Autenticação

A API suporta dois métodos de autenticação:

1. **Token JWT**: Usando o esquema Bearer
2. **API Key**: Usando o esquema ApiKey

Ambos devem ser enviados no cabeçalho `Authorization` das requisições.

## Documentação da API

A documentação completa da API está disponível em:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Dados de Exemplo

Ao inicializar o banco de dados, é criada uma conta de teste com uma API key gerada automaticamente. Esta API key é exibida no console durante a inicialização. Também são criados dois templates de exemplo:

1. **welcome_template**: Template de boas-vindas
2. **promo_template**: Template para promoções
