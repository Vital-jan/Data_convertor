from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from ratu.models.rfop_models import Rfop
from ratu.models.ruo_models import Ruo
from ratu.serializers import RfopSerializer
from ratu.serializers import RuoSerializer

from rest_framework.generics import GenericAPIView
from data_converter.pagination import CustomPagination

def index(request):
    return HttpResponse("Hello, world. You're at the ratu index.")

class RfopView(GenericAPIView):
    serializer_class = RfopSerializer
    queryset = Rfop.objects.all()
    pagination_class = CustomPagination
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        payload = {
            'return_code': '0000',
            'return_message': 'Success',
            'data': data
        }
        return Response(data)

class RuoView(GenericAPIView):
    serializer_class = RuoSerializer
    queryset = Ruo.objects.all()
    pagination_class = CustomPagination
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        payload = {
            'return_code': '0000',
            'return_message': 'Success',
            'data': data
        }
        return Response(data)
