from django.db import models
import uuid
import os
from datetime import datetime
from django.contrib.auth import get_user_model

def renomeia_foto(instance,nome):
    ext = nome.split('.')[-1]
    nome_arquivo = uuid.uuid4().hex
    nome_arquivo = f'{nome_arquivo}.{ext}'
    caminho_arquivo = 'fotos/'+datetime.now().strftime('%Y/%m')
    return os.path.join(caminho_arquivo,nome_arquivo)


class Categoria(models.Model):
    nome = models.CharField('Nome',max_length=100)
    usuario = models.ForeignKey(get_user_model(), verbose_name='Usuário', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name ='Categoria'
        verbose_name_plural ='Categorias'
    
    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField('Nome',max_length=60)
    sobrenome = models.CharField('Sobrenome',max_length=60,blank=True)
    telefone = models.CharField('Telefone',max_length=15)
    email = models.EmailField('E-mail',max_length=80,blank=True)
    data_criacao = models.DateField('Data de criação',auto_now_add=True)
    descricao = models.TextField('Descrição',max_length=200,blank=True)
    categoria = models.ForeignKey(Categoria,on_delete=models.PROTECT)
    mostrar = models.BooleanField(default=True)
    foto = models.ImageField(upload_to=renomeia_foto,blank=True)
    usuario = models.ForeignKey(get_user_model(), verbose_name='Usuário', on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name ='Contato'
        verbose_name_plural ='Contatos'
    
    def __str__(self):
        return self.nome