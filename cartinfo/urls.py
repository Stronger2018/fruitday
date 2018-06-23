# python3
from django.conf.urls import url
from cartinfo import views

urlpatterns= [
    url('^$', views.cart_info),
    url('^addcart/', views.add_cart),
]
