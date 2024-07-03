from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_material, name='upload_material'),
    path('search/', views.search_materials, name='search_materials'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('logout/', views.logout, name='logout'),
    path('chatbot/response/', views.chatbot, name='chatbot_response'),
]
