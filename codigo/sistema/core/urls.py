from django.urls import path
from .views import login_view, dashboard, cadastrar_pessoa

urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('pessoas/cadastrar/', cadastrar_pessoa, name= 'cadastrar_pessoa'),
]