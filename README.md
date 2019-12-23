# Loja de Computadores

Sistema Loja com controle de montagem de computadores pelo cliente.

# Iniciando
### Instale as dependencias
```
    pip install -r requirements.txt
```

### Definir as seguintes variáveis no ambiente
```
SECRET_KEY # Chave de criptografia do django
DEBUG # Aplicacao iniciará em modo de debug ("True", "False")
DATABASE_URL # URL de acesso ao banco de dados
```

### Prepare o banco para a aplicação
```
    python manage.py migrate
```

### Crie um usuário para gerenciar o sistema através do comando
```
    python manage.py createsuperuser
```

### Iniciando a aplicação
```
    python manage.py runserver
```

# Administração
O cadastro de usuários e produtos é feito pela administração.
Também é possível cadastrar uma montagem pela administração.

### /admin
Acesso a administração

# API do Sistema
## Produtos
Os produtos são cadastrados pela administração e são listados a seguir.

### /api/processadores/
Lista os Processadores
```
[
    {
        "url": "http://localhost:8000/api/processadores/1/",
        "descricao": "Processador Intel Core i5",
        "marca": "intel"
    }
]
```

### /api/placas-maes/
Lista as placas mães
```
[
    {
        "url": "http://localhost:8000/api/placas-maes/1/",
        "descricao": "Placa Mãe Asus Prime",
        "slots_memoria": 2,
        "memoria_suportaca": 16,
        "video_integrado": false,
        "processadores_suportados": [
            "http://localhost:8000/api/processadores/1/",
            "http://localhost:8000/api/processadores/2/"
        ]
    }
]
```

### /api/memorias-ram/
Lista as memórias RAM
```
[
    {
        "url": "http://localhost:8000/api/memorias-ram/1/",
        "descricao": "Hiper X",
        "tamanho": 4
    }
]
```

### /api/placas-de-video/
Lista as placas de vídeo
```
[
    {
        "url": "http://localhost:8000/api/placas-de-video/1/",
        "descricao": "Placa de Video Gigabyte Geforce GTX 1060 6GB"
    }
]
```

## Usuários
Os todos os clientes são usuários do sistema, os usuários são cadastrados pela administração

### /api/usuario/
Lista os usuários
```
[
    {
        "url": "http://localhost:8000/api/usuario/1/",
        "username": "rian",
        "first_name": "Felipe",
        "last_name": "Rian",
        "email": "feliperian@gmail.com"
    }
]
```

## Montagem
O computador pode ser montado e listado pela API ou pela administração

### /api/computador/
Lista a monstagem de computadores

#### GET
```
[
    {
        "url": "http://localhost:8000/api/computador/2/",
        "memoria": [
            {
                "url": "http://localhost:8000/api/computador-memoria/17/",
                "memoria": "http://localhost:8000/api/memorias-ram/3/"
            }
        ],
        "cliente": "http://localhost:8000/api/usuario/1/",
        "processador": "http://localhost:8000/api/processadores/1/",
        "placa_mae": "http://localhost:8000/api/placas-maes/1/",
        "placa_video": "http://localhost:8000/api/placas-de-video/1/"
    }
]
```

#### POST
Exemplo de uma requisição de montagem de um computador:
##### Enviado:
```
{
    "memoria": [
        {
            "memoria": "http://localhost:8000/api/memorias-ram/2/"
        },
        {
            "memoria": "http://localhost:8000/api/memorias-ram/2/"
        }
    ],
    "cliente": "http://localhost:8000/api/usuario/1/",
    "processador": "http://localhost:8000/api/processadores/1/",
    "placa_mae": "http://localhost:8000/api/placas-maes/1/",
    "placa_video": "http://localhost:8000/api/placas-de-video/2/"
}
```
##### Retorno 201:
```
{
    "url": "http://localhost:8000/api/computador/1/",
    "memoria": [
        {
            "url": "http://localhost:8000/api/computador-memoria/11/",
            "memoria": "http://localhost:8000/api/memorias-ram/2/"
        },
        {
            "url": "http://localhost:8000/api/computador-memoria/12/",
            "memoria": "http://localhost:8000/api/memorias-ram/2/"
        }
    ],
    "cliente": "http://localhost:8000/api/usuario/1/",
    "processador": "http://localhost:8000/api/processadores/1/",
    "placa_mae": "http://localhost:8000/api/placas-maes/1/",
    "placa_video": "http://localhost:8000/api/placas-de-video/2/"
}
```

### /api/computador/verbose/
Lista os pedidos de montagem de computadores com informações verbosas
```
[
    {
        "id": 2,
        "memoria": [
            "Hiper X 16 GB"
        ],
        "cliente": "rian",
        "processador": "Processador Intel Core i5",
        "placa_mae": "Placa Mãe Asus Prime",
        "placa_video": "Placa de Video Gigabyte Geforce GTX 1060 6GB"
    }
]
```

### /api/computador-memoria/
Lista os controles de vinculo das memórias com os computadores montados
```
[
    {
        "url": "http://localhost:8000/api/computador-memoria/11/",
        "memoria": "http://localhost:8000/api/memorias-ram/2/"
    }
]
```
