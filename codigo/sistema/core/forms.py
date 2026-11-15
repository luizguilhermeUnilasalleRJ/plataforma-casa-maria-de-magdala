from datetime import date
from django import forms
from .models import Pessoa, Atendimento, Especialidades, Acompanhamento, SolicitacaoCadastro


def cpf_valido(cpf):
    cpf = ''.join(caractere for caractere in cpf if caractere.isdigit())

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for tamanho in (9, 10):
        soma = sum(
            int(cpf[i]) * (tamanho + 1 - i)
            for i in range(tamanho)
        )

        digito = (soma * 10) % 11

        if digito == 10:
            digito = 0

        if digito != int(cpf[tamanho]):
            return False

    return True


class PessoaForm(forms.ModelForm):

    class Meta:
        model = Pessoa

        fields = [
            'nome',
            'data_nascimento',
            'cpf',
            'telefone',
            'nome_responsavel',
            'estado_civil',
            'endereco',
            'data_entrada',
            'origem_cadastro',
        ]

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']

        if not cpf_valido(cpf):
            raise forms.ValidationError(
                'O CPF informado é inválido.'
            )

        return ''.join(
            caractere for caractere in cpf
            if caractere.isdigit()
        )

    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']

        if data > date.today():
            raise forms.ValidationError(
                'A data de nascimento não pode ser futura.'
            )

        if data.year < 1900:
            raise forms.ValidationError(
                'Informe um ano de nascimento válido.'
            )

        return data

    def clean_data_entrada(self):
        data = self.cleaned_data['data_entrada']

        if data > date.today():
            raise forms.ValidationError(
                'A data de entrada não pode ser futura.'
            )

        if data.year < 1900:
            raise forms.ValidationError(
                'Informe um ano de entrada válido.'
            )

        return data

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']

        numeros = ''.join(
            caractere for caractere in telefone
            if caractere.isdigit()
        )

        if len(numeros) not in (10, 11):
            raise forms.ValidationError(
                'Informe um telefone com DDD e 10 ou 11 dígitos.'
            )

        if len(set(numeros)) == 1:
            raise forms.ValidationError(
                'Informe um número de telefone válido.'
            )

        return numeros


class AtendimentoForm(forms.ModelForm):

    class Meta:
        model = Atendimento

        fields = [
            'pessoa',
            'data_atendimento',
            'modalidade',
            'observacoes',
        ]

        widgets = {
            'pessoa': forms.Select(attrs={'data-placeholder': 'Selecione uma pessoa'}),
            'data_atendimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

        labels = {
            'pessoa': 'Pessoa',
            'data_atendimento': 'Data do atendimento',
            'modalidade': 'Modalidade',
            'observacoes': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pessoa'].empty_label = None

        self.fields['modalidade'].choices = [
            ('', 'Selecione uma modalidade')
        ] + list(Atendimento.MODALIDADE_CHOICES)

    def clean_data_atendimento(self):
        data = self.cleaned_data['data_atendimento']

        if data > date.today():
            raise forms.ValidationError(
                'A data do atendimento não pode ser futura.'
            )

        if data.year < 1900:
            raise forms.ValidationError(
                'Informe uma data de atendimento válida.'
            )

        return data

    def clean_pessoa(self):
        pessoa = self.cleaned_data['pessoa']

        if not pessoa.ativo:
            raise forms.ValidationError(
                'Não é possível registrar atendimento para uma pessoa inativa.'
            )

        return pessoa


class AcompanhamentoForm(forms.ModelForm):

    class Meta:
        model = Acompanhamento

        fields = [
            'pessoa',
            'especialidades',
            'data_inicio',
            'data_alta_prevista',
            'data_alta',
            'observacoes',
        ]

        widgets = {
            'pessoa': forms.Select(
                attrs={'data-placeholder': 'Selecione uma pessoa'}
            ),
            'especialidades': forms.Select(
                attrs={'data-placeholder': 'Selecione uma atividade'}
            ),
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_alta_prevista': forms.DateInput(attrs={'type': 'date'}),
            'data_alta': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

        labels = {
            'pessoa': 'Pessoa',
            'especialidades': 'Atividade',
            'data_inicio': 'Data de início',
            'data_alta_prevista': 'Data prevista de alta',
            'data_alta': 'Data efetiva de alta',
            'observacoes': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pessoa'].empty_label = None
        self.fields['especialidades'].empty_label = None

    def clean_data_inicio(self):
        data = self.cleaned_data['data_inicio']

        if data > date.today():
            raise forms.ValidationError(
                'A data de início não pode ser futura.'
            )

        if data.year < 1900:
            raise forms.ValidationError(
                'Informe uma data de início válida.'
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        data_inicio = cleaned_data.get('data_inicio')
        data_prevista = cleaned_data.get('data_alta_prevista')
        data_efetiva = cleaned_data.get('data_alta')

        if data_inicio and data_prevista:
            if data_prevista < data_inicio:
                self.add_error(
                    'data_alta_prevista',
                    'A previsão de alta não pode ser anterior ao início.'
                )

        if data_inicio and data_efetiva:
            if data_efetiva < data_inicio:
                self.add_error(
                    'data_alta',
                    'A alta efetiva não pode ser anterior ao início.'
                )

            if data_efetiva > date.today():
                self.add_error(
                    'data_alta',
                    'A alta efetiva não pode ser futura.'
                )

        return cleaned_data

    def clean_pessoa(self):
        pessoa = self.cleaned_data['pessoa']

        if not pessoa.ativo:
            raise forms.ValidationError(
                'Não é possível criar acompanhamento para uma pessoa inativa.'
            )

        return pessoa

    def clean_especialidades(self):
        especialidade = self.cleaned_data['especialidades']

        if not especialidade.ativa:
            raise forms.ValidationError(
                'Esta especialidade está inativa.'
            )

        return especialidade

class SolicitacaoCadastroForm(forms.ModelForm):

    class Meta:
        model = SolicitacaoCadastro

        fields = [
            'nome',
            'data_nascimento',
            'cpf',
            'telefone',
            'email',
            'nome_responsavel',
            'estado_civil',
            'endereco',
        ]

        widgets = {
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'estado_civil': forms.Select(),
        }

        labels = {
            'nome': 'Nome completo',
            'data_nascimento': 'Data de nascimento',
            'cpf': 'CPF',
            'telefone': 'Telefone com DDD',
            'email': 'E-mail',
            'nome_responsavel': 'Nome do responsável',
            'estado_civil': 'Estado civil',
            'endereco': 'Endereço',
        }

        def clean_cpf(self):
            cpf = self.cleaned_data['cpf']

            if not cpf_valido(cpf):
                raise forms.ValidationError(
                    'O CPF informado é inválido.'
                )

            return ''.join(
            caractere for caractere in cpf
            if caractere.isdigit()
            )

        def clean_data_nascimento(self):
            data = self.cleaned_data['data_nascimento']

            if data > date.today():
                raise forms.ValidationError(
                    'A data de nascimento não pode ser futura.'
                )

            if data.year < 1900:
                raise forms.ValidationError(
                    'Informe um ano de nascimento válido.'
                )

            return data

        def clean_telefone(self):
            telefone = self.cleaned_data['telefone']

            numeros = ''.join(
                caractere for caractere in telefone
                if caractere.isdigit()
            )

            if len(numeros) not in (10, 11):
                raise forms.ValidationError(
                    'Informe um telefone com DDD e 10 ou 11 dígitos.'
                )

            if len(set(numeros)) == 1:
                raise forms.ValidationError(
                    'Informe um número de telefone válido.'
                )

            return numeros