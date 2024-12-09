# API - Consumo de Mensagens

## Descrição

Esta API é um serviço responsável por consumir mensagens de filas de processamento assíncrono utilizando RabbitMQ. Ela está configurada para processar dois tipos principais de mensagens: SMS e E-mail. A API se conecta ao RabbitMQ, consome as mensagens de duas filas distintas (uma para SMS e outra para E-mail) e realiza o envio real das mensagens. A lógica de envio das mensagens (por SMS ou E-mail) é executada diretamente na API de consumo, que integra com serviços externos como o Twilio para SMS e servidores SMTP para E-mail. Ao iniciar o serviço, ele fica ouvindo as filas do RabbitMQ de forma contínua e assíncrona, consumindo as mensagens assim que elas chegam nas filas configuradas.

## Funcionalidades

- **Consumo de Mensagens:** A API consome mensagens em duas filas: sms_queue e email_queue, processando mensagens de SMS e e-mail, respectivamente.
- **Envio de SMS:** Quando uma mensagem de SMS é consumida da fila, a API utiliza o serviço Twilio para enviar o SMS para o número indicado.
- **Envio de E-mail** Quando uma mensagem de e-mail é consumida da fila, a API envia o e-mail utilizando um servidor SMTP configurado.

## Estrutura do Projeto

```plaintext
api-message-consumer/
├── app/
│   ├── services/
│   │   └── message_consumer_service.py
│   └── main.py
├── .gitignore
├── Dockerfile
├── README.md
├── docker-compose.yml
└── pyproject.toml
```

## Como Usar

1- Clone este repositório:
   ```bash
   git clone https://github.com/lazzarusxd/api-message-consumer.git
   ```


2- Navegue até o diretório do projeto:
   ```bash
   cd api-message-consumer
   ```


3- Configure o arquivo ".env":
- Crie um arquivo ".env" na raiz do projeto, contendo as váriaveis necessárias:
   ```bash
    RABBITMQ_DEFAULT_USER=seu_user
    RABBITMQ_DEFAULT_PASS=sua_senha
    RABBITMQ_HOST=container_rabbitmq
    RABBITMQ_PORT=porta_rabbitmq
    TWILIO_SID=sua_twilio_sid
    TWILIO_AUTH_TOKEN=sua_twilio_auth_token
    TWILIO_PHONE_NUMBER=seu_numero_twilio
    SMTP_USER=seu_usuario_smtp
    SMTP_PASSWORD=sua_senha_smtp
    SMTP_HOST=servidor_smtp
    SMTP_PORT=porta_smtp
   ```


4- Crie seu ambiente de desenvolvimento e instale as dependências usando Poetry:
   ```bash
   poetry install
   ```


5- Execute seu ambiente de desenvolvimento com as dependências usando Poetry:
   ```bash
   poetry shell
   ```


6- Configure o interpretador Python na sua IDE:
- Caso seu ambiente de desenvolvimento tenha sido criado no WSL, selecione-o e escolha a opção "System Interpreter".
  
- Navegue até o diretório retornado no terminal após a execução do comando do Passo 5.
  
- Procure o executável do Python dentro do ambiente virtual.


7- Crie e execute os containers Docker necessários:
   ```bash
   docker-compose up --build
   ```


8- Assim que o container for executado, a API começará a consumir as mensagens das filas do RabbitMQ automaticamente. O serviço ficará rodando em um loop contínuo, aguardando novas mensagens nas filas configuradas.


### **Logs**:

- **Logs de Consumo de Mensagens**: Durante a execução, a API irá imprimir mensagens de log no terminal, indicando quando começou o consumo de mensagens, quando um SMS ou e-mail foi enviado com sucesso, ou se houve algum erro ao tentar consumir ou enviar a mensagem.
- **Erros**: Caso ocorra algum erro na conexão com o RabbitMQ ou no envio de mensagens, os logs de erro serão exibidos no terminal.


### **Possíveis Erros**:

- ***500***: Erro interno do servidor.

## Contato:

João Lázaro - joaolazarofera@gmail.com

Link do projeto - https://github.com/lazzarusxd/api-message-consumer
