from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import PessoaForm, AtendimentoForm, AcompanhamentoForm, SolicitacaoCadastroForm
from .models import Pessoa, Atendimento, Especialidades, Acompanhamento, SolicitacaoCadastro


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


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


@login_required
def cadastrar_pessoa(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Pessoa cadastrada com sucesso!')
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
            messages.success(request, 'Cadastro atualizado com sucesso!')

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


@login_required
def cadastrar_atendimento(request):
    form = AtendimentoForm(request.POST or None)

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


@login_required
def cadastrar_acompanhamento(request):
    form = AcompanhamentoForm(request.POST or None)

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

@login_required
def listar_solicitacoes(request):
    solicitacoes = SolicitacaoCadastro.objects.filter(
        status = 'pendente'
    ).order_by('-data_solicitacao')

    return render(
        request,
        'solicitacoes/lista.html',
        {'solicitacoes' : solicitacoes}
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
            return redirect('detalhes_solicitacao',
                            solicitacao_id=solicitacao.id)

        if Pessoa.objects.filter(cpf=solicitacao.cpf).exists():
            messages.error(
                request,
                'Já existe uma pessoa cadastrada com este CPF.'
            )
            return redirect('detalhes_solicitacao',
                            solicitacao_id=solicitacao.id)

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