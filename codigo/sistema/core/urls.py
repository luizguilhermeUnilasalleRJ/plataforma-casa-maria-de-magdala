from os import name

from django.urls import path

from .views import (
    login_view,
    dashboard,
    cadastrar_pessoa,
    listar_pessoas,
    detalhes_pessoa,
    alterar_cadastro,
    alterar_status_pessoa,
    cadastrar_atendimento,
    cadastrar_acompanhamento,
    solicitar_cadastro,
    solicitacao_enviada,
    listar_solicitacoes, detalhes_solicitacao,
    aprovar_solicitacao, recusar_solicitacao
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),

    path('pessoas/cadastrar/', cadastrar_pessoa, name='cadastrar_pessoa'),
    path('pessoas/', listar_pessoas, name='listar_pessoas'),
    path('pessoas/<int:pessoa_id>/', detalhes_pessoa, name='detalhes_pessoa'),
    path('pessoas/<int:pessoa_id>/editar/', alterar_cadastro, name='editar_pessoa'),
    path('pessoas/<int:pessoa_id>/status/', alterar_status_pessoa, name='alterar_status_pessoa'),

    path('atendimentos/cadastrar/', cadastrar_atendimento, name='cadastrar_atendimento'),
    path('acompanhamentos/cadastrar/', cadastrar_acompanhamento, name='cadastrar_acompanhamento'),

    path('solicitar-cadastro/', solicitar_cadastro, name='solicitar_cadastro'),
    path('solicitacao-enviada/', solicitacao_enviada, name='solicitacao_enviada'),
    path('solicitacoes/', listar_solicitacoes, name= 'listar_solicitacoes'),
    path('solicitacoes/<int:solicitacao_id>/',detalhes_solicitacao, name= 'detalhes_solicitacao'),
    path('solicitacoes/<int:solicitacao_id>/aprovar/',aprovar_solicitacao, name= 'aprovar_solicitacao'),
    path('solicitacoes/<int:solicitacao_id>/recusar/', recusar_solicitacao, name = 'recusar_solicitacao'),
]