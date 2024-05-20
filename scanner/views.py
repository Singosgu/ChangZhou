from dateutil.relativedelta import relativedelta
from django.http import StreamingHttpResponse
from django.utils import timezone
from .models import ListModel
from rest_framework import viewsets
from . import serializers
from utils.page import MyPageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filter import Filter
from rest_framework.generics import RetrieveAPIView,GenericAPIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from stock.models import StockBinModel
from dn.models import DnDetailModel
from dn.filter import DnDetailFilter
from userprofile.models import Users


class SannerDnDetailPickingListView(viewsets.ModelViewSet):
    """
        list:
            Response a data list（all）
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnDetailFilter


    def get_project(self):
        try:
            id = self.kwargs.get('pk')
            return id
        except:
            return None

    def get_queryset(self):
        id = self.get_project()
        if self.request.user:
            u = Users.objects.filter(vip=9).first()
            if u is None:
                superopenid = None
            else:
                superopenid = u.openid
            query_dict = {'is_delete': False}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            if id is not None:
                query_dict['id'] = id
            return DnDetailModel.objects.filter(**query_dict)
        else:
            return DnDetailModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return serializers.SannerDnDetailPickingListGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

class ListViewSet(viewsets.ModelViewSet):
    """
        list:
            Response a data list（all）
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = Filter

    def get_project(self):
        try:
            id = self.kwargs.get('pk')
            return id
        except:
            return None

    def get_queryset(self):
        id = self.get_project()
        if self.request.user:
            u = Users.objects.filter(vip=9).first()
            if u is None:
                superopenid = None
            else:
                superopenid = u.openid
            query_dict = {}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            if id is not None:
                query_dict['id'] = id
            return ListModel.objects.filter(**query_dict)
        else:
            return ListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.ListGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)



class SannerView(viewsets.ModelViewSet):
    """
        Retrieve:
            Response a data retrieve
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = Filter
    lookup_field = 'bar_code'
    def get_project(self):
        try:
            bar_code = self.kwargs['bar_code']
            return bar_code
        except:
            return None

    def get_queryset(self):
        bar_code = self.get_project()
        if self.request.user:
            u = Users.objects.filter(vip=9).first()
            if u is None:
                superopenid = None
            else:
                superopenid = u.openid
            query_dict = {}
            query_dict['bar_code'] = bar_code
            qs_list = ListModel.objects.filter(**query_dict)
            if qs_list.exists():
                return qs_list
            else:
                try:
                    ups_mian_dan_code = bar_code.split('420')[1][5:]
                    query_dict['bar_code'] = ups_mian_dan_code
                    return ListModel.objects.filter(**query_dict)
                except:
                    return ListModel.objects.none()
        else:
            return ListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.ListGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)