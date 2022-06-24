from django.urls import path

from . import views

app_name = 'queries'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:query_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('create/inp/', views.inp, name='inp'),

    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
