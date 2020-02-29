from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models

from pprint import pprint  # para o print formatar o dicionario no console


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
        # TODO: remover abaixo
        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()
        # foi apenas para apagar a sessao

        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))

        variacao_id = self.request.GET.get('vid')
        # vid é o nome que fica na url adicionaraocarrinho/?vid=1
        # variacao_id é uma string, se quiser utilizar para int tem que converter

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)
            # o referer é a url vvanterior a que "esta na classe". OBS: isso é meio que uma gambiarra, mas funciona

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            # criando a chave carrinho na sessão do usuário

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1
            # se cair aqui, é pq está tentando adicionar uma variação uma segunda vez ou +

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu carrinho. '
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho


        else:
            # adicionando uma nova variação que ainda não existe no carrinho
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }
            # incluindo um produto no carrinho

        self.request.session.save()
        pprint(carrinho)  # o pprint formata no console a impressão de um json/dict

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}.'
        )
        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            # caso não exista variação apenas retorna para pag anterior sem aviso mesmo
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            # variacao nao existe no carrinho
            return redirect(http_referer)

        carrinho = self.request.session['carrinho'][variacao_id]

        messages.success(
            self.request,
            f'Produto {carrinho["produto_nome"]} {carrinho["variacao_nome"]} removido do seu carrinho.'
        )

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()

        return redirect(http_referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }

        return render(self.request, 'produto/carrinho.html', contexto)


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
