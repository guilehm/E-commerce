from .models import Carrinho

def calcular_frete(cep_destino, cep_origem='14407000', peso='2', tipo_frete='04014',
                  altura='10', largura='20', comprimento='20'):
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

    return (url)


def prazo_maior_ano(request):
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