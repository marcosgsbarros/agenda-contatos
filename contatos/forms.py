from django import forms
from contatos.models import Contato,Categoria


class CadastroContatoForm(forms.ModelForm):
    
    class Meta:
        model = Contato
        fields = ['nome', 'sobrenome','telefone', 'email','descricao','categoria','foto']
        
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario is not None:
            # Filtra as categorias para mostrar apenas as do usuário atual
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)

    
class CadastroCategoriaForm(forms.ModelForm):
    
    class Meta:
        model = Categoria
        fields = ['nome']
        
