from django.contrib import admin
from .models import Produto, Variacao  # outra forma idêntica seria: from produto.models import Produto
# poderia ser: from . import models -> porém vai precisar sempre digitar models.Classe


class VariacaoInline(admin.TabularInline):  # ou StackedInline. TabularInline fica como se fosse uma tabela
    model = Variacao
    extra = 1  # com isso vai mostrar 1 campo a mais em branco


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_preco_formatado', 'get_preco_promocional_formatado']

    # quando entrar em Produto, quais os "filhos" desse produto você quer ver para editar junto
    inlines = [
        VariacaoInline
    ]


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)
