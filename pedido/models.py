from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Pedido é um "filho" de usuário, pois ele é quem tem os pedidos
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(
        default='C',
        max_length=1,  # apenas 1 letra
        choices=(
            ('A', 'Aprovado'),  # (valor_real, descricao_do_valor)
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )

    def __str__(self):
        return f'Pedido N. {self.pk}'



class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=50)
    # vai ser o nome do produto e o max_length tem que ser igual ao do produto
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    # em tese não precisa, pois o que importa é o preco do pedido, se é promocional ou nao, nao importa aqui.
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)  # mesma imagem a ser exibida no carrinho do cliente, queremos apenas o caminho da imagem

    def __str__(self):
        return f'Item do {self.pedido}'  # o self.pedido vai retornar a string do __str__ daquela classe

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
