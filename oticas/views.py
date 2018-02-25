from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import RegistroForm, EnderecoForm
from .models import Carrinho
from .models import Oculos

from urllib.request import Request, urlopen


# Create your views here.

def index(request):
    """A página inicial de Oticas"""
    return render(request, 'oticas/index.html')

def context(request): # Criado para enviar context ao base.html
    if request.user.is_authenticated():
        qtd_carrinhos = Carrinho.objects.all()
        qtd_carrinho= request.user.carrinho_set.all().count()
        context = {
            'qtd_carrinho': qtd_carrinho,
            'qtd_carrinhos': qtd_carrinhos,
        }
        return context
    else:
        carrinho = 0
        context = {
            'qtd_carrinho': carrinho
        }
        return context

def oculos(request):
    """Mostra todos os óculos"""
    oculos = Oculos.objects.order_by('-data_adc')
    context = {'oculos': oculos}
    return render(request, 'oticas/oculos.html', context)

def cadastro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('oticas:login')
        else:
            return render(request, 'oticas/cadastro.html', context)
    else:
        form = RegistroForm()

        context = {'form': form}
        return render(request, 'oticas/cadastro.html', context)

@login_required
def endereco(request):

    if request.method == 'POST':
        end_form = EnderecoForm(request.POST)
        context = {'end_form': end_form}
        if end_form.is_valid():
            novo_end = end_form.save(commit=False)
            novo_end.user = request.user
            novo_end.save()
            return redirect('oticas:index')
        else:
            return render(request, 'oticas/endereco.html', context)
    else:
        end_form = EnderecoForm()

        context = {'end_form': end_form}
        return render(request, 'oticas/endereco.html', context)

@login_required
def carrinho(request):
    oculos = Carrinho.objects.filter(dono=request.user).order_by('data_adc')
    total = Carrinho.objects.filter(dono=request.user).aggregate(Sum('valor_total'))['valor_total__sum'] or 0.00

    def calcula_frete (cep_destino='04110021', cep_origem ='14409652', peso='2', tipo_frete='04014',
                       altura = '10', largura = '20', comprimento = '20'):

        url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?'
        url += '&nCdEmpresa='
        url += '&sDsSenha='
        url += '&nCdServico=' + tipo_frete
        url += '&sCepOrigem=' + cep_origem
        url += '&sCepDestino=' + cep_destino
        url += '&nVlPeso=' + peso
        url += '&nCdFormato=1'
        url += '&nVlComprimento=' + comprimento
        url += '&nVlAltura=' + altura
        url += '&nVlLargura=' + largura
        url += '&nVlDiametro=0'
        url += '&sCdMaoPropria=n'
        url += '&nVlValorDeclarado=0'
        url += '&sCdAvisoRecebimento=n'
        url += '&StrRetorno=xml'
        url += '&nIndicaCalculo=3'

        return(url)

    cep_destino = request.user.enderecouser_set.values()[0]['cep']
    url = calcula_frete(cep_destino)

    request1 = Request(url)
    result = urlopen(request1).read()

    result = result.decode('ISO-8859-1')
    find_valor = ('<Valor>')
    find_end_valor = ('</Valor>')
    pos_valor = result.index(find_valor)
    pos_end_valor = result.index(find_end_valor)

    find_prazo = ('<PrazoEntrega>')
    find_end_prazo = ('</PrazoEntrega>')
    pos_prazo = result.index(find_prazo)
    pos_end_prazo = result.index(find_end_prazo)

    valor = result[pos_valor + len(find_valor): pos_end_valor]
    prazo = result[pos_prazo + len(find_prazo): pos_end_prazo]

    valor_math = valor.replace(',', '.')
    valor_math = float(valor_math)

    total_math = float(total)

    total_geral = total_math + valor_math

    context = {
        'url' : url,
        'valor' : valor,
        'prazo' : prazo,
        'oculos': oculos,
        'total': total,
        'total_geral' : total_geral,
    }

    return render(request, 'oticas/carrinho.html', context)

@login_required
def adicionaCarrinho(request, oculos_id):
    oculos = Oculos.objects.get(id=oculos_id)
    oculos_a_adicionar = Carrinho(produto=oculos, dono=request.user, valor_total=oculos.valor)
    oculos_a_adicionar.save()
    return redirect('oticas:oculos')

@login_required
def deletaCarrinho(request, oculos_id):
    oculos = Carrinho.objects.get(id=oculos_id)
    oculos.delete()
    return redirect('oticas:carrinho')

@login_required
def comprar(request):

    oculos = Carrinho.objects.filter(dono=request.user).order_by('data_adc')
    total = Carrinho.objects.filter(dono=request.user).aggregate(Sum('valor_total'))['valor_total__sum'] or 0.00

    def calcula_frete (cep_destino='04110021', cep_origem ='14409652', peso='2', tipo_frete='04014',
                       altura = '10', largura = '20', comprimento = '20'):

        url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?'
        url += '&nCdEmpresa='
        url += '&sDsSenha='
        url += '&nCdServico=' + tipo_frete
        url += '&sCepOrigem=' + cep_origem
        url += '&sCepDestino=' + cep_destino
        url += '&nVlPeso=' + peso
        url += '&nCdFormato=1'
        url += '&nVlComprimento=' + comprimento
        url += '&nVlAltura=' + altura
        url += '&nVlLargura=' + largura
        url += '&nVlDiametro=0'
        url += '&sCdMaoPropria=n'
        url += '&nVlValorDeclarado=0'
        url += '&sCdAvisoRecebimento=n'
        url += '&StrRetorno=xml'
        url += '&nIndicaCalculo=3'

        return(url)

    cep_destino = request.user.enderecouser_set.values()[0]['cep']
    url = calcula_frete(cep_destino)

    request1 = Request(url)
    result = urlopen(request1).read()

    result = result.decode('ISO-8859-1')
    find_valor = ('<Valor>')
    find_end_valor = ('</Valor>')
    pos_valor = result.index(find_valor)
    pos_end_valor = result.index(find_end_valor)

    find_prazo = ('<PrazoEntrega>')
    find_end_prazo = ('</PrazoEntrega>')
    pos_prazo = result.index(find_prazo)
    pos_end_prazo = result.index(find_end_prazo)

    valor = result[pos_valor + len(find_valor): pos_end_valor]
    prazo = result[pos_prazo + len(find_prazo): pos_end_prazo]

    valor_math = valor.replace(',', '.')
    valor_math = float(valor_math)
    valor_unit = valor_math / oculos.count()
    valor_unit = round(valor_unit,2)

    context = {
        'url' : url,
        'valor' : valor,
        'prazo' : prazo,
        'oculos': oculos,
        'total': total,
        'valor_unit': valor_unit,
    }

    return render(request, 'oticas/comprar.html', context)