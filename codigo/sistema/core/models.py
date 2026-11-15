from django.db import models


class Pessoa(models.Model):
    nome = models.CharField(max_length=150)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True)
    nome_responsavel = models.CharField(max_length=150, blank=True)
    estado_civil = models.CharField(max_length=30)
    endereco = models.CharField(max_length=260, blank=True)
    data_entrada = models.DateField()
    origem_cadastro = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Atendimento(models.Model):

    MODALIDADE_CHOICES = [
        ('presencial', 'Presencial'),
        ('online', 'Online')
    ]

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        related_name='atendimentos'
    )

    data_atendimento = models.DateField()

    modalidade = models.CharField(
        max_length=20,
        choices=MODALIDADE_CHOICES
    )

    observacoes = models.TextField(blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Atendimento de {self.pessoa.nome} em {self.data_atendimento}'


class Especialidades(models.Model):

    CATEGORIA_CHOICES = [
        ('terapeutica', 'Parte Terapêutica'),
        ('artesanato', 'Artesanato'),
        ('capacitacao', 'Cursos de Capacitação'),
        ('educacao', 'Educação e Cultura'),
    ]

    nome = models.CharField(max_length=100)

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES
    )

    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Acompanhamento(models.Model):

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        related_name='acompanhamentos'
    )

    especialidades = models.ForeignKey(
        Especialidades,
        on_delete=models.PROTECT,
        related_name='acompanhamentos'
    )

    data_inicio = models.DateField()

    # Previsão: pode ser futura.
    data_alta_prevista = models.DateField(
        null=True,
        blank=True
    )

    # Alta efetiva: quando o acompanhamento realmente termina.
    data_alta = models.DateField(
        null=True,
        blank=True
    )

    observacoes = models.TextField(blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        return 'Encerrado' if self.data_alta else 'Ativo'

    def __str__(self):
        return f'{self.pessoa.nome} - {self.especialidades.nome}'

class SolicitacaoCadastro(models.Model):

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('recusada', 'Recusada'),
    ]

    ESTADO_CIVIL_CHOICES = [
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
        ('uniao_estavel', 'União estável'),
    ]

    nome = models.CharField(max_length=150)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True)
    nome_responsavel = models.CharField(max_length=150, blank=True)
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES)
    endereco = models.CharField(max_length=260, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.get_status_display()}'