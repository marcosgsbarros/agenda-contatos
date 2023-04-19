from django.urls import path
from .views import IndexView,DetalhesView,BuscaView,CadastroContatoView,ContatoUpdateView,\
    ContatoDeleteView,CadastroCategoriaView,CategoriasListView,CategoriaUpdateView,CategoriaDeleteView


urlpatterns = [
    path('',IndexView.as_view(template_name='contatos/index.html'),name='index'),
    path('detalhes/<int:pk>/',DetalhesView.as_view(template_name='contatos/detalhes.html'), name='detalhes'),
    path('busca/',BuscaView.as_view(template_name='contatos/busca.html'), name='busca'),
    path('cadastrar-contato/',CadastroContatoView.as_view(template_name='contatos/cadastro_contatos.html'),name='cadcontato'),
    path('editar-contato/<int:pk>/',ContatoUpdateView.as_view(template_name='contatos/editar_contato.html'),name='editar'),
    path('deletar-contato/<int:pk>/',ContatoDeleteView.as_view(template_name='contatos/deletar_contato.html'),name='deletar'),
    path('cadastrar-categoria/',CadastroCategoriaView.as_view(template_name='contatos/cadastro_categoria.html'),name='cadcategoria'),
    path('listar-categorias/',CategoriasListView.as_view(template_name='contatos/categorias.html'),name='categorias'),
    path('editar-categoria/<int:pk>/',CategoriaUpdateView.as_view(template_name='contatos/editar_categoria.html'),name='editcategoria'),
    path('deletar-categoria/<int:pk>/',CategoriaDeleteView.as_view(template_name='contatos/deletar_categoria.html'),name='delcategoria'),
] 