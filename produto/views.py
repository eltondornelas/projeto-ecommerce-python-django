from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'  # nome do objeto do template
    paginate_by = 3



class DetalheProduto(DetailView):
    # View precisaria utilizar muito código por isso trocou para DetailView
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarAoCarrinho(View):
    # quando usar o class based View, vai precisar escrever os métodos Get e Post, caso necessário
    # essa classe não renderiza, apenas redireciona
    def get(self, *args, **kwargs):       
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))

        variacao_id = self.request.GET.get('vid')
        # vid é o nome que fica na url adicionaraocarrinho/?vid=1

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)        
        # o referer é a url anterior a que "esta na classe". OBS: isso é meio que uma gambiarra, mas funciona
    
        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            # criando a chave carrinho na sessão do usuário

        carrinho = self.request.sessio['carrinho']

        if variacao_id in carrinho:
             # TODO: Variação existe no carrinho
             pass
        
        else:
            # TODO: variação não existe no carrinho
            pass

        return HttpResponse(f'{variacao.produto} {variacao.nome}')



class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover carrinho')



class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')



class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
