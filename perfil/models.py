from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

import re

from utils.validacpf import valida_cpf



class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, help_text='Apenas números.')
    # tamanhos abaixo relacionados a endereço estão seguindo as recomenções do correios
    # o normal seria criar um outro model de Endereco fazendo uma ForeignKey para o Usuário
    endereco = models.CharField(max_length=50, verbose_name='Endereço')
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.usuario}'  # pegando o first_name do user que é do Django

    def clean(self):  # validando campos
        error_messages = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None
        perfil = Perfil.objects.filter(cpf=cpf_enviado).first()

        if perfil:
            cpf_salvo = perfil.cpf  # o que esta salvo no banco de dados

            if cpf_salvo is not None and self.pk != perfil.pk:
                # caso obtenho um cpf da base de dados, ou seja, não é None
                # se os pks forem iguais, significa que o cliente está atualizando o cpf
                error_messages['cpf'] = 'CPF já existe.'

        # dessa forma consegue levantar excecao para cada campo específico
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP inválido, digite apenas números.'

        # vai armazenando os erros e mostra todos de uma vez, caso tenha 1 ou mais
        if error_messages:
            raise ValidationError(error_messages)


    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'


