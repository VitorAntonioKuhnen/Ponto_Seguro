<p align="center">
   <img width="200" src="https://github.com/VitorAntonioKuhnen/Ponto_Seguro/assets/57823410/86441a26-41fc-4eed-b51c-202fc168ed1a" />
</p>

### Ponto Seguro
<hr>

<p align="center">
   <img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=RED&style=for-the-badge" #vitrinedev/>
</p>

### Tópicos 

- [Descrição do projeto](#descrição-do-projeto)

- [Funcionalidades](#funcionalidades)

- [Ferramentas utilizadas](#ferramentas-utilizadas)

- [Acesso ao projeto](#acesso-ao-projeto)

- [Abrir e rodar o projeto](#abrir-e-rodar-o-projeto)

- [Equipe](#equipe)

## Descrição do projeto 

<p align="justify">
 O Projeto em desenvolvimento é para disciplina de Desenvolvimento de Aplicação do curso de Tecnologia em Análise e Desenvolvimento de Sistemas. 
 O Ponto Seguro é um sistema para Gestão de Ponto que serve para controle da marcação do ponto, é um sistema responsável por registrar os horários de entrada, 
  pausa e saída dos funcionários durante todo o mês. Ou seja, é a partir desse sistema que a organização também conseguirá extrair informações como quantidade 
  de horas extras, saldo do banco de horas, quantidades de faltas e atrasos. Dessa forma, o departamento de recursos humanos consegue fechar a folha de pagamento
  dos colaboradores de modo fácil e rápido.
</p>

## Funcionalidades
- Usuário - Operacional

:heavy_check_mark: `Funcionalidade 1:` Realizar o login no sistema.

:heavy_check_mark: `Funcionalidade 2:` Registrar a marcação de ponto, entrada, saída para a pausa, entrada e saída.

- Usuário - RH - Desenvolvedor/TI

:heavy_check_mark: `Funcionalidade 1:` Realizar o login no sistema;

:heavy_check_mark: `Funcionalidade 2:` Realizar cadastro dos usuários, podendo ser todo colaborador da empresa;

:heavy_check_mark: `Funcionalidade 3:` Armazenar dados de registro de ponto do usuário, como as batidas de entrada, saída para pausa, entrada e saída no banco de dados MySQL;

:heavy_check_mark: `Funcionalidade 4:` Cadastrar escalas em grupos com diferentes horários, conforme necessidade  de escala da empresa;

:heavy_check_mark: `Funcionalidade 5:` Exportar histórico de marcação de ponto do colaborador em pdf;

:heavy_check_mark: `Funcionalidade 6:` Aprovar marcação de ponto fora da escala, com a justificativa, que pode ser visualizada e aprovada pelo coordenador responsável daque setor;

:heavy_check_mark: `Funcionalidade 7:` Visualizar e alterar a marcação de ponto, com o propósito de fazer a correção em caso de atestado ou outra justificativa aceitável pela empresa.


## Ferramentas utilizadas

<a href="https://www.mysql.com/products/workbench/" target="_blank"> 
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original-wordmark.svg"alt="MySQL" width="40" height="40"/> 
</a> 

<a href="https://www.python.org/" target="_blank"> 
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" alt="Python" width="40" height="40"/> 
</a> 

<a href="https://www.w3schools.com/js/" target="_blank"> 
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-plain.svg" alt="JavaScript" width="40" height="40"/> 
</a> 

<a href="https://www.w3schools.com/html/" target="_blank"> 
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original-wordmark.svg" alt="HTML5" width="40" height="40"/> 
</a> 

<a href="https://www.w3schools.com/css/" target="_blank"> 
 <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original-wordmark.svg" alt="CSS3" width="40" height="40"/> 
</a> 

<a href="https://www.w3schools.com/django/" target="_blank"> 
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain-wordmark.svg" alt="Django" width="40" height="40"/>
</a>           

<a href="https://getbootstrap.com/docs/5.2/getting-started/introduction/" target="_blank"> 
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-plain-wordmark.svg"  alt="Bootstrap" width="40" height="40" />
</a>            

<a href="https://www.figma.com" target="_blank"> 
 <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg" alt=Figma" width="40" height="40"/>
</a>      
                                                                                                                         
<a href="https://code.visualstudio.com/" target="_blank"> 
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" alt=VsCode" width="40" height="40"/>
</a>                

<a href="https://www.w3schools.com/xml/ajax_intro.asp" target="_blank"> 
  <img src="https://github.com/VitorAntonioKuhnen/Ponto_Seguro/assets/57823410/de0a8bfe-8fbc-4825-9b9d-3e63283372c3" alt=Ajax" width="40" height="40"/>
</a> 
                                                                                                                                                                                                                                                                                                                                                                                       
          
## Acesso ao projeto

Você pode [acessar o código fonte do projeto](https://github.com/VitorAntonioKuhnen/Ponto_Seguro.git) ou [baixá-lo](https://github.com/VitorAntonioKuhnen/Ponto_Seguro/archive/refs/heads/Back.zip).

## Abrir e rodar o projeto

Após baixar o projeto, você pode abrir com a IDE de sua preferência (IDE usado no projeto VsCode) ou clonar o projeto direto do GitHab.

* Para clonar o projeto na sua máquina:
- Com o Git Bash instalado na sua máquina, clica com o direito do mouse na área de trabalho e selecione Git Bash Here (Irá abrir um terminal no PC) e digite o seguinte comando:
~~~
git clone -b Back https://github.com/VitorAntonioKuhnen/Ponto_Seguro.git
~~~ 
* Para baixar o projeto na sua máquina
* Procure o local onde o projeto está e o selecione (Caso o projeto seja baixado via zip, é necessário extraí-lo antes de procurá-lo);
* Abra o codigo na IDE VsCode
* Após abrir o projeto no VsCode, criar uma pasta na raiz no projeto com o nome **.env** para ter as variaveis de segurança do sistema.
* Dentro desse arquivo coloque essas variaveis:
~~~
SECRET_KEY = 'django-insecure-b(w!7eilg8r$)9rwqk6xmy1!1tptn_%ze)_9ba7m)g7%r*w3$)'

RECAPTCHA_PUBLIC_KEY = 'chave publica do recaptcha'
RECAPTCHA_PRIVATE_KEY = 'chave privada do recaptcha'


Email = 'email do admin cadastrado'
SenhaApp = 'senha do admin'
email_tls = 'Se for verdadeiro, usar true'
email_port = 'senha do email que manda os email'
email_host = 'email que vai ser usado para mandar os email'


ENGINE = 'motor do banco de dados'
NAME = 'nome do banco de dado'
USER = 'Usuário com o acesso a todo o sistema - admin'
PASSWORD = 'senha do banco dado'
HOST ='host do banco dado'
PORT = '3306'
ssl = '{'require_secure_transport': <False ou True}'
                                                                                                                                                     
TOKEK 'Token da APi de feriado site: https://api.invertexto.com/api-feriados'
ESTADOUF = 'SC'                                                                                                                                                                                                         
~~~
 
*Após inserir as variáveis de segurança do sistema, abra o cmd (command prompt) e crie um venv (ambiente virtual do python) para criar a venv digite esse comando:

~~~
python -m venv venv
~~~

* Comando para iniciar a venv (ativar o ambiente virtual):

~~~
.\venv\Scripts\activate
~~~

* Após ativar o ambiente virtual, na raiz do projeto, tem um arquivo chamado requirements.txt (onde tem todas as dependências do projetos)                                                                                   
* Para baixar as dependências tem que executar esse comando, porém tem q estar na venv (dentro do ambiente virtual), digite o comando para instalar o requeriments.txt.
                                                                                                                                                     
~~~
pip install -r requirements.txt
~~~

* Após instalar os arquivos requirents.txt, digite o comando a seguir para iniciar o servidor:

~~~
python manage.py runserver
~~~

* Vai ser exebido no terminal um link http, copie e cole no seu navegador  🏆 
##  Equipe

| [<img src="https://github.com/VitorAntonioKuhnen/Ponto_Seguro/assets/57823410/e6baf733-104b-4e92-985d-1e230ff5db61" height=120 width=115><br><sub>Marcello Henrique A. Nunes</sub>](https://github.com/MarcelloAbreu) |  [<img src="https://github.com/VitorAntonioKuhnen/Ponto_Seguro/assets/57823410/b493e984-0d6d-439c-92d1-47abab27eb84" height=120 width=115><br><sub>Maria Artemisia D. Sousa</sub>](https://github.com/ArtemisiaDutra)  | 
| :---: | :---: 
| [<img src="https://github.com/VitorAntonioKuhnen/Ponto_Seguro/assets/57823410/002bf449-df9c-4b4a-ace4-e2566f8234bc" height=120 width=115><br><sub>Vinicius M. Schutz</sub>](https://github.com/vinicius-schutz) |  [<img src="https://github.com/VitorAntonioKuhnen/Ponto_Seguro/assets/57823410/7c5a459e-0aa4-4fc7-9cac-3110fa4632a8" height=120 width=115><br><sub>Vítor Antônio Kuhnen</sub>](https://github.com/VitorAntonioKuhnen)  | 


