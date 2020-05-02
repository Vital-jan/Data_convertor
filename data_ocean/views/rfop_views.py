from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from data_ocean.models.rfop_models import Rfop
from data_ocean.serializers.rfop_serializers import RfopSerializer
from data_converter.pagination import CustomPagination
from data_ocean.views.views import Views

class RfopView(Views):

    serializer_class = RfopSerializer
    queryset = Rfop.objects.all()
    serializer = RfopSerializer(queryset, many=True)
    pagination_class = CustomPagination

    def get_queryset (self):
        # returns queryset with API parameters:
        #state_id=
        #state= (contains)
        #state_exclude= (not contains)
        #kved_id=
        #kved= (contains)
        #name= (contains)
        #address= (contains)
        #address_exclude= (not contains)

        resp = self.queryset.all()
        print(self.queryset.get(id=1))

        if self.get_parameters (''):

            filter_state_id = self.get_parameters ('state_id', 1)
            filter_state = self.get_parameters ('state')
            filter_state_exclude = self.get_parameters ('state_exclude')
            filter_kved_id = self.get_parameters ('kved_id', 1)
            filter_kved = self.get_parameters ('kved')
            # filter_kvet doesn`t works cause at kved_models.py is: def __str__(self):  return f"КВЕД {self.code}, назва: {self.name}"
            filter_name = self.get_parameters ('name')
            filter_address = self.get_parameters ('address')
            filter_address_exclude = self.get_parameters ('address_exclude')

            if filter_state_id: resp = resp.filter(state_id = filter_state_id)
            if filter_state: resp = resp.filter(state__name__icontains = filter_state)
            if filter_state_exclude: resp = resp.exclude(state__name__icontains = filter_state_exclude)
            if filter_kved_id: resp = resp.filter(kved_id = filter_kved_id)
            if filter_kved: resp = resp.filter(kved__name__icontains = filter_kved)
            if filter_name: resp = resp.filter(fullname__icontains = filter_name)
            if filter_address: resp = resp.filter(address__icontains = filter_address)
            if filter_address_exclude: resp = resp.exclude(address__icontains = filter_address_exclude)

        return resp
        
