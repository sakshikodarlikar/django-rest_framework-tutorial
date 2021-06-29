from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import permissions
from .models import *
from .serializers import *
from django.http import JsonResponse,HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


#Generic Viewsets
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


""" 
class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = Article.objects.all()
    serializer_class  = ArticleSerializer

 """

#Viewsets
""" 
class ArticleViewSet(viewsets.ViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def list(self,request):
        articles = Article.objects.all()
        serialize = ArticleSerializer(articles, many=True)
        return Response(serialize.data)

    def create(self,request):
        serialize = ArticleSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None):
        articles = Article.objects.all()
        article = get_object_or_404(articles,pk=pk)
        serialize = ArticleSerializer(article)
        return Response(serialize.data)

    def update(self,request,pk=None):
        articles = Article.objects.all()
        article = get_object_or_404(articles,pk=pk)
        serialize = ArticleSerializer(article,data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        articles = Article.objects.all()
        article = get_object_or_404(articles,pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  """

#Generic API
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Article.objects.all()
    serializer_class  = ArticleSerializer

    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class GenericDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = Article.objects.all()
    serializer_class  = ArticleSerializer

    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]


    def get(self,request,pk=None):
        return self.retrieve(request,pk)

    def put(self,request,pk=None):
        return self.update(request,pk)

    def delete(self,request,pk=None):
        return self.destroy(request,pk)


# Class Based API View 
class ArticleList(APIView):
    def get(self,request):
        articles = Article.objects.all()
        serialize = ArticleSerializer(articles, many=True)
        return Response(serialize.data)

    def post(self,request):
        serialize = ArticleSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

class ArticleDetail(APIView):
    def get_object(self,pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,pk):
        article = self.get_object(pk)
        serialize = ArticleSerializer(article)
        return Response(serialize.data)

    def put(self,request,pk):
        article = self.get_object(pk)  
        serialize = ArticleSerializer(article,data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Function Based View
@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serialize = ArticleSerializer(articles, many=True)
        return Response(serialize.data)
    
    elif request.method == 'POST':
        serialize = ArticleSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialize = ArticleSerializer(article)
        return Response(serialize.data)

    if request.method == 'PUT':
        serialize = ArticleSerializer(article,data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



 