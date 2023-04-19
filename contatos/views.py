from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from django.core.paginator import Paginator
from django.http import Http404
from .models import Contato,Categoria
from django.shortcuts import get_object_or_404,redirect
from django.db.models import Q , Value
from django.db.models.functions import Concat
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CadastroContatoForm,CadastroCategoriaForm
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.contrib.auth.mixins import LoginRequiredMixin

#Página principal Index.html
class IndexView(LoginRequiredMixin,ListView):
    
    model = Contato
    template_name = 'index'
    paginate_by = 7
    
    def get_queryset(self):
        return Contato.objects.filter(usuario=self.request.user).filter(mostrar=True).order_by('nome')
    
    # Envia informações dos contatos cadastrados no banco de dados
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        contatos_mostrados = self.get_queryset()
        paginator = Paginator(contatos_mostrados,self.paginate_by)
        page = self.request.GET.get('page')
        context['contatos'] = paginator.get_page(page)
        return context
        #Contato.objects.filter(mostrar=True).order_by('nome')
    
        

#Mostra detalhes ao selecionar o contato     
class DetalhesView(LoginRequiredMixin,DetailView):
    
    model = Contato
    template_name = 'detalhes'
    
    
     # Verifica se o caminho da url está correta, caso contrário retorna um erro 404
    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        contato = get_object_or_404(queryset, id=self.kwargs['pk'])
        
        # Verifica se o contato pertence ao usuário atual
        if contato.usuario != self.request.user:
            raise Http404()
        
        # Verifica se o contato pode ser mostrado
        if not contato.mostrar:
            raise Http404()
        
        return contato
      
  
#Pesquisa os contatos no banco de dados
class BuscaView(LoginRequiredMixin,ListView):
    
    model = Contato
    template_name = 'busca'
    paginate_by = 10
    
    #Verifica se o campo de busca está vazio
    def dispatch(self,request,*args, **kwargs):
        
        termo = self.request.GET.get('termo')
        space = termo.count(' ')
        
        if termo is None or space == len(termo):
            messages.add_message(request,messages.ERROR,'O campo de busca não pode ficar vazio')
            return redirect('index')
            
        return super().dispatch(request, *args, **kwargs)
    
    #Filtra resultados apenas do usuario cadastrado
    def get_queryset(self):
        return Contato.objects.filter(usuario=self.request.user)
    
    #Traz os resultados
    def get_context_data(self, **kwargs):
        
        #campos first_name e last_name são concatenados para facilitar a busca pelo nome completo
        campos_nome = Concat('nome',Value(' '),'sobrenome')
        termo = self.request.GET.get('termo')
        
        context = super().get_context_data(**kwargs)
        
        #Busca feita por nome ou telefone
        contatos_mostrados = self.get_queryset().annotate(
            nomecompleto = campos_nome
            ).filter(
            Q(nomecompleto__icontains=termo) | Q(telefone__icontains=termo),
            mostrar=True,
            )
        #Verifica a quantidade de usuarios e quantas páginas serão necessárias para mostrá-los   
        if contatos_mostrados.exists():#Tambem ocultam os usuarios que estão marcados para não serem mostrados na base admin
            paginator = Paginator(contatos_mostrados,self.paginate_by) 
            page = self.request.GET.get('page')
            context['contatos'] = paginator.get_page(page)
            return context
        else:
            messages.add_message(self.request,messages.INFO,'Nenhum contato encontrado')
            return context
        

#Faz cadastro de novos contatos na agenda
class CadastroContatoView(LoginRequiredMixin,CreateView):

    form_class = CadastroContatoForm
    success_url = reverse_lazy('index')
    template_name = 'cadcontatos'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.save()
        messages.success(self.request,'Cadastro feito com sucesso')
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,'Ocorreu um erro ao cadastrar')
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs
  
#Edita contatos na agenda    
class ContatoUpdateView(LoginRequiredMixin,UpdateView):
    
    model = Contato
    fields = ['nome', 'sobrenome','telefone', 'email','descricao','categoria','foto']
    template_name_suffix = 'editar'
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.save()
        messages.success(self.request,'Contato editado com sucesso')
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,'Erro ao editar, revise os dados')
        return super().form_invalid(form)


#Exclui contatos
class ContatoDeleteView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    
    model = Contato
    success_url = reverse_lazy('index')
    success_message = 'Contato excluído com sucesso'
    

#Mostra categorias cadastradas
class CategoriasListView(LoginRequiredMixin,ListView):
    
    model = Categoria
    paginate_by = 10
    
    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias = self.get_queryset()
        paginator = Paginator(categorias,self.paginate_by)
        page = self.request.GET.get('page')
        context['categorias'] = paginator.get_page(page)
        return context
    

#Cadastro de novas categorias dos contatos da agenda
class CadastroCategoriaView(LoginRequiredMixin,CreateView):

    form_class = CadastroCategoriaForm
    success_url = reverse_lazy('categorias')
    template_name = 'cadcategoria'
    
    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        nome = form.cleaned_data['nome']
        nomes = [nome.upper(),nome.lower(),nome.title(),nome.capitalize()]
        if [nome for nome in nomes if self.get_queryset().filter(nome=nome).exists()]:
            messages.error(self.request,f'Categoria {nome} já existe')
            return super().form_invalid(form)
        else:
            form.save()
            messages.success(self.request,'Cadastro feito com sucesso')
            return super().form_valid(form)

  
#Edita categoria    
class CategoriaUpdateView(LoginRequiredMixin,UpdateView):
    
    model = Categoria
    fields = ['nome']
    template_name_suffix = 'editcategoria'
    success_url = reverse_lazy('categorias')
    
    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)
    
    def form_valid(self, form):
    # Executa a validação personalizada de categoria
        form.instance.usuario = self.request.user
        nome = form.cleaned_data['nome']
        nomes = [nome.upper(),nome.lower(),nome.title(),nome.capitalize()]
        if [nome for nome in nomes if self.get_queryset().filter(nome=nome).exists()]:
            messages.error(self.request,f'Categoria {nome} já existe')
            return super().form_invalid(form)
        else:
            form.save()
            messages.success(self.request,'Categoria editada com sucesso')
            return super().form_valid(form)


#Exclui categoria
class CategoriaDeleteView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    
    model = Categoria
    success_url = reverse_lazy('categorias')
    success_message = "Categoria Excluída com sucesso"

    def form_valid(self, form):
        #Tenta validar a exclusão
        try:
            return super().form_valid(form)
        except ProtectedError:
             # Se houver objetos relacionados com relacionamentos protegidos, redireciona para uma página de erro.
            messages.error(self.request, 'Não é possível excluir esta categoria, pois existem registros relacionados a ela.')
            return redirect('categorias')