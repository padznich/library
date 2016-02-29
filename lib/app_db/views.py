from django.shortcuts import render
from django.http import HttpResponse, Http404
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics #!!!! COOL

from app_db.models import App_db
from app_db.serializers import App_dbSerializer, UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET', 'POST'])
def app_db_list(request, format=None):
    """
    List all code app_db, or create a new app_db.
    """
    if request.method == 'GET':
        app_db = App_db.objects.all()
        serializer = App_dbSerializer(app_db, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = App_dbSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def app_db_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code app_db.
    """
    try:
        app_db = App_db.objects.get(pk=pk)
    except App_db.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = App_dbSerializer(app_db)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = App_dbSerializer(app_db, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        app_db.delete()
        return Response(status=204)


class AppdbList(APIView):
    """
    List all app_db, or create a new app_db.
    """
    def get(self, request, format=None):
        app_db = App_db.objects.all()
        serializer = App_dbSerializer(app_db, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = App_dbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppdbDetail(APIView):
    """
    Retrieve, update or delete a app_db instance.
    """
    def get_object(self, pk):
        try:
            return App_db.objects.get(pk=pk)
        except App_db.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        app_db = self.get_object(pk)
        serializer = App_dbSerializer(app_db)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        app_db = self.get_object(pk)
        serializer = App_dbSerializer(app_db, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        app_db = self.get_object(pk)
        app_db.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetList(generics.ListCreateAPIView):
    queryset = App_db.objects.all()
    serializer_class = App_dbSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = App_db.objects.all()
    serializer_class = App_dbSerializer
