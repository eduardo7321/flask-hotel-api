# REST API de Hotéis com Python

Este repositório contém o código de uma REST API para gerenciamento de hotéis, construída com boas práticas de desenvolvimento de Webservices. A aplicação foi desenvolvida utilizando **Python** e segue os princípios do REST, com funcionalidades que vão desde o armazenamento básico em memória até integração com banco de dados e autenticação de usuários.
Realizei esse projeto acompanhando o curso do professor Danilo Moreira na udemy, implementando minhas melhorias.

## Funcionalidades

- **Gerenciamento de Hotéis**: Cadastro, consulta, atualização e remoção de hotéis.
- **Armazenamento de Dados**: Inicialmente, os dados são armazenados em memória, evoluindo para uma integração com banco de dados.
- **Autenticação de Usuários**: Implementação de funcionalidades como cadastro, login e logout de usuários utilizando JWT.
- **Filtros Avançados de Consultas**: Permite consultas personalizadas para listar hotéis com base em parâmetros específicos.

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
`git clone https://github.com/seu-usuario/nome-do-repositorio.git`
`cd nome-do-repositorio`
```

### 2. Criar e ativar um ambiente virtual

```bash
`python virtualenv ambvir` #ambvir é o nome do ambiente virtual,fica ao seu critério
`source venv/bin/activate`  # No Windows: venv\Scripts\activate` `
```

### 3. Instalar as dependências

```bash
`pip install -r requirements.txt`
```

### 4. Executar a aplicação

```bash
`python app.py`
```

### 5. Testar a API

Você pode usar um cliente HTTP, como [Postman](https://www.postman.com/) ou `curl`, para testar as rotas da API.

## Tecnologias Utilizadas

- **Python**
- **Flask** (ou outro framework de sua escolha)
- **SQLite/PostgreSQL** para persistência de dados
- **JWT** para autenticação de usuários

## Estrutura do Projeto

```bash
├── app.py               # Arquivo principal da aplicação
├── models/              # Modelos de dados
├── routes/              # Definição de rotas da API
├── services/            # Serviços e regras de negócios
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação do projeto`
```

## Próximos Passos

- Implementação de testes automatizados.
- Melhorias na documentação e exemplos de uso.
- Otimização de consultas e performance.
