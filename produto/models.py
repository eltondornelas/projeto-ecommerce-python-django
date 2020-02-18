import os

from django.conf import settings
from django.db import models
from PIL import Image


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)  # é apenas descrição na página inicial, 255 é até grande
    descricao_longa = models.TextField()  # ilimitado
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField()  # dessa forma fica obrigatório informar um valor
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples'),
        )
    )


    @staticmethod
    def resize_image(img, new_width=800):  # máximo já fica 800
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        # print(img_full_path)
        # print(original_width, original_height)

        if original_width <= new_width:
            # print('retornando. largura original menor que nova largura')
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)  # LANCZOS é um calc mat para diminuir a img em pixels
        new_img.save(
            img_full_path,
            optmize=True,
            quality=50
        )

        # print('Imagem foi redimensionada.')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)


    # Mostra o nome real em admin
    def __str__(self):
        return self.nome


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.nome or self.produto.nome
        # ou nome da variação ou nome do produto


    # essa classe controla em deixar singular ou plural o nome da classe que está inserida
    # pesquisar por: django model plural name
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
    
