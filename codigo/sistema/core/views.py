from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PessoaForm


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

    return render(request, 'login.html')


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