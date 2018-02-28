"""Define padrões de URL para oticas."""

from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    # Página inicial
    url(r'^$', views.index, name='index'),
    url(r'^oculos/$', views.oculos, name='oculos'),
    url(r'^login/$', login, {'template_name': 'oticas/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'oticas/logout.html'}, name='logout'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^endereco/$', views.endereco, name='endereco'),
    url(r'^carrinho/$', views.carrinho, name='carrinho'),
    url(r'^comprar/$', views.comprar, name='comprar'),
    url(r'^contato/$', views.contato, name='contato'),
    url(r'^carrinho/(?P<oculos_id>\d+)/adicionar$', views.adicionaCarrinho, name='adicionar'),
    url(r'^carrinho/(?P<oculos_id>\d+)/deletar$', views.deletaCarrinho, name='deletar'),
]