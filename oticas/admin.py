from django.contrib import admin
from oticas.models import Oculos, EnderecoUser, Carrinho

# Register your models here.

class OculosAdmin(admin.ModelAdmin):
    list_display = ['__str__','material','sexo', 'data_adc', 'prazo','valor','pagamento', 'disp']
    list_filter = ['material','sexo','estilo','publico','disp']
    list_editable = ['prazo','valor','pagamento','disp']
    class Meta:
        model = Oculos


class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'rua', 'bairro', 'cidade']
    class Meta:
        model = EnderecoUser


class CarrinhoAdmin(admin.ModelAdmin):
    usuario = Carrinho.dono
    list_display = ['__str__','dono','data_adc', 'valor_total']
    class Meta:
        model = Carrinho


admin.site.register(Oculos, OculosAdmin)
admin.site.register(EnderecoUser, EnderecoAdmin)
admin.site.register(Carrinho, CarrinhoAdmin)

