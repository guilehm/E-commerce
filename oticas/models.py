from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Oculos(models.Model):
    """Informações sobre os óculos"""
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    estilo = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    publico = models.CharField(max_length=100)
    sexo = models.CharField(max_length=100)
    prazo = models.CharField(max_length=2)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    pagamento = models.CharField(max_length=100)
    descricao = models.TextField()
    disp = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to="oticas/fotos")
    img1 = models.ImageField(upload_to="oticas/fotos", blank=True)
    img2 = models.ImageField(upload_to="oticas/fotos", blank=True)
    img3 = models.ImageField(upload_to="oticas/fotos", blank=True)
    data_adc = models.DateTimeField(auto_now_add=True)
    data_upd = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        """Devolve a marca + modelo"""
        return (self.marca + ": " + self.modelo)


    class Meta:
        ordering = ('-data_adc',)
        verbose_name_plural = 'Oculos'


class EnderecoUser(models.Model):
    """Informações sobre os endereços"""
    user = models.ForeignKey(User)
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=200)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=20, blank=True)
    bairro = models.CharField(max_length=40)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = 'Endereço dos Usuários'

    def __str__(self):
        """Devolve o nome + cidade"""
        return (self.user.username + ": " + self.user.first_name)


class Carrinho(models.Model):
    produto = models.ForeignKey(Oculos)
    dono = models.ForeignKey(User)
    data_adc = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(null=True, max_digits=6, decimal_places=2)

    def adicionar(self):
        Carrinho.produto.save()

    def __str__(self):
        return (self.produto.marca + " : " + self.produto.modelo)

    @property
    def marca(self):
        return self.produto.marca

    @property
    def modelo(self):
        return self.produto.modelo

    @property
    def estilo(self):
        return self.produto.estilo

    @property
    def cep(self):
        return self.dono.cep

    @property
    def prazo(self):
        return self.produto.prazo

    @property
    def valor(self):
        return self.produto.valor

    @property
    def pagamento(self):
        return self.produto.pagamento

    @property
    def imagem(self):
        return self.produto.imagem

    @property
    def img1(self):
        return self.produto.img1

    @property
    def img2(self):
        return self.produto.img2

    @property
    def img3(self):
        return self.produto.img3

    @property
    def descricao(self):
        return self.produto.descricao