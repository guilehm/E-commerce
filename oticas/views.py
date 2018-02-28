from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistroForm, EnderecoForm, ContatoForm, CepForm
from .models import Carrinho
from .models import Oculos

from urllib.request import Request, urlopen


# Create your views here.

def index(request):
    """A página inicial de Oticas"""
    return render(request, 'oticas/index.html')

def context(request): # Criado para enviar context ao base.html
    if request.user.is_authenticated():
        qtd_carrinho= request.user.carrinho_set.all().count()
        context = {
            'qtd_carrinho': qtd_carrinho,
        }
        return context
    else:
        key = request.session.session_key
        carrinho = Carrinho.objects.filter(dono_ano=key).count()
        context = {
            'qtd_carrinho': carrinho
        }
        return context

def oculos(request):
    """Mostra todos os óculos"""
    if not request.session.session_key:
        request.session.create()

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



def adicionaCarrinho(request, oculos_id):
    if request.user.is_authenticated():
        oculos = Oculos.objects.get(id=oculos_id)
        oculos_a_adicionar = Carrinho(produto=oculos, dono=request.user, valor_total=oculos.valor)
        oculos_a_adicionar.save()
    else:
        key = request.session.session_key
        if request.session.session_key:
            oculos = Oculos.objects.get(id=oculos_id)
            oculos_a_adicionar = Carrinho(produto=oculos, dono_ano=key, valor_total=oculos.valor)
            oculos_a_adicionar.save()
        else:
            oculos = Oculos.objects.get(id=oculos_id)
            request.session.create()
            oculos_a_adicionar = Carrinho(produto=oculos, dono_ano=key, valor_total=oculos.valor)
            oculos_a_adicionar.save()

    return redirect('oticas:oculos')



def carrinho(request):
    if request.user.is_authenticated():
        oculos = Carrinho.objects.filter(dono=request.user).order_by('data_adc')
        total = Carrinho.objects.filter(dono=request.user).aggregate(Sum('valor_total'))['valor_total__sum'] or 0.00


        def calcula_frete (cep_destino, cep_origem ='14407000', peso='2', tipo_frete='04014',
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

        def prazo_maior (request):
            if request.user.is_authenticated():
                carrinho = Carrinho.objects.filter(dono=request.user)
                if carrinho:
                    lista_prazo = []
                    for i in carrinho:
                        lista_prazo.append(i.prazo)

                    return (int(max(lista_prazo)))
                else:
                    return (0)

            else:
                key = request.session.session_key

                carrinho = Carrinho.objects.filter(dono_ano=key).order_by('data_adc')
                if carrinho:
                    lista_prazo = []
                    for i in carrinho:
                        lista_prazo.append(i.prazo)

                    return (int(max(lista_prazo)))

                else:
                    return (0)

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
        prazo = int(result[pos_prazo + len(find_prazo): pos_end_prazo])

        prazo_maior_prod = prazo_maior(request)

        prazo += prazo_maior_prod

        valor_math = valor.replace(',', '.')
        valor_math = float(valor_math)

        total_math = float(total)

        total_geral = total_math + valor_math

        context = {
            'url': url,
            'valor': valor,
            'prazo': prazo,
            'oculos': oculos,
            'total': total,
            'total_geral': total_geral,
        }

        return render(request, 'oticas/carrinho.html', context)

    else:
        key = request.session.session_key

        oculos = Carrinho.objects.filter(dono_ano=key).order_by('data_adc')
        total = Carrinho.objects.filter(dono_ano=key).aggregate(Sum('valor_total'))['valor_total__sum'] or 0.00

        def calcula_frete(request):
            pass


        context = {
            'oculos' : oculos,
            'total' : total,
        }

        return render(request, 'oticas/carrinho.html', context)


def deletaCarrinho(request, oculos_id):
    oculos = Carrinho.objects.get(id=oculos_id)
    oculos.delete()
    return redirect('oticas:carrinho')

@login_required
def comprar(request):

    oculos = Carrinho.objects.filter(dono=request.user).order_by('data_adc')
    total = Carrinho.objects.filter(dono=request.user).aggregate(Sum('valor_total'))['valor_total__sum'] or 0.00

    def calcula_frete (cep_destino='04110021', cep_origem ='14409652', peso='2', tipo_frete='04014',
                       altura ='10', largura ='20', comprimento ='20'):

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


def contato(request):
    sucesso = False
    if request.method == 'POST':
        contato_form = ContatoForm(request.POST)
        if contato_form.is_valid():
            nome = contato_form.cleaned_data['nome']
            email = contato_form.cleaned_data['email']
            mensagem = contato_form.cleaned_data['mensagem']
            mensagem = 'Nome: {0}\nE-mail: {1}\n{2}'.format(nome, email, mensagem)
            send_mail(
                'Contato do Gui E-commerce', mensagem, settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL]
            )
            sucesso= True
    else:
        contato_form = ContatoForm()
    context = {
        'contato_form' : contato_form,
        'sucesso' : sucesso
    }
    return render(request,'oticas/contato.html', context)