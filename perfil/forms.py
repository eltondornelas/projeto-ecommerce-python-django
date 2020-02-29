from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)
        # excluindo o campo usuario do model Perfil, para que ele não tenha a opção de selecionar um usuario


class UserForm(forms.ModelForm):
    # formulario de cadastro do proprio usuario

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'  # para exibir como Senha
    )
    # não é requerido para que nao precisa atualizar senha toda vez que for atualizar os outros dados

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha'  # para exibir como Senha
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario
        # dessa forma consegue saber quem esta enviando o formulário, se existe ou não

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data  # pega os dados "cru" do formulário
        cleaned = self.cleaned_data  # pega os dados limpos do formulário
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password')

        usuario_db = User.objects.filter(username=usuario_data).first()  # se aparecer algum é porque existe
        email_db = User.objects.filter(username=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As duas senhas não são iguais'
        error_msg_password_short = 'A senha tem que ter mínimo de 6 caracteres'

        # usuarios logados: atualizacao
        if self.usuario:
            # validation_error_msgs['username'] = 'Bla bla bla bla'
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                if email_data != email_db.email:  # os _db traz a consulta inteira, precisa dizer qual campo
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short


        # usuarios não logados: cadastro
        else:
            validation_error_msgs['username'] = 'Bla bla bla bla'

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))
