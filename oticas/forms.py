from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EnderecoUser


class RegistroForm(UserCreationForm):

    email = forms.EmailField(label='E-mail', required=True)
    telefone = forms.CharField()
    cpf = forms.CharField(label='CPF')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'telefone',
            'cpf',
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
        }

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'cpf': 'CPF',
        }


    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.telefone = self.cleaned_data['telefone']
        user.cpf = self.cleaned_data['cpf']

        if commit:
            user.save()

        return user


class EnderecoForm(forms.ModelForm):
    cep = forms.TextInput()
    rua = forms.TextInput()
    numero = forms.TextInput()
    complemento = forms.TextInput()
    bairro = forms.TextInput()
    cidade = forms.TextInput()
    estado = forms.TextInput()

    class Meta:
        model = EnderecoUser
        fields = (
            'cep',
            'rua',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
        )

        labels = {
            'cep': 'CEP',
            'rua': 'Rua',
            'numero': 'Número',
            'complemento': 'Complemento',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado',
        }

        widgets = {
            'cep': forms.TextInput(attrs={'onblur': "pesquisacep(this.value);"}),
        }

    def save(self, commit=True):
        user = super(EnderecoForm, self).save(commit=False)
        user.cep = self.cleaned_data['cep']
        user.rua = self.cleaned_data['rua']
        user.numero = self.cleaned_data['numero']
        user.complemento = self.cleaned_data['complemento']
        user.bairro = self.cleaned_data['bairro']
        user.cidade = self.cleaned_data['cidade']
        user.estado = self.cleaned_data['estado']

        if commit:
            user.save()

        return user


class ContatoForm(forms.Form):

    nome = forms.CharField(label='Nome', required=True)
    email = forms.EmailField(label='Email')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea(), required=True)

    def __init__(self, *args, **kwargs):
        super(ContatoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['nome'].widget.attrs['id'] = 'id_nome_contato'
        self.fields['nome'].widget.attrs['placeholder'] = 'Digite seu nome completo'
        self.fields['email'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['email'].widget.attrs['placeholder'] = 'Digite seu email'
        self.fields['mensagem'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['mensagem'].widget.attrs['placeholder'] = 'Escreva aqui sua mensagem...'
