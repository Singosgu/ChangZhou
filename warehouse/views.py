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
from django.utils import timezone
from dn.models import DnListModel, DnDetailModel, PickingListModel
from utils.md5 import Md5
from scanner.models import ListModel as scanner
from customer.models import ListModel as customer
from goods.models import ListModel as goods
from utils.datasolve import sumOfList
from stock.models import StockListModel as stocklist
from dn.models import OrderTypeList as ordertype
from dn.models import CarrierList as carrierlist

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
        # pay_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y/%m/%d")
        get_orders = requests.get(
            'https://api.teapplix.com/api2/OrderNotification?DetailLevel=shipping|none|inventory|dropship&NotShipped=1&PageSize=100&WarehouseId=' + str(data.get('warehouse_id', '')),
            headers=headers).json()
        for i in range(get_orders.get('Pagination', '').get('TotalPages', '')):
            get_order = requests.get(
                'https://api.teapplix.com/api2/OrderNotification?DetailLevel=shipping|none|inventory|dropship&NotShipped=1&PageSize=100&PageNumber=' + str(
                    i + 1) + '&WarehouseId=' + str(data.get('warehouse_id', '')),
                headers=headers).json().get('Orders')
            for v in get_order:
                for x in v.get('OrderItems', ''):
                    if goods.objects.filter(goods_code=x.get('ItemSKU', ''), is_delete=False).exists() is False:
                        goods_bar_code = Md5.md5(x.get('ItemSKU', ''))
                        goods.objects.create(
                            goods_code=x.get('ItemSKU', ''),
                            goods_desc='N/A',
                            goods_supplier='N/A',
                            goods_unit='N/A',
                            goods_class='N/A',
                            goods_brand='N/A',
                            goods_color='N/A',
                            goods_shape='N/A',
                            goods_specs='N/A',
                            goods_origin='N/A',
                            creater=self.request.auth.name,
                            bar_code=goods_bar_code,
                            openid=data.get('openid')
                        )
                        scanner.objects.create(openid=data.get('openid', ''), mode="GOODS", code=x.get('ItemSKU', ''),
                                               bar_code=goods_bar_code)
            for j in get_order:
                qs_set = DnListModel.objects.filter(is_delete=False)
                order_day = str(timezone.now().strftime('%Y%m%d'))
                if len(qs_set) > 0:
                    dn_last_code = qs_set.order_by('-id').first().dn_code
                    if dn_last_code[2:10] == order_day:
                        order_create_no = str(int(dn_last_code[10:]) + 1)
                        dn_code = 'DN' + order_day + order_create_no
                    else:
                        dn_code = 'DN' + order_day + '1'
                else:
                    dn_code = 'DN' + order_day + '1'
                bar_code = Md5.md5(str(j.get('TxnId', '')))
                if DnListModel.objects.filter(txnid=j.get('TxnId', ''), is_delete=False).exists() is False:
                    total_weight_list = []
                    total_volume_list = []
                    total_cost_list = []
                    priority = 1
                    if j.get('ShippingDetails', '')[0].get('Package', '').get('Method', '') != 'SpecialShip':
                        priority = 2
                    for p in j.get('OrderItems', ''):
                        goods_detail = goods.objects.filter(goods_code=p.get('ItemSKU', '')).first()
                        total_weight_list.append(round(goods_detail.goods_weight * int(p.get('Quantity', '')) / 1000, 4))
                        total_volume_list.append(round(goods_detail.unit_volume * int(p.get('Quantity', '')) / 1000 / 1000 / 1000, 4))
                        total_cost_list.append(round(goods_detail.goods_price * int(p.get('Quantity', '')), 2))
                    order_line = 1
                    if len(j.get('OrderItems', '')) == 1 and j.get('OrderItems', '')[0].get('Quantity', '') == 1:
                        order_line = 1
                    else:
                        order_line = 2
                    DnListModel.objects.create(
                        txnid=j.get('TxnId', ''),
                        order_line=order_line,
                        order_type=j.get('ShippingDetails', '')[0].get('Package', '').get('Method', ''),
                        tp_detail=j,
                        dn_code=dn_code,
                        total_weight=sumOfList(total_weight_list, len(total_weight_list)),
                        total_volume=sumOfList(total_volume_list, len(total_volume_list)),
                        total_cost=sumOfList(total_cost_list, len(total_cost_list)),
                        customer=j.get('To', '').get('Name', ''),
                        creater=self.request.auth.name,
                        bar_code=bar_code,
                        openid=data.get('openid', ''),
                        priority=priority,
                        warehouse_id=int(data.get('warehouse_id', ''))
                    ),
                    if customer.objects.filter(openid=data.get('openid', ''), customer_name=j.get('To', '').get('Name', ''), is_delete=False).exists() is False:
                        customer.objects.create(
                            openid=data.get('openid', ''),
                            customer_name=j.get('To', '').get('Name', ''),
                            customer_city=j.get('To', '').get('City', ''),
                            customer_address=j.get('To', '').get('Street', '') + j.get('To', '').get('Street2', ''),
                            customer_contact=j.get('To', '').get('PhoneNumber', ''),
                            customer_manager=j.get('To', '').get('Email', ''),
                            creater=self.request.auth.name
                        )
                    for k in j.get('OrderItems', ''):
                        goods_detail = goods.objects.filter(goods_code=k.get('ItemSKU', '')).first()
                        DnDetailModel.objects.create(
                            openid=data.get('openid', ''),
                            txnid=j.get('TxnId', ''),
                            order_line=order_line,
                            order_type=j.get('ShippingDetails', '')[0].get('Package', '').get('Method', ''),
                            dn_code=dn_code,
                            customer=j.get('To', '').get('Name', ''),
                            goods_code=goods_detail.goods_code,
                            goods_desc=goods_detail.goods_desc,
                            goods_qty=k.get('Quantity', ''),
                            goods_weight=round(goods_detail.goods_weight * k.get('Quantity') / 1000, 4),
                            goods_volume=round(goods_detail.unit_volume * k.get('Quantity') / 1000 / 1000 / 1000, 4),
                            goods_cost=round(goods_detail.goods_price * k.get('Quantity'), 2),
                            creater=self.request.auth.name,
                            priority=priority,
                            warehouse_id=int(data.get('warehouse_id', ''))
                        )
                        if carrierlist.objects.filter().exists() is False:
                            carrierlist.objects.create(
                                carrier=j.get('ShippingDetails', '')[0].get('Package', '').get('TrackingInfo', '').get('CarrierName', '')
                            )
                        if ordertype.objects.filter().exists() is False:
                            ordertype.objects.create(
                                order_type=j.get('ShippingDetails', '')[0].get('Package', '').get('Method', '')
                            )
                        if stocklist.objects.filter(
                                openid=data.get('openid', ''),
                                goods_code=goods_detail.goods_code,
                                can_order_stock__gte=0
                        ).exists():
                            goods_qty_change = stocklist.objects.filter(
                                openid=data.get('openid'),
                                goods_code=goods_detail.goods_code
                            ).first()
                            goods_qty_change.dn_stock = goods_qty_change.dn_stock + int(k.get('Quantity'))
                            goods_qty_change.save()
                        else:
                            stocklist.objects.create(
                                openid=data.get('openid'),
                                goods_code=goods_detail.goods_code,
                                goods_desc=goods_detail.goods_desc,
                                dn_stock=int(k.get('Quantity'))
                            )
                    scanner.objects.create(openid=data.get('openid', ''), mode="DN", code=dn_code, bar_code=bar_code)
        return Response({'msg': 'success'}, status=200)
