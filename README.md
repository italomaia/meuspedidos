Aplicativo para recebimento de inscrições de candidatos interessados
em trabalhar na empresa meuspedidos.

Instalando
==========
O aplicativo está configurado para ser colocado em deploy no Heroku.
Basta enviar o código para um repositório do Heroku, configurar
as variáveis de ambiente (SECRET_KEY e SENDGRID_PASSWD) e pronto.

Para testar o aplicativo local, faça o seguinte:

Certifique-se de que o python-dev está instalado:

    sudo apt-get install python-dev

Instale as dependências:

    pip install -r requirements.txt

Crie o banco de dados:
    
    python manage.py migrate

E pronto ; )

Testando
========
Para testar, certifique-se de que tox está instalado:

    sudo pip install tox

e rode o camando:

    tox
