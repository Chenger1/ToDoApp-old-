from django.urls import path
from .views import *
urlpatterns = [
path('', action_view, name='action_url'),
path('history/', history_view, name='history_url'),
path('create-action/', ActionsAddView.as_view(), name='add_action_url'),
path('create-category/', CategoryAddView.as_view(), name='add_category_url'),
path('registration/', RegisterView.as_view(), name='register_url'),
path('login/', LoginView.as_view(), name='login_url'),
path('logout/', logout_view, name='logout_url'),
path('hidden<slug:slug>/', hidden_view, name='hidden_url'),
path('delete<slug:slug>/', delete_view, name='delete_url'),
path('restore<slug:slug>/', restore_view, name='restore_url'),
path('update<slug:slug>/', UpdateView.as_view(), name='update_url'),
path('category<slug:slug>/', category_view, name='category_url'),
]