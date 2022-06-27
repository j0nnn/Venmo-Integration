from django.urls import path

from . import views

app_name = 'queries'
urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cred/', views.cred, name='cred'),
    path('index/', views.index, name='index'),
    path('<int:query_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('create/inp/', views.inp, name='inp'),
    # path('create/loading/', views.loading, name='loading'),
    path('del/<int:query_id>/', views.delete, name='del'),
]
