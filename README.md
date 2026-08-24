# Plataforma Casa Maria de Magdala

## Descrição do Projeto

A **Plataforma Casa Maria de Magdala** é um projeto acadêmico desenvolvido com o objetivo de apoiar as atividades da Casa Maria de Magdala, organização que atua na área de HIV/AIDS.

O projeto será composto por um **site institucional**, voltado à divulgação de informações, conscientização e orientação sobre HIV/AIDS, e por um **sistema interno de gerenciamento**, destinado ao apoio das atividades administrativas e dos atendimentos realizados pela organização.

A plataforma busca centralizar informações e facilitar a organização das atividades da instituição por meio de uma solução digital simples, acessível e organizada.

## Objetivos

* Desenvolver um site institucional para a Casa Maria de Magdala;
* Disponibilizar informações educativas sobre HIV/AIDS;
* Facilitar o acesso a informações de prevenção e apoio;
* Desenvolver um sistema para auxiliar no gerenciamento das atividades da organização;
* Aplicar conhecimentos de desenvolvimento web, programação e banco de dados;
* Desenvolver uma solução tecnológica adequada às necessidades apresentadas pela organização.

## Tecnologias Utilizadas

### Site

* HTML5
* CSS3
* JavaScript

### Sistema

* Python
* Flask
* SQLAlchemy

### Banco de Dados

* PostgreSQL

### Ferramentas

* Git
* GitHub

## Estrutura do Projeto

```text
Projeto Web III/
│
├── README.md
│
├── codigo/
│   ├── site/
│   └── sistema/
│
├── banco-de-dados/
│
└── evidencias/
```

### `codigo/`

Contém os códigos-fonte do projeto, separados entre o site institucional e o sistema interno.

### `banco-de-dados/`

Contém os arquivos utilizados para criação e configuração do banco de dados.

### `evidencias/`

Contém registros do desenvolvimento do projeto, como capturas de tela, diagramas e materiais relacionados à apresentação.

## Instruções de Uso

### Pré-requisitos

Para executar o projeto, será necessário ter instalado:

* Python 3.x
* PostgreSQL
* Git

### Instalação

Clone o repositório:

```bash
git clone https://github.com/luizguilhermeUnilasalleRJ/plataforma-casa-maria-de-magdala.git
```

Entre na pasta do projeto:

```bash
cd "Projeto Web III"
```

Crie um ambiente virtual Python:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### Banco de Dados

Após configurar o PostgreSQL, execute os scripts disponíveis na pasta:

```text
banco-de-dados/
```

As informações de conexão com o banco deverão ser configuradas de acordo com o ambiente de execução.

### Execução

Após a instalação das dependências e configuração do banco de dados, execute a aplicação Python:

```bash
python codigo/sistema/app.py
```

O endereço de acesso à aplicação será informado pelo Flask no terminal.

## Equipe

Projeto desenvolvido pelos alunos do curso de **Sistemas de Informação – UNILASALLE-RJ**.

## Projeto Acadêmico

Este projeto foi desenvolvido como parte das atividades acadêmicas da disciplina **Projeto Web III**.
