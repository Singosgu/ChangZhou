import traceback
import requests
import datetime
from rest_framework import viewsets
from .models import ListModel
from . import serializers
from utils.page import MyPageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .filter import Filter
from rest_framework.exceptions import APIException
from userprofile.models import Users
from .page import MyPageNumberPaginationWarehouse


class APIViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）

        list:
            Response a data list（all）

        create:
            Create a data line（post）

        delete:
            Delete a data line（delete)

        partial_update:
            Partial_update a data（patch：partial_update）

        update:
            Update a data（put：update）
    """
    pagination_class = MyPageNumberPaginationWarehouse
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
            query_dict = {'is_delete': False}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            if id is not None:
                query_dict['id'] = id
            return ListModel.objects.filter(**query_dict)
        else:
            return ListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return serializers.WarehouseGetSerializer
        elif self.action in ['create']:
            return serializers.WarehousePostSerializer
        elif self.action in ['update']:
            return serializers.WarehouseUpdateSerializer
        elif self.action in ['partial_update']:
            return serializers.WarehousePartialUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data['openid'] = self.request.auth.openid
        if len(data['warehouse_name']) > 45:
            raise APIException({"detail": "The warehouse name is set to more than 45 characters"})
        if ListModel.objects.filter(openid=data['openid'], warehouse_name=data['warehouse_name'],
                                    is_delete=False).exists():
            raise APIException({"detail": "Data Exists"})
        else:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=200, headers=headers)

    def update(self, request, pk):
        qs = self.get_object()
        data = self.request.data
        print(data)
        if len(data['warehouse_name']) > 45:
            raise APIException({"detail": "The warehouse name is set to more than 45 characters"})
        serializer = self.get_serializer(qs, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)

    def partial_update(self, request, pk):
        qs = self.get_object()
        if qs.openid != self.request.auth.openid:
            raise APIException({"detail": "Cannot partial_update data which not yours"})
        else:
            data = self.request.data
            if len(data['warehouse_name']) > 45:
                raise APIException({"detail": "The warehouse name is set to more than 45 characters"})
            serializer = self.get_serializer(qs, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=200, headers=headers)

    def destroy(self, request, pk):
        qs = self.get_object()
        if qs.openid != self.request.auth.openid:
            raise APIException({"detail": "Cannot delete data which not yours"})
        else:
            qs.is_delete = True
            qs.save()
            serializer = self.get_serializer(qs, many=False)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=200, headers=headers)


class GetAllViewSet(viewsets.ModelViewSet):
    pagination_class = MyPageNumberPaginationWarehouse
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
            if id is None:
                return ListModel.objects.filter(is_delete=False)
            else:
                return ListModel.objects.filter(id=id, is_delete=False)
        else:
            return ListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return serializers.WarehouseGetSerializer
        elif self.action in ['create']:
            return serializers.WarehousePostSerializer
        elif self.action in ['update']:
            return serializers.WarehouseUpdateSerializer
        elif self.action in ['partial_update']:
            return serializers.WarehousePartialUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)


class GetOrderViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）

        list:
            Response a data list（all）

        create:
            Create a data line（post）

        delete:
            Delete a data line（delete)

        partial_update:
            Partial_update a data（patch：partial_update）

        update:
            Update a data（put：update）
    """
    pagination_class = MyPageNumberPaginationWarehouse
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
            query_dict = {'is_delete': False}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            if id is not None:
                query_dict['id'] = id
            return ListModel.objects.filter(**query_dict)
        else:
            return ListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.WarehousePostSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'APItoken': 'e7d82-0913c-5fe10-603c2-be99e-a42e9-a837'
        }
        print(data.get('openid', ''))
        pay_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y/%m/%d")
        get_orders = requests.get(
            'https://api.teapplix.com/api2/OrderNotification?NotShipped=0&PageSize=100&WarehouseId=' + str(data.get('warehouse_id', '')) + '&PaymentDateStart=' + pay_day,
            headers=headers).json()
        for i in range(get_orders.get('Pagination', '').get('TotalPages', '')):
            get_order = requests.get(
                'https://api.teapplix.com/api2/OrderNotification?NotShipped=0&PageSize=100&PageNumber=' + str(
                    i + 1) + '&WarehouseId=' + str(data.get('warehouse_id', '')) + '&PaymentDateStart=' + pay_day,
                headers=headers).json().get('Orders')
            for j in get_order:
                print(j)
        return Response({'msg': 'success'}, status=200)
