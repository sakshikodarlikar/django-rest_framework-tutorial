from collections import namedtuple
from django.db import router
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('viewset',views.ArticleViewSet, basename='article_viewset')


urlpatterns = [
    path('viewset/', include(router.urls), name='article_viewset'),    

    #path('article/', views.article_list ,name= 'article_list'),
    path('article/', views.ArticleList.as_view() ,name= 'article_list'),

    #path('detail/<int:pk>/', views.article_detail ,name= 'article_detail'),
    path('detail/<int:pk>/', views.ArticleDetail.as_view() ,name= 'article_detail'),

    path('generic/article/', views.GenericAPIView.as_view() ,name= 'GenericAPIView'),
    path('generic/detail/<int:pk>/', views.GenericDetail.as_view() ,name= 'GenericDetail'),

]
