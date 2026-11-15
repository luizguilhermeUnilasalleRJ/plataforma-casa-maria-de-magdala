from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from io import BytesIO
import base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from openpyxl import Workbook
from docx import Document

from .forms import (
    PessoaForm,
    AtendimentoForm,
    AcompanhamentoForm,
    SolicitacaoCadastroForm
)

from .models import (
    Pessoa,
    Atendimento,
    Especialidades,
    Acompanhamento,
    SolicitacaoCadastro
)


# =====================================================
# DASHBOARD
# =====================================================

@login_required
def dashboard(request):
    indicadores = {
        'total_pessoas': Pessoa.objects.count(),
        'pessoas_ativas': Pessoa.objects.filter(ativo=True).count(),
        'total_atendimentos': Atendimento.objects.count(),
        'solicitacoes_pendentes': SolicitacaoCadastro.objects.filter(
            status='pendente'
        ).count(),
    }

    return render(
        request,
        'dashboard.html',
        {'indicadores': indicadores}
    )


# =====================================================
# LOGIN
# =====================================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            return redirect('/dashboard/')

        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')


# =====================================================
# SOLICITAÇÃO PÚBLICA DE CADASTRO
# =====================================================

def solicitar_cadastro(request):
    if request.method == 'POST':
        form = SolicitacaoCadastroForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('solicitacao_enviada')

    else:
        form = SolicitacaoCadastroForm()

    return render(
        request,
        'solicitacoes/cadastro.html',
        {'form': form}
    )


def solicitacao_enviada(request):
    return render(
        request,
        'solicitacoes/confirmacao.html'
    )


# =====================================================
# CADASTRO DE PESSOAS
# =====================================================

@login_required
def cadastrar_pessoa(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Pessoa cadastrada com sucesso!'
            )

            return redirect('cadastrar_pessoa')

    else:
        form = PessoaForm()

    return render(
        request,
        'pessoas/cadastro.html',
        {'form': form}
    )


@login_required
def listar_pessoas(request):
    pesquisa = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'ativos')

    pessoas = Pessoa.objects.all()

    if status == 'ativos':
        pessoas = pessoas.filter(ativo=True)

    elif status == 'inativos':
        pessoas = pessoas.filter(ativo=False)

    if pesquisa:
        pessoas = pessoas.filter(
            Q(nome__icontains=pesquisa) |
            Q(cpf__icontains=pesquisa)
        )

    pessoas = pessoas.order_by('nome')

    return render(
        request,
        'pessoas/lista.html',
        {
            'pessoas': pessoas,
            'pesquisa': pesquisa,
            'status': status,
        }
    )


@login_required
def detalhes_pessoa(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)

    atendimentos = pessoa.atendimentos.order_by(
        '-data_atendimento',
        '-id'
    )

    acompanhamentos = pessoa.acompanhamentos.select_related(
        'especialidades'
    ).order_by(
        '-data_inicio',
        '-id'
    )

    return render(
        request,
        'pessoas/detalhes.html',
        {
            'pessoa': pessoa,
            'atendimentos': atendimentos,
            'acompanhamentos': acompanhamentos,
        }
    )


@login_required
def alterar_cadastro(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)

    if request.method == 'POST':
        form = PessoaForm(request.POST, instance=pessoa)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Cadastro atualizado com sucesso!'
            )

            return redirect(
                'detalhes_pessoa',
                pessoa_id=pessoa.id
            )

    else:
        form = PessoaForm(instance=pessoa)

    return render(
        request,
        'pessoas/cadastro.html',
        {'form': form}
    )


@login_required
@require_POST
def alterar_status_pessoa(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)

    pessoa.ativo = not pessoa.ativo
    pessoa.save()

    if pessoa.ativo:
        messages.success(request, 'Cadastro reativado com sucesso!')
    else:
        messages.success(request, 'Cadastro inativado com sucesso!')

    return redirect(
        'detalhes_pessoa',
        pessoa_id=pessoa.id
    )


# =====================================================
# CADASTRO DE ATENDIMENTOS
# =====================================================

@login_required
def cadastrar_atendimento(request, pessoa_id=None):
    pessoa = None

    if pessoa_id is not None:
        pessoa = get_object_or_404(
            Pessoa,
            id=pessoa_id,
            ativo=True
        )

    form = AtendimentoForm(
        request.POST or None,
        initial={'pessoa': pessoa} if pessoa else None
    )

    form.fields['pessoa'].queryset = Pessoa.objects.filter(
        ativo=True
    ).order_by('nome')

    if request.method == 'POST':
        if form.is_valid():
            atendimento = form.save()

            messages.success(
                request,
                'Atendimento cadastrado com sucesso!'
            )

            return redirect(
                'detalhes_pessoa',
                pessoa_id=atendimento.pessoa.id
            )

    return render(
        request,
        'atendimentos/cadastrar.html',
        {'form': form}
    )


# =====================================================
# EDIÇÃO DE ATENDIMENTOS
# =====================================================

@login_required
def editar_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(
        Atendimento,
        id=atendimento_id
    )

    form = AtendimentoForm(
        request.POST or None,
        instance=atendimento
    )

    form.fields['pessoa'].queryset = Pessoa.objects.filter(
        Q(ativo=True) | Q(pk=atendimento.pessoa_id)
    ).order_by('nome')

    if request.method == 'POST':
        if form.is_valid():
            atendimento_atualizado = form.save()

            messages.success(
                request,
                'Atendimento atualizado com sucesso!'
            )

            return redirect(
                'detalhes_pessoa',
                pessoa_id=atendimento_atualizado.pessoa.id
            )

    return render(
        request,
        'atendimentos/cadastrar.html',
        {
            'form': form,
            'edicao': True,
        }
    )


# =====================================================
# CADASTRO DE ACOMPANHAMENTOS
# =====================================================

@login_required
def cadastrar_acompanhamento(request, pessoa_id=None):
    pessoa = None

    if pessoa_id is not None:
        pessoa = get_object_or_404(
            Pessoa,
            id=pessoa_id,
            ativo=True
        )

    form = AcompanhamentoForm(
        request.POST or None,
        initial={'pessoa': pessoa} if pessoa else None
    )

    form.fields['pessoa'].queryset = Pessoa.objects.filter(
        ativo=True
    ).order_by('nome')

    form.fields['especialidades'].queryset = Especialidades.objects.filter(
        ativa=True
    ).order_by('nome')

    if request.method == 'POST':
        if form.is_valid():
            acompanhamento = form.save()

            messages.success(
                request,
                'Acompanhamento cadastrado com sucesso.'
            )

            return redirect(
                'detalhes_pessoa',
                pessoa_id=acompanhamento.pessoa.id
            )

    return render(
        request,
        'acompanhamentos/cadastrar.html',
        {'form': form}
    )


# =====================================================
# EDIÇÃO DE ACOMPANHAMENTOS
# =====================================================

@login_required
def editar_acompanhamento(request, acompanhamento_id):
    acompanhamento = get_object_or_404(
        Acompanhamento,
        id=acompanhamento_id
    )

    form = AcompanhamentoForm(
        request.POST or None,
        instance=acompanhamento
    )

    form.fields['pessoa'].queryset = Pessoa.objects.filter(
        Q(ativo=True) | Q(pk=acompanhamento.pessoa_id)
    ).order_by('nome')

    form.fields['especialidades'].queryset = Especialidades.objects.filter(
        Q(ativa=True) | Q(pk=acompanhamento.especialidades_id)
    ).order_by('nome')

    if request.method == 'POST':
        if form.is_valid():
            acompanhamento_atualizado = form.save()

            messages.success(
                request,
                'Acompanhamento atualizado com sucesso!'
            )

            return redirect(
                'detalhes_pessoa',
                pessoa_id=acompanhamento_atualizado.pessoa.id
            )

    return render(
        request,
        'acompanhamentos/cadastrar.html',
        {
            'form': form,
            'edicao': True,
        }
    )


# =====================================================
# SOLICITAÇÕES DE CADASTRO
# =====================================================

@login_required
def listar_solicitacoes(request):
    solicitacoes = SolicitacaoCadastro.objects.filter(
        status='pendente'
    ).order_by('-data_solicitacao')

    return render(
        request,
        'solicitacoes/lista.html',
        {'solicitacoes': solicitacoes}
    )


@login_required
def detalhes_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(
        SolicitacaoCadastro,
        id=solicitacao_id
    )

    return render(
        request,
        'solicitacoes/detalhes.html',
        {'solicitacao': solicitacao}
    )


@login_required
@require_POST
def aprovar_solicitacao(request, solicitacao_id):
    with transaction.atomic():
        solicitacao = get_object_or_404(
            SolicitacaoCadastro.objects.select_for_update(),
            id=solicitacao_id
        )

        if solicitacao.status != 'pendente':
            messages.error(
                request,
                'Esta solicitação já foi analisada.'
            )

            return redirect(
                'detalhes_solicitacao',
                solicitacao_id=solicitacao.id
            )

        if Pessoa.objects.filter(cpf=solicitacao.cpf).exists():
            messages.error(
                request,
                'Já existe uma pessoa cadastrada com este CPF.'
            )

            return redirect(
                'detalhes_solicitacao',
                solicitacao_id=solicitacao.id
            )

        Pessoa.objects.create(
            nome=solicitacao.nome,
            data_nascimento=solicitacao.data_nascimento,
            cpf=solicitacao.cpf,
            telefone=solicitacao.telefone,
            email=solicitacao.email,
            nome_responsavel=solicitacao.nome_responsavel,
            estado_civil=solicitacao.get_estado_civil_display(),
            endereco=solicitacao.endereco,
            data_entrada=timezone.localdate(),
            origem_cadastro='online',
        )

        solicitacao.status = 'aprovada'
        solicitacao.save(update_fields=['status'])

    messages.success(
        request,
        'Solicitação aprovada e pessoa cadastrada com sucesso!'
    )

    return redirect('listar_solicitacoes')


@login_required
@require_POST
def recusar_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(
        SolicitacaoCadastro,
        id=solicitacao_id
    )

    if solicitacao.status != 'pendente':
        messages.error(
            request,
            'Esta solicitação já foi analisada.'
        )

        return redirect(
            'detalhes_solicitacao',
            solicitacao_id=solicitacao.id
        )

    solicitacao.status = 'recusada'
    solicitacao.save(update_fields=['status'])

    messages.success(
        request,
        'Solicitação recusada com sucesso.'
    )

    return redirect('listar_solicitacoes')


# =====================================================
# EXPORTAÇÃO DE RELATÓRIOS
# =====================================================

@login_required
def exportar_dados(request):
    formato = request.GET.get('formato')

    if formato not in ['excel', 'word']:
        messages.error(request, 'Formato de exportação inválido.')
        return redirect('dashboard')

    if request.method == 'POST':
        selecionados = request.POST.getlist('dados')

        if not selecionados:
            messages.error(
                request,
                'Selecione pelo menos uma categoria para exportar.'
            )
            return redirect(f"{request.path}?formato={formato}")

        if formato == 'excel':
            return gerar_excel(selecionados)

        return gerar_word(selecionados)

    return render(
        request,
        'relatorios/exportar.html',
        {'formato': formato}
    )


# =====================================================
# GERAÇÃO DE EXCEL
# =====================================================

def gerar_excel(selecionados):
    arquivo = Workbook()
    arquivo.remove(arquivo.active)

    if 'pessoas' in selecionados:
        planilha = arquivo.create_sheet('Pessoas')

        planilha.append([
            'Nome',
            'Data de nascimento',
            'CPF',
            'Telefone',
            'E-mail',
            'Estado civil',
            'Data de entrada',
            'Origem do cadastro',
            'Situação'
        ])

        for pessoa in Pessoa.objects.all().order_by('nome'):
            planilha.append([
                pessoa.nome,
                pessoa.data_nascimento,
                pessoa.cpf,
                pessoa.telefone,
                pessoa.email,
                pessoa.estado_civil,
                pessoa.data_entrada,
                pessoa.origem_cadastro,
                'Ativa' if pessoa.ativo else 'Inativa'
            ])

    if 'atendimentos' in selecionados:
        planilha = arquivo.create_sheet('Atendimentos')

        planilha.append([
            'Pessoa',
            'Data do atendimento',
            'Modalidade'
        ])

        atendimentos = Atendimento.objects.select_related(
            'pessoa'
        ).order_by('-data_atendimento')

        for atendimento in atendimentos:
            planilha.append([
                atendimento.pessoa.nome,
                atendimento.data_atendimento,
                atendimento.get_modalidade_display()
            ])

    if 'acompanhamentos' in selecionados:
        planilha = arquivo.create_sheet('Acompanhamentos')

        planilha.append([
            'Pessoa',
            'Especialidade',
            'Data de início',
            'Alta prevista',
            'Data da alta',
            'Situação'
        ])

        acompanhamentos = Acompanhamento.objects.select_related(
            'pessoa',
            'especialidades'
        ).order_by('-data_inicio')

        for acompanhamento in acompanhamentos:
            planilha.append([
                acompanhamento.pessoa.nome,
                acompanhamento.especialidades.nome,
                acompanhamento.data_inicio,
                acompanhamento.data_alta_prevista,
                acompanhamento.data_alta,
                acompanhamento.status
            ])

    if 'altas' in selecionados:
        planilha = arquivo.create_sheet('Altas')

        planilha.append([
            'Pessoa',
            'Especialidade',
            'Data de início',
            'Data da alta'
        ])

        altas = Acompanhamento.objects.filter(
            data_alta__isnull=False
        ).select_related(
            'pessoa',
            'especialidades'
        ).order_by('-data_alta')

        for alta in altas:
            planilha.append([
                alta.pessoa.nome,
                alta.especialidades.nome,
                alta.data_inicio,
                alta.data_alta
            ])

    for planilha in arquivo.worksheets:
        for coluna in planilha.columns:
            maior_largura = max(
                len(str(celula.value or ''))
                for celula in coluna
            )

            letra = coluna[0].column_letter

            planilha.column_dimensions[letra].width = min(
                maior_largura + 3,
                40
            )

    buffer = BytesIO()
    arquivo.save(buffer)
    buffer.seek(0)

    resposta = HttpResponse(
        buffer.getvalue(),
        content_type=(
            'application/vnd.openxmlformats-officedocument.'
            'spreadsheetml.sheet'
        )
    )

    resposta['Content-Disposition'] = (
        'attachment; filename="relatorio_magdala.xlsx"'
    )

    return resposta


# =====================================================
# GERAÇÃO DE WORD
# =====================================================

def gerar_word(selecionados):
    documento = Document()

    documento.add_heading(
        'Relatório — Casa Maria de Magdala',
        level=0
    )

    documento.add_paragraph(
        f'Data de geração: {timezone.localdate().strftime("%d/%m/%Y")}'
    )

    if 'pessoas' in selecionados:
        documento.add_heading('Pessoas cadastradas', level=1)

        tabela = documento.add_table(rows=1, cols=5)
        tabela.style = 'Table Grid'

        cabecalho = tabela.rows[0].cells

        for celula, titulo in zip(
            cabecalho,
            ['Nome', 'CPF', 'Telefone', 'Entrada', 'Situação']
        ):
            celula.text = titulo

        for pessoa in Pessoa.objects.all().order_by('nome'):
            linha = tabela.add_row().cells

            valores = [
                pessoa.nome,
                pessoa.cpf,
                pessoa.telefone,
                pessoa.data_entrada.strftime('%d/%m/%Y'),
                'Ativa' if pessoa.ativo else 'Inativa'
            ]

            for celula, valor in zip(linha, valores):
                celula.text = str(valor)

    if 'atendimentos' in selecionados:
        documento.add_heading('Atendimentos', level=1)

        tabela = documento.add_table(rows=1, cols=3)
        tabela.style = 'Table Grid'

        for celula, titulo in zip(
            tabela.rows[0].cells,
            ['Pessoa', 'Data', 'Modalidade']
        ):
            celula.text = titulo

        atendimentos = Atendimento.objects.select_related(
            'pessoa'
        ).order_by('-data_atendimento')

        for atendimento in atendimentos:
            linha = tabela.add_row().cells

            valores = [
                atendimento.pessoa.nome,
                atendimento.data_atendimento.strftime('%d/%m/%Y'),
                atendimento.get_modalidade_display()
            ]

            for celula, valor in zip(linha, valores):
                celula.text = str(valor)

    if 'acompanhamentos' in selecionados:
        documento.add_heading('Acompanhamentos', level=1)

        tabela = documento.add_table(rows=1, cols=5)
        tabela.style = 'Table Grid'

        for celula, titulo in zip(
            tabela.rows[0].cells,
            ['Pessoa', 'Especialidade', 'Início', 'Alta prevista', 'Situação']
        ):
            celula.text = titulo

        acompanhamentos = Acompanhamento.objects.select_related(
            'pessoa',
            'especialidades'
        ).order_by('-data_inicio')

        for acompanhamento in acompanhamentos:
            linha = tabela.add_row().cells

            valores = [
                acompanhamento.pessoa.nome,
                acompanhamento.especialidades.nome,
                acompanhamento.data_inicio.strftime('%d/%m/%Y'),
                (
                    acompanhamento.data_alta_prevista.strftime('%d/%m/%Y')
                    if acompanhamento.data_alta_prevista
                    else 'Não informada'
                ),
                acompanhamento.status
            ]

            for celula, valor in zip(linha, valores):
                celula.text = str(valor)

    if 'altas' in selecionados:
        documento.add_heading('Altas registradas', level=1)

        tabela = documento.add_table(rows=1, cols=4)
        tabela.style = 'Table Grid'

        for celula, titulo in zip(
            tabela.rows[0].cells,
            ['Pessoa', 'Especialidade', 'Início', 'Data da alta']
        ):
            celula.text = titulo

        altas = Acompanhamento.objects.filter(
            data_alta__isnull=False
        ).select_related(
            'pessoa',
            'especialidades'
        ).order_by('-data_alta')

        for alta in altas:
            linha = tabela.add_row().cells

            valores = [
                alta.pessoa.nome,
                alta.especialidades.nome,
                alta.data_inicio.strftime('%d/%m/%Y'),
                alta.data_alta.strftime('%d/%m/%Y')
            ]

            for celula, valor in zip(linha, valores):
                celula.text = str(valor)

    buffer = BytesIO()
    documento.save(buffer)
    buffer.seek(0)

    resposta = HttpResponse(
        buffer.getvalue(),
        content_type=(
            'application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document'
        )
    )

    resposta['Content-Disposition'] = (
        'attachment; filename="relatorio_magdala.docx"'
    )

    return resposta


# =====================================================
# GERAÇÃO DOS GRÁFICOS
# =====================================================

def gerar_grafico(titulo, rotulos, valores, tipo='barra'):
    figura, eixo = plt.subplots(figsize=(8, 4))

    if tipo == 'pizza':
        if not any(valores):
            plt.close(figura)
            return None

        eixo.pie(
            valores,
            labels=rotulos,
            autopct='%1.1f%%',
            startangle=90
        )

        eixo.axis('equal')

    else:
        eixo.bar(rotulos, valores)
        eixo.set_ylabel('Quantidade')
        eixo.tick_params(axis='x', rotation=30)

    eixo.set_title(titulo)
    figura.tight_layout()

    buffer = BytesIO()

    figura.savefig(
        buffer,
        format='png',
        dpi=150,
        bbox_inches='tight'
    )

    plt.close(figura)
    buffer.seek(0)

    imagem = base64.b64encode(
        buffer.getvalue()
    ).decode('utf-8')

    return imagem


# =====================================================
# RELATÓRIO GERAL PARA IMPRESSÃO
# =====================================================

@login_required
def relatorio_impressao(request):
    pessoas = Pessoa.objects.all().order_by('nome')

    atendimentos = Atendimento.objects.select_related(
        'pessoa'
    ).order_by('-data_atendimento')

    acompanhamentos = Acompanhamento.objects.select_related(
        'pessoa',
        'especialidades'
    ).order_by('-data_inicio')

    # 1. Cadastros por mês
    cadastros_mensais = Pessoa.objects.annotate(
        mes=TruncMonth('data_entrada')
    ).values(
        'mes'
    ).annotate(
        total=Count('id')
    ).order_by('mes')

    rotulos_cadastros = [
        item['mes'].strftime('%m/%Y')
        for item in cadastros_mensais
    ]

    valores_cadastros = [
        item['total']
        for item in cadastros_mensais
    ]

    grafico_cadastros = gerar_grafico(
        'Cadastros por mês',
        rotulos_cadastros,
        valores_cadastros
    ) if valores_cadastros else None

    # 2. Atendimentos por mês
    atendimentos_mensais = Atendimento.objects.annotate(
        mes=TruncMonth('data_atendimento')
    ).values(
        'mes'
    ).annotate(
        total=Count('id')
    ).order_by('mes')

    rotulos_atendimentos = [
        item['mes'].strftime('%m/%Y')
        for item in atendimentos_mensais
    ]

    valores_atendimentos = [
        item['total']
        for item in atendimentos_mensais
    ]

    grafico_atendimentos = gerar_grafico(
        'Atendimentos por mês',
        rotulos_atendimentos,
        valores_atendimentos
    ) if valores_atendimentos else None

    # 3. Atendimentos por modalidade
    modalidades = Atendimento.objects.values(
        'modalidade'
    ).annotate(
        total=Count('id')
    ).order_by('modalidade')

    escolhas_modalidade = dict(
        Atendimento._meta.get_field('modalidade').choices
    )

    rotulos_modalidades = [
        escolhas_modalidade.get(
            item['modalidade'],
            item['modalidade']
        )
        for item in modalidades
    ]

    valores_modalidades = [
        item['total']
        for item in modalidades
    ]

    grafico_modalidades = gerar_grafico(
        'Atendimentos por modalidade',
        rotulos_modalidades,
        valores_modalidades,
        tipo='pizza'
    ) if valores_modalidades else None

    # 4. Acompanhamentos ativos e encerrados
    ativos = Acompanhamento.objects.filter(
        data_alta__isnull=True
    ).count()

    encerrados = Acompanhamento.objects.filter(
        data_alta__isnull=False
    ).count()

    grafico_acompanhamentos = gerar_grafico(
        'Situação dos acompanhamentos',
        ['Ativos', 'Encerrados'],
        [ativos, encerrados],
        tipo='pizza'
    ) if ativos + encerrados > 0 else None

    return render(
        request,
        'relatorios/imprimir.html',
        {
            'pessoas': pessoas,
            'atendimentos': atendimentos,
            'acompanhamentos': acompanhamentos,
            'total_pessoas': pessoas.count(),
            'total_atendimentos': atendimentos.count(),
            'total_acompanhamentos': acompanhamentos.count(),
            'grafico_cadastros': grafico_cadastros,
            'grafico_atendimentos': grafico_atendimentos,
            'grafico_modalidades': grafico_modalidades,
            'grafico_acompanhamentos': grafico_acompanhamentos,
        }
    )