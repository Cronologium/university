from django.conf.urls import url
import views
import algorithms

app_name = 'lab1'
urlpatterns = [
    url(r'^lab1$', views.template_lab1, name='Lab1'),
    url(r'^lab1/belaso/encryption$', algorithms.belaso_encrypt, name='Belaso encryption'),
    url(r'^lab1/belaso/decryption$', algorithms.belaso_decrypt, name='Belaso decryption'),
    
]