from django.views.generic import TemplateView,CreateView,View
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CadastroForm,AutenticacaoForm
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import AccessMixin,LoginRequiredMixin
from django.shortcuts import redirect
from django.views.decorators.csrf import requires_csrf_token


#verfica se o usuario está logado
class NonAuthenticatedUserMixin(AccessMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

#Valida o formulario de login
@requires_csrf_token
class LoginView(NonAuthenticatedUserMixin,LoginView):
    
    form_class = AutenticacaoForm
    template_name = 'login'
      
    def form_invalid(self,form):
        
        messages.error(self.request,'Nome de usuário ou senha inválidos')
        return super().form_invalid(form)

  
#Faz logout na página    
class LogoutView(LogoutView):

    next_page = reverse_lazy('login')

#Cadastra novo usuario
class CadastroView(NonAuthenticatedUserMixin,CreateView):

    form_class = CadastroForm
    success_url = reverse_lazy('login')
    template_name = 'cadastro.html'
    
    #Valida formulario de cadastro e mostra mensagem de erro ou sucesso
    def form_valid(self, form):     
        form.save()
        
        messages.success(self.request,'Cadastro feito com sucesso')
        return super().form_valid(form)
    
    def form_invalid(self,form):
        
        messages.error(self.request,'Ocorreu um erro ao cadastrar')
        return super().form_invalid(form)

#Dashboard mostra quem está logado no sistema

class DashboardView(LoginRequiredMixin,TemplateView):
    
    template_name = "dashboard.html"

    #Envia informação do usuario para o template dashboard.html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


