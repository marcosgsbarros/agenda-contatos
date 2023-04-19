from django.contrib import admin
from .models import Contato,Categoria


@admin.register(Contato)
class ContatosAdmin(admin.ModelAdmin):
    list_display = [
        'nome','sobrenome','telefone','email','categoria','data_criacao','mostrar'
    ]
    search_fields = ['nome','sobrenome']
    
    list_editable = ('telefone','mostrar')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

    
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = [
        'nome'
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        #return qs.filter(usuario=request.user)

admin.site.site_header = 'Painel administrador da agenda'
admin.site.site_title = 'Painel'
admin.site.index_title = 'Painel Agenda'
