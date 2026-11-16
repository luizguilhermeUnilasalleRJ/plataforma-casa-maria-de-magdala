Sistema de Gerenciamento — Casa Maria de Magdala

Sistema web desenvolvido como projeto acadêmico da disciplina Projeto Web III, do curso de Sistemas de Informação do Centro Universitário La Salle do Rio de Janeiro (Unilasalle-RJ), em parceria com a instituição Casa Maria de Magdala.

O objetivo é desenvolver uma plataforma para auxiliar a instituição no gerenciamento de pessoas cadastradas, atendimentos, acompanhamentos por especialidade, encaminhamentos, altas e relatórios administrativos.

---

1. Sobre o projeto

A plataforma busca centralizar informações administrativas da instituição, reduzindo a dependência de registros manuais e facilitando a consulta e o acompanhamento dos dados.

O sistema possui uma área restrita, acessível mediante autenticação, destinada aos funcionários autorizados da instituição.

Entre os objetivos estão:

- Centralizar os cadastros de pessoas.
- Registrar e consultar atendimentos.
- Controlar o acompanhamento das pessoas nas diferentes especialidades.
- Registrar datas de início e alta de cada acompanhamento.
- Preservar o histórico de participação nas especialidades.
- Gerar relatórios administrativos e estatísticos.
- Facilitar a consulta de informações da instituição.

2. Tecnologias utilizadas

Tecnologia| Finalidade
Python| Linguagem principal do projeto
Django| Framework de desenvolvimento web
PostgreSQL| Sistema de gerenciamento de banco de dados
HTML5| Estrutura das páginas
CSS3| Estilização e responsividade
JavaScript| Recursos de interação no navegador
Git| Controle de versão
GitHub| Hospedagem do código-fonte

3. Arquitetura do sistema

O projeto utiliza a arquitetura baseada no padrão MVT (Model-View-Template), adotado pelo Django.

A organização é dividida em três componentes principais:

- Models: representam as entidades e os dados armazenados no banco.
- Views: processam as requisições, executam regras de negócio e controlam o fluxo das funcionalidades.
- Templates: apresentam as páginas HTML ao usuário.

O banco de dados PostgreSQL é responsável pelo armazenamento persistente das informações.

4. Funcionalidades do sistema

4.1. Autenticação

- Tela de login.
- Autenticação de usuários.
- Restrição de acesso às páginas administrativas para usuários não autenticados.

4.2. Gerenciamento de pessoas

- Cadastro de pessoas.
- Consulta de cadastros.
- Pesquisa por nome ou CPF.
- Visualização dos detalhes de cada pessoa.
- Edição de informações cadastrais.
- Inativação e reativação de cadastros.
- Filtros por situação do cadastro.

A inativação não exclui os dados da pessoa, permitindo preservar seu histórico.

4.3. Gerenciamento de atendimentos

- Registro individual de cada atendimento.
- Associação do atendimento a uma pessoa cadastrada.
- Registro da data do atendimento.
- Identificação da modalidade presencial ou online.
- Campo para observações.
- Consulta do histórico de atendimentos por pessoa.

Cada atendimento possui seu próprio registro no banco de dados.

4.4. Gerenciamento de especialidades

Funcionalidade planejada para administrar as especialidades oferecidas pela instituição.

A estrutura deverá permitir:

- Cadastro de especialidades.
- Edição das informações.
- Ativação e desativação de especialidades.
- Organização por categorias.

As categorias e especialidades serão baseadas nas informações fornecidas pela instituição.

4.5. Gerenciamento de acompanhamentos

Funcionalidade planejada para controlar a participação de cada pessoa nas especialidades.

Cada acompanhamento deverá possuir:

- Pessoa relacionada.
- Especialidade.
- Data de início.
- Data de alta, quando aplicável.
- Situação do acompanhamento.

Uma pessoa poderá participar de várias especialidades simultaneamente.

Também será permitido retornar a uma especialidade após receber alta. Nesse caso, será criado um novo registro de acompanhamento, preservando o histórico anterior.

4.6. Gerenciamento de encaminhamentos

Módulo sujeito à consolidação das regras operacionais com a instituição.

A estrutura inicialmente considerada prevê que um atendimento possa gerar vários encaminhamentos, cada um relacionado a uma especialidade.

4.7. Relatórios administrativos

Funcionalidade planejada para apresentar informações consolidadas sobre:

- Quantidade de pessoas cadastradas.
- Pessoas ativas e inativas.
- Quantidade de atendimentos.
- Atendimentos presenciais e online.
- Acompanhamentos por especialidade.
- Ingressos e altas.
- Encaminhamentos realizados.

4.8. Exportação de dados

Funcionalidade planejada para permitir a exportação de relatórios em formato Excel (.xlsx).

---

5. Modelagem do banco de dados

O banco de dados utiliza PostgreSQL e possui relacionamentos entre as entidades do sistema.

Entidades principais

Pessoa

Armazena as informações cadastrais das pessoas atendidas pela instituição.

Atendimento

Representa cada atendimento realizado, mantendo a associação com a pessoa correspondente.

Especialidade

Representa as atividades e os serviços disponibilizados pela instituição.

Acompanhamento

Representa o período em que uma pessoa participa de determinada especialidade.

Relacionamentos previstos

- Uma pessoa pode possuir vários atendimentos.
- Uma pessoa pode possuir vários acompanhamentos.
- Uma especialidade pode estar relacionada a vários acompanhamentos.
- Uma pessoa pode possuir vários acompanhamentos da mesma especialidade, em períodos diferentes.
- Um atendimento poderá gerar vários encaminhamentos.

Representação conceitual

Pessoa (1) → (N) Atendimento

Pessoa (1) → (N) Acompanhamento

Especialidade (1) → (N) Acompanhamento

Atendimento (1) → (N) Encaminhamento

---

6. Estrutura de diretórios

A organização geral do projeto segue a estrutura abaixo:

Projeto Web III/
│
├── codigo/
│   └── sistema/
│       │
│       ├── config/
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       │
│       ├── core/
│       │   ├── migrations/
│       │   ├── templates/
│       │   │   ├── pessoas/
│       │   │   ├── atendimentos/
│       │   │   ├── dashboard.html
│       │   │   └── login.html
│       │   │
│       │   ├── static/
│       │   │   └── css/
│       │   │
│       │   ├── admin.py
│       │   ├── forms.py
│       │   ├── models.py
│       │   ├── urls.py
│       │   └── views.py
│       │
│       ├── venv/
│       ├── manage.py
│       └── requirements.txt
│
└── README.md

Observação: a estrutura apresenta a organização geral esperada. Arquivos e diretórios podem variar conforme a evolução do projeto.

---

7. Pré-requisitos

Para executar o projeto localmente, são necessários:

- Python 3.14 ou versão compatível com as dependências instaladas.
- PostgreSQL.
- Git.
- Pip.
- Um navegador atualizado.

O projeto foi desenvolvido utilizando Django 6.1.1 e PostgreSQL.

8. Instalação e configuração

8.1. Clonar o repositório

git clone https://github.com/luizguilhermeUnilasalleRJ/plataforma-casa-maria-de-magdala.git

8.2. Entrar na pasta do projeto

No Git Bash:

cd plataforma-casa-maria-de-magdala/codigo/sistema

8.3. Criar o ambiente virtual

python -m venv venv

8.4. Ativar o ambiente virtual

No Git Bash do Windows:

source venv/Scripts/activate

8.5. Instalar as dependências

pip install -r requirements.txt

8.6. Configurar o PostgreSQL

É necessário possuir uma instância PostgreSQL em execução e criar o banco de dados utilizado pelo sistema.

O projeto utiliza as seguintes configurações locais:

- Banco de dados: "casa_maria_magdala"
- Porta: "2103"
- Driver Python: "psycopg2-binary"

As credenciais e demais parâmetros devem ser configurados de acordo com o arquivo "settings.py" e a configuração local do PostgreSQL.

Não compartilhe credenciais de banco de dados ou arquivos ".env" no repositório.

8.7. Executar as migrações

python manage.py makemigrations
python manage.py migrate

8.8. Criar um usuário administrador

python manage.py createsuperuser

8.9. Iniciar o servidor

python manage.py runserver

O sistema poderá ser acessado pelo endereço:

http://127.0.0.1:8000/

---

9. Verificação do projeto

Para verificar possíveis problemas de configuração:

python manage.py check

Para executar os testes automatizados:

python manage.py test

---

10. Segurança e proteção de dados

Considerando a natureza das informações administradas pela instituição, a segurança é um aspecto fundamental do projeto.

Entre os cuidados previstos estão:

- Autenticação para acesso à área administrativa.
- Restrição de acesso às funcionalidades internas.
- Proteção das operações de alteração por meio de requisições POST e CSRF.
- Validação dos dados enviados pelos formulários.
- Preservação do histórico de atendimentos e acompanhamentos.
- Controle de acesso às informações pessoais.
- Armazenamento seguro das credenciais de acesso ao banco.
- Coleta e utilização apenas das informações necessárias às atividades da instituição.

O desenvolvimento deverá observar os princípios da Lei Geral de Proteção de Dados Pessoais (LGPD — Lei nº 13.709/2018).

---

11. Equipe de desenvolvimento

Projeto desenvolvido por estudantes do curso de Sistemas de Informação do Centro Universitário La Salle do Rio de Janeiro (Unilasalle-RJ), no contexto da disciplina Projeto Web III.

Instituição parceira: Casa Maria de Magdala.

Coordenação acadêmica: Unilasalle-RJ.

---

12. Status do desenvolvimento

O sistema encontra-se em desenvolvimento.

Módulo| Situação
Autenticação| Implementado
Dashboard| Implementado
Cadastro de pessoas| Implementado
Listagem e pesquisa| Implementado
Detalhes de pessoas| Implementado
Edição de cadastros| Implementado
Inativação e reativação| Implementado
Cadastro de atendimentos| Implementado
Histórico de atendimentos| Implementado
Cadastro de especialidades| Planejado
Acompanhamentos| Planejado
Encaminhamentos| Em definição
Altas| Planejado
Relatórios| Planejado
Exportação Excel| Planejado
Testes finais e ajustes visuais| Pendente

---

13. Licença e utilização

Este sistema foi desenvolvido para fins acadêmicos, como parte de um projeto de extensão e desenvolvimento de software em parceria com a Casa Maria de Magdala.

Sua utilização deverá respeitar as finalidades institucionais e as regras de proteção de dados aplicáveis.

---

Projeto Web III — Sistema de Gerenciamento da Casa Maria de Magdala

Centro Universitário La Salle do Rio de Janeiro — Unilasalle-RJ.