from django import forms
from .models import Pessoa


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
            raise forms.ValidationError('Digite um CPF válido.')

        return ''.join(caractere for caractere in cpf if caractere.isdigit())