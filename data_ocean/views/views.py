from rest_framework.generics import GenericAPIView
from data_converter.pagination import CustomPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class Views (GenericAPIView):
    
    def get_parameters (self, param, int_value = 0):
        # returns http request parameter specified <param> or None if <param> not send by http request
        # returns all http request parameters if <param> not defined
        # if <int_value> = 1, validate value of <param> and returns 0, if that's not integer
        if param:
            try:
                resp = self.request.query_params[param]
                if int_value: resp = int(resp)
            except:
                resp = None
            return resp

        return self.request.query_params 


    def get(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        return Response(data)
        
