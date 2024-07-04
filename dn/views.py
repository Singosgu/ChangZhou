from dateutil.relativedelta import relativedelta
from rest_framework import viewsets
from .models import DnListModel, DnDetailModel, PickingListModel, PickingSumModel, CarrierList
from . import serializers
from .page import MyPageNumberPaginationDNList, MyPageNumberPaginationDNDetail, MyPageNumberPaginationPicking
from utils.page import MyPageNumberPagination
from utils.datasolve import sumOfList, transportation_calculate
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .filter import DnListFilter, DnDetailFilter, DnPickingListFilter, DnPickingSumFilter
from rest_framework.exceptions import APIException
from customer.models import ListModel as customer
from warehouse.models import ListModel as warehouse
from binset.models import ListModel as binset
from goods.models import ListModel as goods
from payment.models import TransportationFeeListModel as transportation
from stock.models import StockListModel as stocklist
from stock.models import StockBinModel as stockbin
from driver.models import ListModel as driverlist
from driver.models import DispatchListModel as driverdispatch
from scanner.models import ListModel as scanner
from cyclecount.models import QTYRecorder as qtychangerecorder
from cyclecount.models import CyclecountModeDayModel as cyclecount
from django.db.models import Q
from django.db.models import Sum
from utils.md5 import Md5
import re, random
from .serializers import FileListRenderSerializer, FileDetailRenderSerializer
from django.http import StreamingHttpResponse, JsonResponse
from django.utils import timezone
from .files import FileListRenderCN, FileListRenderEN, FileDetailRenderCN, FileDetailRenderEN, PickListRenderCN, PickListRenderEN
from rest_framework.settings import api_settings
from staff.models import ListModel as staff
from userprofile.models import Users
from django.db.models import Sum


class DnListViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）

        list:
            Response a data list（all）

        create:
            Create a data line（post）

        delete:
            Delete a data line（delete)

    """
    pagination_class = MyPageNumberPaginationDNList
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

    def get_project(self):
        try:
            id = self.kwargs.get('pk')
            return id
        except:
            return None

    def get_queryset(self):
        id = self.get_project()
        if self.request.user:
            empty_qs = DnListModel.objects.filter(
                Q(openid=self.request.auth.openid, dn_status=1, is_delete=False) & Q(customer=''))
            cur_date = timezone.now()
            date_check = relativedelta(day=1)
            if len(empty_qs) > 0:
                for i in range(len(empty_qs)):
                    if empty_qs[i].create_time <= cur_date - date_check:
                        empty_qs[i].delete()
            vip_level = self.request.auth.vip
            query_dict = {'is_delete': False}
            if vip_level == 9:
                pass
            else:
                query_dict['openid'] = self.request.auth.openid
            if id is not None:
                query_dict['id'] = id
            txnid_search = self.request.GET.get('txnid__in', '')
            if txnid_search:
                query_dict['txnid__in'] = txnid_search.split(',')
            order_type_search = self.request.GET.get('order_type_search', '')
            if order_type_search:
                query_dict['order_type'] = order_type_search
            order_line_search = self.request.GET.get('order_line', '')
            if order_line_search:
                query_dict['order_line'] = int(order_line_search)
            carrier_search = self.request.GET.get('carrier', '')
            if carrier_search:
                query_dict['carrier'] = carrier_search
            list_qs = DnListModel.objects.filter(Q(**query_dict) & ~Q(customer=''))
            sku_search = self.request.GET.get('sku_search__in', '')
            if sku_search:
                query_dict['goods_code__in'] = sku_search.split(',')
                detail_qs = DnDetailModel.objects.filter(Q(**query_dict) & ~Q(customer=''))
                check_txnid = []
                for x in detail_qs:
                    if x.txnid != '':
                        if x.txnid in check_txnid:
                            pass
                        else:
                            if list_qs.filter(txnid=x.txnid).exists() is False:
                                check_txnid.append(x.txnid)
                if len(check_txnid) > 0:
                    new_list_qs = DnListModel.objects.filter(txnid__in=check_txnid)
                    result = list_qs | new_list_qs
                else:
                    result = list_qs
            else:
                result = list_qs
            return result.order_by('-update_time')
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return serializers.DNListGetSerializer
        elif self.action in ['create']:
            return serializers.DNListPostSerializer
        elif self.action in ['update']:
            return serializers.DNListUpdateSerializer
        elif self.action in ['partial_update']:
            return serializers.DNListPartialUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data['openid'] = self.request.auth.openid
        custom_dn = self.request.GET.get('custom_dn', '')
        if custom_dn:
            data['dn_code'] = custom_dn
        else:
            qs_set = DnListModel.objects.filter(is_delete=False)
            order_day =str(timezone.now().strftime('%Y%m%d'))
            if len(qs_set) > 0:
                dn_last_code = qs_set.order_by('-id').first().dn_code
                if dn_last_code[2:10] == order_day:
                    order_create_no = str(int(dn_last_code[10:]) + 1)
                    data['dn_code'] = 'DN' + order_day + order_create_no
                else:
                    data['dn_code'] = 'DN' + order_day + '1'
            else:
                data['dn_code'] = 'DN' + order_day + '1'
        data['bar_code'] = Md5.md5(str(data['dn_code']))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        scanner.objects.create(openid=self.request.auth.openid, mode="DN", code=data['dn_code'],
                               bar_code=data['bar_code'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)

    def destroy(self, request, pk):
        qs = self.get_object()
        # if qs.openid != self.request.auth.openid:
        #     raise APIException({"detail": "Cannot delete data which not yours"})
        vip_level = self.request.auth.vip
        if vip_level != 9:
            raise APIException({"detail": "Please switch to all warehouse for operation"})
        if qs.dn_status == 1:
            qs.is_delete = True
            dn_detail_list = DnDetailModel.objects.filter(openid=qs.openid, dn_code=qs.dn_code,
                                          dn_status=1, is_delete=False)
            for i in range(len(dn_detail_list)):
                goods_qty_change = stocklist.objects.filter(openid=qs.openid,
                                                            goods_code=str(dn_detail_list[i].goods_code)).first()
                goods_qty_change.dn_stock = goods_qty_change.dn_stock - int(dn_detail_list[i].goods_qty)
                dn_detail_list[i].is_delete = True
                dn_detail_list[i].save()
                goods_qty_change.save()
            qs.save()
            return Response({"detail": "success"}, status=200)
        else:
            raise APIException({"detail": "This order has Confirmed or Deliveried"})

class DnDetailViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）

        list:
            Response a data list（all）

        create:
            Create a data line（post）

        update:
            Update a data（put：update）
    """
    pagination_class = MyPageNumberPaginationDNDetail
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
            return serializers.DNDetailGetSerializer
        elif self.action in ['create']:
            return serializers.DNDetailPostSerializer
        elif self.action in ['update']:
            return serializers.DNDetailUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        vip_level = self.request.auth.vip
        if vip_level == 9:
            raise APIException({"detail": "总管理员不可以生成拣货单"})

        if DnListModel.objects.filter(openid=self.request.auth.openid, dn_code=str(data['dn_code']), is_delete=False).exists():
            if customer.objects.filter(customer_name=str(data['customer']), is_delete=False).exists():
                staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                                  id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
                for i in range(len(data['goods_code'])):
                    if goods.objects.filter(goods_code=str(data['goods_code'][i]), is_delete=False).exists():
                        check_data = {
                            'openid': self.request.auth.openid,
                            'dn_code': str(data['dn_code']),
                            'customer': str(data['customer']),
                            'goods_code': str(data['goods_code'][i]),
                            'goods_qty': int(data['goods_qty'][i]),
                            'creater': str(staff_name)
                        }
                        serializer = self.get_serializer(data=check_data)
                        serializer.is_valid(raise_exception=True)
                    else:
                        raise APIException({"detail": str(data['goods_code'][i]) + " does not exists"})
                post_data_list = []
                weight_list = []
                volume_list = []
                cost_list = []
                for j in range(len(data['goods_code'])):
                    goods_detail = goods.objects.filter(goods_code=str(data['goods_code'][j]), is_delete=False).first()
                    goods_weight = round(goods_detail.goods_weight * int(data['goods_qty'][j]) / 1000, 4)
                    goods_volume = round(goods_detail.unit_volume * int(data['goods_qty'][j]), 4)
                    goods_cost = round(goods_detail.goods_price * int(data['goods_qty'][j]), 2)
                    if stocklist.objects.filter(openid=self.request.auth.openid, goods_code=str(data['goods_code'][j]),
                                                can_order_stock__gte=0).exists():
                        goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                                    goods_code=str(data['goods_code'][j])).first()
                        goods_qty_change.dn_stock = goods_qty_change.dn_stock + int(data['goods_qty'][j])
                        goods_qty_change.save()
                    else:
                        stocklist.objects.create(openid=self.request.auth.openid,
                                                 goods_code=str(data['goods_code'][j]),
                                                 goods_desc=goods_detail.goods_desc,
                                                 dn_stock=int(data['goods_qty'][j]))
                    post_data = DnDetailModel(openid=self.request.auth.openid,
                                              dn_code=str(data['dn_code']),
                                              customer=str(data['customer']),
                                              goods_code=str(data['goods_code'][j]),
                                              goods_desc=str(goods_detail.goods_desc),
                                              goods_qty=int(data['goods_qty'][j]),
                                              goods_weight=goods_weight,
                                              goods_volume=goods_volume,
                                              goods_cost=goods_cost,
                                              creater=str(staff_name))
                    weight_list.append(goods_weight)
                    volume_list.append(goods_volume)
                    cost_list.append(goods_cost)
                    post_data_list.append(post_data)
                total_weight = sumOfList(weight_list, len(weight_list))
                total_volume = sumOfList(volume_list, len(volume_list))
                total_cost = sumOfList(cost_list, len(cost_list))
                customer_city = customer.objects.filter(customer_name=str(data['customer']), is_delete=False).first().customer_city
                warehouse_city = warehouse.objects.filter(openid=self.request.auth.openid).first().warehouse_city
                transportation_fee = transportation.objects.filter(
                    Q(openid=self.request.auth.openid, send_city__icontains=warehouse_city, receiver_city__icontains=customer_city,
                      is_delete=False) | Q(openid='init_data', send_city__icontains=warehouse_city, receiver_city__icontains=customer_city,
                                           is_delete=False))
                transportation_res = {
                    "detail": []
                }
                if len(transportation_fee) >= 1:
                    transportation_list = []
                    for k in range(len(transportation_fee)):
                        transportation_cost = transportation_calculate(total_weight,
                                                                       total_volume,
                                                                       transportation_fee[k].weight_fee,
                                                                       transportation_fee[k].volume_fee,
                                                                       transportation_fee[k].min_payment)
                        transportation_detail = {
                            "transportation_supplier": transportation_fee[k].transportation_supplier,
                            "transportation_cost": transportation_cost
                        }
                        transportation_list.append(transportation_detail)
                    transportation_res['detail'] = transportation_list
                DnDetailModel.objects.bulk_create(post_data_list, batch_size=100)
                DnListModel.objects.filter(openid=self.request.auth.openid, dn_code=str(data['dn_code'])).update(
                    customer=str(data['customer']), total_weight=total_weight, total_volume=total_volume,
                    total_cost=total_cost, transportation_fee=transportation_res)
                return Response({"detail": "success"}, status=200)
            else:
                raise APIException({"detail": "customer does not exists"})
        else:
            raise APIException({"detail": "DN Code does not exists"})

    def update(self, request, *args, **kwargs):
        data = self.request.data
        if DnListModel.objects.filter(openid=self.request.auth.openid, dn_code=str(data['dn_code']),
                                       dn_status=1, is_delete=False).exists():
            if customer.objects.filter(customer_name=str(data['customer']), is_delete=False).exists():
                staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                                  id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
                for i in range(len(data['goods_code'])):
                    check_data = {
                        'openid': self.request.auth.openid,
                        'dn_code': str(data['dn_code']),
                        'customer': str(data['customer']),
                        'goods_code': str(data['goods_code'][i]),
                        'goods_qty': int(data['goods_qty'][i]),
                        'creater': str(staff_name)
                    }
                    serializer = self.get_serializer(data=check_data)
                    serializer.is_valid(raise_exception=True)
                dn_detail_list = DnDetailModel.objects.filter(openid=self.request.auth.openid,
                                              dn_code=str(data['dn_code']), is_delete=False)
                for v in range(len(dn_detail_list)):
                    goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                                goods_code=str(dn_detail_list[v].goods_code)).first()
                    goods_qty_change.dn_stock = goods_qty_change.dn_stock - dn_detail_list[v].goods_qty
                    if goods_qty_change.dn_stock < 0:
                        goods_qty_change.dn_stock = 0
                    goods_qty_change.save()
                    dn_detail_list[v].is_delete = True
                    dn_detail_list[v].save()
                post_data_list = []
                weight_list = []
                volume_list = []
                cost_list = []
                for j in range(len(data['goods_code'])):
                    goods_detail = goods.objects.filter(goods_code=str(data['goods_code'][j]), is_delete=False).first()
                    goods_weight = round(goods_detail.goods_weight * int(data['goods_qty'][j]) / 1000, 4)
                    goods_volume = round(goods_detail.unit_volume * int(data['goods_qty'][j]), 4)
                    goods_cost = round(goods_detail.goods_price * int(data['goods_qty'][j]), 2)
                    if stocklist.objects.filter(openid=self.request.auth.openid, goods_code=str(data['goods_code'][j]),
                                                can_order_stock__gt=0).exists():
                        goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                                    goods_code=str(data['goods_code'][j])).first()
                        goods_qty_change.dn_stock = goods_qty_change.dn_stock + int(data['goods_qty'][j])
                        goods_qty_change.save()
                    else:
                        stocklist.objects.create(openid=self.request.auth.openid,
                                                 goods_code=str(data['goods_code'][j]),
                                                 goods_desc=goods_detail.goods_desc,
                                                 dn_stock=int(data['goods_qty'][j]))
                    post_data = DnDetailModel(openid=self.request.auth.openid,
                                              dn_code=str(data['dn_code']),
                                              customer=str(data['customer']),
                                              goods_code=str(data['goods_code'][j]),
                                              goods_desc=str(goods_detail.goods_desc),
                                              goods_qty=int(data['goods_qty'][j]),
                                              goods_weight=goods_weight,
                                              goods_volume=goods_volume,
                                              goods_cost=goods_cost,
                                              creater=str(staff_name))
                    weight_list.append(goods_weight)
                    volume_list.append(goods_volume)
                    cost_list.append(goods_cost)
                    post_data_list.append(post_data)
                total_weight = sumOfList(weight_list, len(weight_list))
                total_volume = sumOfList(volume_list, len(volume_list))
                total_cost = sumOfList(cost_list, len(cost_list))
                customer_city = customer.objects.filter(customer_name=str(data['customer']), is_delete=False).first().customer_city
                warehouse_city = warehouse.objects.filter(openid=self.request.auth.openid).first().warehouse_city
                transportation_fee = transportation.objects.filter(
                    Q(openid=self.request.auth.openid, send_city__icontains=warehouse_city,
                      receiver_city__icontains=customer_city,
                      is_delete=False) | Q(openid='init_data', send_city__icontains=warehouse_city,
                                           receiver_city__icontains=customer_city,
                                           is_delete=False))
                transportation_res = {
                    "detail": []
                }
                if len(transportation_fee) >= 1:
                    transportation_list = []
                    for k in range(len(transportation_fee)):
                        transportation_cost = transportation_calculate(total_weight,
                                                                       total_volume,
                                                                       transportation_fee[k].weight_fee,
                                                                       transportation_fee[k].volume_fee,
                                                                       transportation_fee[k].min_payment)
                        transportation_detail = {
                            "transportation_supplier": transportation_fee[k].transportation_supplier,
                            "transportation_cost": transportation_cost
                        }
                        transportation_list.append(transportation_detail)
                    transportation_res['detail'] = transportation_list
                DnDetailModel.objects.bulk_create(post_data_list, batch_size=100)
                DnListModel.objects.filter(openid=self.request.auth.openid, dn_code=str(data['dn_code'])).update(
                    customer=str(data['customer']), total_weight=total_weight, total_volume=total_volume,
                    total_cost=total_cost, transportation_fee=transportation_res)
                return Response({"detail": "success"}, status=200)
            else:
                raise APIException({"detail": "Customer does not exists"})
        else:
            raise APIException({"detail": "DN Code has been Confirmed or does not exists"})

    def destroy(self, request, pk):
        qs = self.get_object()
        if qs.openid != self.request.auth.openid:
            raise APIException({"detail": "Cannot delete data which not yours"})
        else:
            if qs.dn_status == 2 and qs.back_order_label:
                qs.is_delete = True
                goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                            goods_code=str(qs.goods_code)).first()
                goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - int(qs.goods_qty)
                goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - int(qs.goods_qty)
                goods_qty_change.save()
                qs.save()
                if DnDetailModel.objects.filter(openid=self.request.auth.openid, dn_code=qs.dn_code, is_delete=False).exists():
                    pass
                else:
                    DnListModel.objects.filter(openid=self.request.auth.openid, dn_code=qs.dn_code).update(is_delete=True)
                return Response({"detail": "success"}, status=200)
            else:
                raise APIException({"detail": "This order has Confirmed or Deliveried"})

class DnViewPrintViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）
    """
    serializer_class = serializers.DNListGetSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

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
            return DnListModel.objects.filter(**query_dict)
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return serializers.DNDetailGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def retrieve(self, request, pk):
        qs = self.get_object()
        u = Users.objects.filter(vip=9).first()
        if u is None:
            superopenid = None
        else:
            superopenid = u.openid
        openid = {}
        if self.request.auth.openid != superopenid:
            openid['openid'] = self.request.auth.openid
        if qs.openid != self.request.auth.openid and self.request.auth.openid != superopenid:
            raise APIException({"detail": "Cannot update data which not yours"})
        else:
            context = {}
            dn_detail_list = DnDetailModel.objects.filter(**openid,
                                                          dn_code=qs.dn_code,
                                                          is_delete=False)
            dn_detail = serializers.DNDetailGetSerializer(dn_detail_list, many=True)
            customer_detail = customer.objects.filter(customer_name=qs.customer).first()
            warehouse_detail = warehouse.objects.filter(**openid).first()
            context['dn_detail'] = dn_detail.data
            context['customer_detail'] = {
                "customer_name": customer_detail.customer_name,
                "customer_city": customer_detail.customer_city,
                "customer_address": customer_detail.customer_address,
                "customer_contact": customer_detail.customer_contact
            }
            context['warehouse_detail'] = {
                "warehouse_name": warehouse_detail.warehouse_name,
                "warehouse_city": warehouse_detail.warehouse_city,
                "warehouse_address": warehouse_detail.warehouse_address,
                "warehouse_contact": warehouse_detail.warehouse_contact
            }
        return Response(context, status=200)

class DnNewOrderViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

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
            return DnListModel.objects.filter(**query_dict)
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DNListPartialUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, pk):
        qs = self.get_object()
        if qs.openid != self.request.auth.openid:
            raise APIException({"detail": "Cannot delete data which not yours"})
        else:
            if qs.dn_status == 1:
                if DnDetailModel.objects.filter(openid=self.request.auth.openid, dn_code=qs.dn_code,
                                                                dn_status=1, is_delete=False).exists():
                    qs.dn_status = 2
                    dn_detail_list = DnDetailModel.objects.filter(openid=self.request.auth.openid, dn_code=qs.dn_code,
                                                                    dn_status=1, is_delete=False)
                    for i in range(len(dn_detail_list)):
                        if stocklist.objects.filter(openid=self.request.auth.openid,
                                                                    goods_code=str(dn_detail_list[i].goods_code)).exists():
                            pass
                        else:
                            goods_detail = goods.objects.filter(goods_code=str(dn_detail_list[i].goods_code)).first()
                            stocklist.objects.create(openid=self.request.auth.openid,
                                                     goods_code=str(dn_detail_list[i].goods_code),
                                                     goods_desc=goods_detail.goods_desc,
                                                     supplier=goods_detail.goods_supplier)
                        goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                                    goods_code=str(
                                                                        dn_detail_list[i].goods_code)).first()
                        goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - dn_detail_list[i].goods_qty
                        goods_qty_change.ordered_stock = goods_qty_change.ordered_stock + dn_detail_list[i].goods_qty
                        goods_qty_change.dn_stock = goods_qty_change.dn_stock - dn_detail_list[i].goods_qty
                        if goods_qty_change.can_order_stock < 0:
                            goods_qty_change.can_order_stock = 0
                        goods_qty_change.save()
                    dn_detail_list.update(dn_status=2)
                    qs.save()
                    serializer = self.get_serializer(qs, many=False)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=200, headers=headers)
                else:
                    raise APIException({"detail": "Please Enter The DN Detail"})
            else:
                raise APIException({"detail": "This DN Status Is Not Pre Order"})

class DnOrderReleaseViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）
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
            query_dict = {'dn_status': 2, 'have_mian_dan': True, 'is_delete': False}
            vip_level = self.request.auth.vip
            if vip_level == 9:
                raise APIException({'detail': '管理员不可以生成拣货单'})
            else:
                query_dict['openid'] = self.request.auth.openid
            if id is not None:
                query_dict['id'] = id
            return DnDetailModel.objects.filter(**query_dict)
        else:
            return DnDetailModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DNDetailGetSerializer
        elif self.action in ['update']:
            return serializers.DNDetailGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        dn_detail_list = self.filter_queryset(self.get_queryset())
        staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                          id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
        picking_list = []
        picking_list_label = 0
        back_order_list = []
        back_order_list_label = 0
        back_order_goods_weight_list = []
        back_order_goods_volume_list = []
        back_order_goods_cost_list = []
        back_order_base_code = DnListModel.objects.filter(is_delete=False).order_by('-id').first().dn_code
        dn_last_code = re.findall(r'\d+', str(back_order_base_code), re.IGNORECASE)
        back_order_dn_code = 'DN' + str(int(dn_last_code[0]) + 1).zfill(8)
        bar_code = Md5.md5(back_order_dn_code)
        for i in range(len(dn_detail_list)):
            qs = DnListModel.objects.filter(openid=self.request.auth.openid, dn_code=dn_detail_list[i].dn_code,
                                            is_delete=False).first()
            qs.dn_status = 3
            qs.save()
            total_weight = qs.total_weight
            total_volume = qs.total_volume
            total_cost = qs.total_cost
            goods_detail = goods.objects.filter(
                                                goods_code=str(dn_detail_list[i].goods_code),
                                                is_delete=False).first()
            if stocklist.objects.filter(openid=self.request.auth.openid,
                                        goods_code=str(dn_detail_list[i].goods_code)).exists() is False:
                stocklist.objects.create(openid=self.request.auth.openid,
                                         goods_code=str(goods_detail.goods_code),
                                         goods_desc=goods_detail.goods_desc,
                                         dn_stock=int(dn_detail_list[i].goods_qty))
            goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                        goods_code=str(
                                                            dn_detail_list[i].goods_code)).first()
            goods_bin_stock_list = stockbin.objects.filter(openid=self.request.auth.openid,
                                                           goods_code=str(dn_detail_list[i].goods_code),
                                                           bin_property="Normal", goods_qty__gt=0).order_by('bin_level')
            can_pick_qty = goods_qty_change.onhand_stock - \
                           goods_qty_change.inspect_stock - \
                           goods_qty_change.hold_stock - \
                           goods_qty_change.damage_stock - \
                           goods_qty_change.pick_stock
            if can_pick_qty > 0:
                if dn_detail_list[i].goods_qty > can_pick_qty:
                    if qs.back_order_label is False:
                        dn_pick_qty = dn_detail_list[i].pick_qty
                        for j in range(len(goods_bin_stock_list)):
                            bin_can_pick_qty = goods_bin_stock_list[j].goods_qty - \
                                               goods_bin_stock_list[j].pick_qty
                            if bin_can_pick_qty > 0:
                                goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[j].pick_qty + bin_can_pick_qty
                                goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                picking_sum = PickingSumModel.objects.filter(openid=self.request.auth.openid, txnid=dn_detail_list[i].txnid)
                                if picking_sum.exists() is False:
                                    bar_code = Md5.md5(str(dn_detail_list[i].txnid) + str(random.randint(1, 9999)))
                                    PickingSumModel.objects.create(openid=self.request.auth.openid,
                                                                   txnid=dn_detail_list[i].txnid,
                                                                   order_line=dn_detail_list[i].order_line,
                                                                   order_type=dn_detail_list[i].order_type,
                                                                   trackingnumber=dn_detail_list[i].trackingnumber,
                                                                   carrier=dn_detail_list[i].carrier,
                                                                   mian_dan=dn_detail_list[i].mian_dan,
                                                                   have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                   dn_code=dn_detail_list[i].dn_code,
                                                                   creater=str(staff_name),
                                                                   bar_code=bar_code
                                                                   )
                                    scanner.objects.create(openid='SCANGOODS', mode="PSUM",
                                                           code=dn_detail_list[i].txnid,
                                                           bar_code=bar_code)
                                picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                     txnid=dn_detail_list[i].txnid,
                                                                     order_line=dn_detail_list[i].order_line,
                                                                     order_type=dn_detail_list[i].order_type,
                                                                     trackingnumber=dn_detail_list[i].trackingnumber,
                                                                     carrier=dn_detail_list[i].carrier,
                                                                     mian_dan=dn_detail_list[i].mian_dan,
                                                                     have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                     dn_code=dn_detail_list[i].dn_code,
                                                                     bin_name=goods_bin_stock_list[j].bin_name,
                                                                     goods_code=goods_bin_stock_list[j].goods_code,
                                                                     pick_qty=bin_can_pick_qty,
                                                                     creater=str(staff_name),
                                                                     t_code=goods_bin_stock_list[j].t_code))
                                scanner.objects.create(openid='SCANGOODS', mode="PLIST",
                                                       code=dn_detail_list[i].txnid,
                                                       bar_code=Md5.md5(
                                                           str(dn_detail_list[i].txnid) + str(random.randint(1, 9999))))
                                picking_list_label = 1
                                dn_pick_qty = dn_pick_qty + bin_can_pick_qty
                                goods_qty_change.save()
                                goods_bin_stock_list[j].save()
                            elif bin_can_pick_qty == 0:
                                continue
                            else:
                                continue
                        dn_detail_list[i].pick_qty = dn_pick_qty
                        dn_back_order_qty = dn_detail_list[i].goods_qty - \
                                            dn_detail_list[i].pick_qty
                        goods_qty_change.back_order_stock = dn_detail_list[i].goods_qty - can_pick_qty
                        dn_detail_list[i].goods_qty = dn_pick_qty
                        dn_detail_list[i].dn_status = 3
                        back_order_goods_volume = round(goods_detail.unit_volume * dn_back_order_qty, 4)
                        back_order_goods_weight = round(
                            (goods_detail.goods_weight * dn_back_order_qty) / 1000, 4)
                        back_order_goods_cost = round(goods_detail.goods_price * dn_back_order_qty, 2)
                        back_order_list.append(DnDetailModel(dn_code=back_order_dn_code,
                                                             dn_status=2,
                                                             customer=qs.customer,
                                                             goods_code=dn_detail_list[i].goods_code,
                                                             goods_desc=dn_detail_list[i].goods_desc,
                                                             goods_qty=dn_back_order_qty,
                                                             goods_weight=back_order_goods_weight,
                                                             goods_volume=back_order_goods_volume,
                                                             goods_cost=back_order_goods_cost,
                                                             creater=str(staff_name),
                                                             back_order_label=True,
                                                             openid=self.request.auth.openid,
                                                             create_time=dn_detail_list[i].create_time))
                        back_order_list_label = 1
                        total_weight = total_weight - back_order_goods_weight
                        total_volume = total_volume - back_order_goods_volume
                        total_cost = total_cost - back_order_goods_cost
                        dn_detail_list[i].goods_weight = dn_detail_list[i].goods_weight - \
                                                         back_order_goods_weight
                        dn_detail_list[i].goods_volume = dn_detail_list[i].goods_volume - \
                                                         back_order_goods_volume
                        dn_detail_list[i].goods_cost = dn_detail_list[i].goods_cost - \
                                                       back_order_goods_cost
                        back_order_goods_weight_list.append(back_order_goods_weight)
                        back_order_goods_volume_list.append(back_order_goods_volume)
                        back_order_goods_cost_list.append(back_order_goods_cost)
                        goods_qty_change.save()
                        dn_detail_list[i].save()
                    else:
                        dn_pick_qty = dn_detail_list[i].pick_qty
                        for j in range(len(goods_bin_stock_list)):
                            bin_can_pick_qty = goods_bin_stock_list[j].goods_qty - \
                                               goods_bin_stock_list[j].pick_qty
                            if bin_can_pick_qty > 0:
                                goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[
                                                                       j].pick_qty + bin_can_pick_qty
                                goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                picking_sum = PickingSumModel.objects.filter(openid=self.request.auth.openid,
                                                                             txnid=dn_detail_list[i].txnid)
                                if picking_sum.exists() is False:
                                    bar_code = Md5.md5(str(dn_detail_list[i].txnid) + str(random.randint(1, 9999)))
                                    PickingSumModel.objects.create(openid=self.request.auth.openid,
                                                                   txnid=dn_detail_list[i].txnid,
                                                                   order_line=dn_detail_list[i].order_line,
                                                                   order_type=dn_detail_list[i].order_type,
                                                                   trackingnumber=dn_detail_list[i].trackingnumber,
                                                                   carrier=dn_detail_list[i].carrier,
                                                                   mian_dan=dn_detail_list[i].mian_dan,
                                                                   have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                   dn_code=dn_detail_list[i].dn_code,
                                                                   creater=str(staff_name),
                                                                   bar_code=bar_code
                                                                   )
                                    scanner.objects.create(openid='SCANGOODS', mode="PSUM",
                                                           code=dn_detail_list[i].txnid,
                                                           bar_code=bar_code)
                                picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                     txnid=dn_detail_list[i].txnid,
                                                                     order_line=dn_detail_list[i].order_line,
                                                                     order_type=dn_detail_list[i].order_type,
                                                                     trackingnumber=dn_detail_list[
                                                                         i].trackingnumber,
                                                                     carrier=dn_detail_list[i].carrier,
                                                                     mian_dan=dn_detail_list[i].mian_dan,
                                                                     have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                     dn_code=dn_detail_list[i].dn_code,
                                                                     bin_name=goods_bin_stock_list[j].bin_name,
                                                                     goods_code=goods_bin_stock_list[
                                                                         j].goods_code,
                                                                     pick_qty=bin_can_pick_qty,
                                                                     creater=str(staff_name),
                                                                     t_code=goods_bin_stock_list[j].t_code))
                                scanner.objects.create(openid='SCANGOODS', mode="PLIST",
                                                       code=dn_detail_list[i].txnid,
                                                       bar_code=Md5.md5(
                                                           str(dn_detail_list[i].txnid) + str(random.randint(1, 9999))))
                                picking_list_label = 1
                                dn_pick_qty = dn_pick_qty + bin_can_pick_qty
                                goods_qty_change.save()
                                goods_bin_stock_list[j].save()
                            elif bin_can_pick_qty == 0:
                                continue
                            else:
                                continue
                        dn_detail_list[i].pick_qty = dn_pick_qty
                        dn_back_order_qty = dn_detail_list[i].goods_qty - \
                                            dn_detail_list[i].pick_qty
                        dn_detail_list[i].goods_qty = dn_pick_qty
                        dn_detail_list[i].dn_status = 3
                        back_order_goods_volume = round(goods_detail.unit_volume * dn_back_order_qty, 4)
                        back_order_goods_weight = round(
                            (goods_detail.goods_weight * dn_back_order_qty) / 1000, 4)
                        back_order_goods_cost = round(goods_detail.goods_price * dn_back_order_qty, 2)
                        back_order_list.append(DnDetailModel(dn_code=back_order_dn_code,
                                                             dn_status=2,
                                                             customer=qs.customer,
                                                             goods_code=dn_detail_list[i].goods_code,
                                                             goods_desc=dn_detail_list[i].goods_desc,
                                                             goods_qty=dn_back_order_qty,
                                                             goods_weight=back_order_goods_weight,
                                                             goods_volume=back_order_goods_volume,
                                                             goods_cost=back_order_goods_cost,
                                                             creater=str(staff_name),
                                                             back_order_label=True,
                                                             openid=self.request.auth.openid,
                                                             create_time=dn_detail_list[i].create_time))
                        back_order_list_label = 1
                        total_weight = total_weight - back_order_goods_weight
                        total_volume = total_volume - back_order_goods_volume
                        total_cost = total_cost - back_order_goods_cost
                        dn_detail_list[i].goods_weight = dn_detail_list[i].goods_weight - \
                                                         back_order_goods_weight
                        dn_detail_list[i].goods_volume = dn_detail_list[i].goods_volume - \
                                                         back_order_goods_volume
                        dn_detail_list[i].goods_cost = dn_detail_list[i].goods_cost - \
                                                       back_order_goods_cost
                        back_order_goods_weight_list.append(back_order_goods_weight)
                        back_order_goods_volume_list.append(back_order_goods_volume)
                        back_order_goods_cost_list.append(back_order_goods_cost)
                        dn_detail_list[i].save()
                elif dn_detail_list[i].goods_qty == can_pick_qty:
                    for j in range(len(goods_bin_stock_list)):
                        bin_can_pick_qty = goods_bin_stock_list[j].goods_qty - goods_bin_stock_list[j].pick_qty
                        if bin_can_pick_qty > 0:
                            dn_need_pick_qty = dn_detail_list[i].goods_qty - dn_detail_list[i].pick_qty
                            if dn_need_pick_qty > bin_can_pick_qty:
                                goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[
                                                                       j].pick_qty + bin_can_pick_qty
                                if qs.back_order_label is True:
                                    goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                    goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                picking_sum = PickingSumModel.objects.filter(openid=self.request.auth.openid,
                                                                             txnid=dn_detail_list[i].txnid)
                                if picking_sum.exists() is False:
                                    bar_code = Md5.md5(str(dn_detail_list[i].txnid) + str(random.randint(1, 9999)))
                                    PickingSumModel.objects.create(openid=self.request.auth.openid,
                                                                   txnid=dn_detail_list[i].txnid,
                                                                   order_line=dn_detail_list[i].order_line,
                                                                   order_type=dn_detail_list[i].order_type,
                                                                   trackingnumber=dn_detail_list[i].trackingnumber,
                                                                   carrier=dn_detail_list[i].carrier,
                                                                   mian_dan=dn_detail_list[i].mian_dan,
                                                                   have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                   dn_code=dn_detail_list[i].dn_code,
                                                                   creater=str(staff_name),
                                                                   bar_code=bar_code
                                                                   )
                                    scanner.objects.create(openid='SCANGOODS', mode="PSUM",
                                                           code=dn_detail_list[i].txnid,
                                                           bar_code=bar_code)
                                picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                     txnid=dn_detail_list[i].txnid,
                                                                     order_line=dn_detail_list[i].order_line,
                                                                     order_type=dn_detail_list[i].order_type,
                                                                     trackingnumber=dn_detail_list[
                                                                         i].trackingnumber,
                                                                     carrier=dn_detail_list[i].carrier,
                                                                     mian_dan=dn_detail_list[i].mian_dan,
                                                                     have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                     dn_code=dn_detail_list[i].dn_code,
                                                                     bin_name=goods_bin_stock_list[j].bin_name,
                                                                     goods_code=goods_bin_stock_list[j].goods_code,
                                                                     pick_qty=bin_can_pick_qty,
                                                                     creater=str(staff_name),
                                                                     t_code=goods_bin_stock_list[j].t_code))
                                scanner.objects.create(openid='SCANGOODS', mode="PLIST",
                                           code=dn_detail_list[i].txnid,
                                           bar_code=Md5.md5(str(dn_detail_list[i].txnid) + str(random.randint(1, 9999))))
                                picking_list_label = 1
                                dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + bin_can_pick_qty
                                goods_bin_stock_list[j].save()
                                goods_qty_change.save()
                            elif dn_need_pick_qty == bin_can_pick_qty:
                                goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[
                                                                       j].pick_qty + bin_can_pick_qty
                                if qs.back_order_label is True:
                                    goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                    goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                picking_sum = PickingSumModel.objects.filter(openid=self.request.auth.openid,
                                                                             txnid=dn_detail_list[i].txnid)
                                if picking_sum.exists() is False:
                                    bar_code = Md5.md5(str(dn_detail_list[i].txnid) + str(random.randint(1, 9999)))
                                    PickingSumModel.objects.create(openid=self.request.auth.openid,
                                                                   txnid=dn_detail_list[i].txnid,
                                                                   order_line=dn_detail_list[i].order_line,
                                                                   order_type=dn_detail_list[i].order_type,
                                                                   trackingnumber=dn_detail_list[i].trackingnumber,
                                                                   carrier=dn_detail_list[i].carrier,
                                                                   mian_dan=dn_detail_list[i].mian_dan,
                                                                   have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                   dn_code=dn_detail_list[i].dn_code,
                                                                   creater=str(staff_name),
                                                                   bar_code=bar_code
                                                                   )
                                    scanner.objects.create(openid='SCANGOODS', mode="PSUM",
                                                           code=dn_detail_list[i].txnid,
                                                           bar_code=bar_code)
                                picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                     txnid=dn_detail_list[i].txnid,
                                                                     order_line=dn_detail_list[i].order_line,
                                                                     order_type=dn_detail_list[i].order_type,
                                                                     trackingnumber=dn_detail_list[
                                                                         i].trackingnumber,
                                                                     carrier=dn_detail_list[i].carrier,
                                                                     mian_dan=dn_detail_list[i].mian_dan,
                                                                     have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                     dn_code=dn_detail_list[i].dn_code,
                                                                     bin_name=goods_bin_stock_list[j].bin_name,
                                                                     goods_code=goods_bin_stock_list[j].goods_code,
                                                                     pick_qty=bin_can_pick_qty,
                                                                     creater=str(staff_name),
                                                                     t_code=goods_bin_stock_list[j].t_code))
                                scanner.objects.create(openid='SCANGOODS', mode="PLIST",
                                                       code=dn_detail_list[i].txnid,
                                                       bar_code=Md5.md5(
                                                           str(dn_detail_list[i].txnid) + str(random.randint(1, 9999))))
                                picking_list_label = 1
                                dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + bin_can_pick_qty
                                dn_detail_list[i].dn_status = 3
                                dn_detail_list[i].save()
                                goods_bin_stock_list[j].save()
                                goods_qty_change.save()
                                break
                            else:
                                break
                        elif bin_can_pick_qty == 0:
                            continue
                        else:
                            continue
                elif dn_detail_list[i].goods_qty < can_pick_qty:
                    for j in range(len(goods_bin_stock_list)):
                        bin_can_pick_qty = goods_bin_stock_list[j].goods_qty - \
                                           goods_bin_stock_list[j].pick_qty
                        if bin_can_pick_qty > 0:
                            dn_need_pick_qty = dn_detail_list[i].goods_qty - \
                                               dn_detail_list[i].pick_qty
                            if dn_need_pick_qty > bin_can_pick_qty:
                                goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[j].pick_qty + \
                                                                   bin_can_pick_qty
                                if qs.back_order_label is True:
                                    goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                    goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - \
                                                                 bin_can_pick_qty
                                goods_qty_change.pick_stock = goods_qty_change.pick_stock + \
                                                              bin_can_pick_qty
                                picking_sum = PickingSumModel.objects.filter(openid=self.request.auth.openid,
                                                                             txnid=dn_detail_list[i].txnid)
                                if picking_sum.exists() is False:
                                    bar_code = Md5.md5(str(dn_detail_list[i].txnid) + str(random.randint(1, 9999)))
                                    PickingSumModel.objects.create(openid=self.request.auth.openid,
                                                                   txnid=dn_detail_list[i].txnid,
                                                                   order_line=dn_detail_list[i].order_line,
                                                                   order_type=dn_detail_list[i].order_type,
                                                                   trackingnumber=dn_detail_list[i].trackingnumber,
                                                                   carrier=dn_detail_list[i].carrier,
                                                                   mian_dan=dn_detail_list[i].mian_dan,
                                                                   have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                   dn_code=dn_detail_list[i].dn_code,
                                                                   creater=str(staff_name),
                                                                   bar_code=bar_code
                                                                   )
                                    scanner.objects.create(openid='SCANGOODS', mode="PSUM",
                                                           code=dn_detail_list[i].txnid,
                                                           bar_code=bar_code)
                                picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                     txnid=dn_detail_list[i].txnid,
                                                                     order_line=dn_detail_list[i].order_line,
                                                                     order_type=dn_detail_list[i].order_type,
                                                                     trackingnumber=dn_detail_list[
                                                                         i].trackingnumber,
                                                                     carrier=dn_detail_list[i].carrier,
                                                                     mian_dan=dn_detail_list[i].mian_dan,
                                                                     have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                     dn_code=dn_detail_list[i].dn_code,
                                                                     bin_name=goods_bin_stock_list[j].bin_name,
                                                                     goods_code=goods_bin_stock_list[j].goods_code,
                                                                     pick_qty=bin_can_pick_qty,
                                                                     creater=str(staff_name),
                                                                     t_code=goods_bin_stock_list[j].t_code))
                                scanner.objects.create(openid='SCANGOODS', mode="PSUM",
                                                       code=dn_detail_list[i].txnid,
                                                       bar_code=Md5.md5(
                                                           str(dn_detail_list[i].txnid) + str(random.randint(1, 9999))))
                                picking_list_label = 1
                                dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + \
                                                             bin_can_pick_qty
                                dn_detail_list[i].save()
                                goods_bin_stock_list[j].save()
                                goods_qty_change.save()
                            elif dn_need_pick_qty == bin_can_pick_qty:
                                goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[
                                                                       j].pick_qty + bin_can_pick_qty
                                if qs.back_order_label is True:
                                    goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                    goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                picking_sum = PickingSumModel.objects.filter(openid=self.request.auth.openid,
                                                                             txnid=dn_detail_list[i].txnid)
                                if picking_sum.exists() is False:
                                    bar_code = Md5.md5(str(dn_detail_list[i].txnid) + str(random.randint(1, 9999)))
                                    PickingSumModel.objects.create(openid=self.request.auth.openid,
                                                                   txnid=dn_detail_list[i].txnid,
                                                                   order_line=dn_detail_list[i].order_line,
                                                                   order_type=dn_detail_list[i].order_type,
                                                                   trackingnumber=dn_detail_list[i].trackingnumber,
                                                                   carrier=dn_detail_list[i].carrier,
                                                                   mian_dan=dn_detail_list[i].mian_dan,
                                                                   have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                   dn_code=dn_detail_list[i].dn_code,
                                                                   creater=str(staff_name),
                                                                   bar_code=bar_code
                                                                   )
                                    scanner.objects.create(openid='SCANGOODS', mode="PSUM",
                                                           code=dn_detail_list[i].txnid,
                                                           bar_code=bar_code)
                                picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                     txnid=dn_detail_list[i].txnid,
                                                                     order_line=dn_detail_list[i].order_line,
                                                                     order_type=dn_detail_list[i].order_type,
                                                                     trackingnumber=dn_detail_list[
                                                                         i].trackingnumber,
                                                                     carrier=dn_detail_list[i].carrier,
                                                                     mian_dan=dn_detail_list[i].mian_dan,
                                                                     have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                     dn_code=dn_detail_list[i].dn_code,
                                                                     bin_name=goods_bin_stock_list[j].bin_name,
                                                                     goods_code=goods_bin_stock_list[j].goods_code,
                                                                     pick_qty=bin_can_pick_qty,
                                                                     creater=str(staff_name),
                                                                     t_code=goods_bin_stock_list[j].t_code))
                                scanner.objects.create(openid='SCANGOODS', mode="PLIST",
                                                       code=dn_detail_list[i].txnid,
                                                       bar_code=Md5.md5(
                                                           str(dn_detail_list[i].txnid) + str(random.randint(1, 9999))))
                                picking_list_label = 1
                                dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + bin_can_pick_qty
                                dn_detail_list[i].dn_status = 3
                                dn_detail_list[i].save()
                                goods_bin_stock_list[j].save()
                                goods_qty_change.save()
                                break
                            elif dn_need_pick_qty < bin_can_pick_qty:
                                goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[j].pick_qty + \
                                                                   dn_need_pick_qty
                                if qs.back_order_label is True:
                                    goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - dn_need_pick_qty
                                    goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - dn_need_pick_qty
                                goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - \
                                                                 dn_need_pick_qty
                                goods_qty_change.pick_stock = goods_qty_change.pick_stock + \
                                                              dn_need_pick_qty
                                picking_sum = PickingSumModel.objects.filter(openid=self.request.auth.openid,
                                                                             txnid=dn_detail_list[i].txnid)
                                if picking_sum.exists() is False:
                                    bar_code = Md5.md5(str(dn_detail_list[i].txnid) + str(random.randint(1, 9999)))
                                    PickingSumModel.objects.create(openid=self.request.auth.openid,
                                                                   txnid=dn_detail_list[i].txnid,
                                                                   order_line=dn_detail_list[i].order_line,
                                                                   order_type=dn_detail_list[i].order_type,
                                                                   trackingnumber=dn_detail_list[i].trackingnumber,
                                                                   carrier=dn_detail_list[i].carrier,
                                                                   mian_dan=dn_detail_list[i].mian_dan,
                                                                   have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                   dn_code=dn_detail_list[i].dn_code,
                                                                   creater=str(staff_name),
                                                                   bar_code=bar_code
                                                                   )
                                    scanner.objects.create(openid='SCANGOODS', mode="PSUM",
                                                           code=dn_detail_list[i].txnid,
                                                           bar_code=bar_code)
                                picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                     txnid=dn_detail_list[i].txnid,
                                                                     order_line=dn_detail_list[i].order_line,
                                                                     order_type=dn_detail_list[i].order_type,
                                                                     trackingnumber=dn_detail_list[
                                                                         i].trackingnumber,
                                                                     carrier=dn_detail_list[i].carrier,
                                                                     mian_dan=dn_detail_list[i].mian_dan,
                                                                     have_mian_dan=dn_detail_list[i].have_mian_dan,
                                                                     dn_code=dn_detail_list[i].dn_code,
                                                                     bin_name=goods_bin_stock_list[j].bin_name,
                                                                     goods_code=goods_bin_stock_list[j].goods_code,
                                                                     pick_qty=dn_need_pick_qty,
                                                                     creater=str(staff_name),
                                                                     t_code=goods_bin_stock_list[j].t_code))
                                scanner.objects.create(openid='SCANGOODS', mode="PLIST",
                                                       code=dn_detail_list[i].txnid,
                                                       bar_code=Md5.md5(str(dn_detail_list[i].txnid) + str(random.randint(1, 9999))))
                                picking_list_label = 1
                                dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + dn_need_pick_qty
                                dn_detail_list[i].dn_status = 3
                                dn_detail_list[i].save()
                                goods_bin_stock_list[j].save()
                                goods_qty_change.save()
                                break
                            else:
                                break
                        elif bin_can_pick_qty == 0:
                            continue
                        else:
                            continue
            elif can_pick_qty == 0:
                if qs.back_order_label is False:
                    goods_qty_change.back_order_stock = goods_qty_change.back_order_stock + dn_detail_list[
                        i].goods_qty
                    back_order_goods_volume = round(goods_detail.unit_volume * dn_detail_list[i].goods_qty, 4)
                    back_order_goods_weight = round(
                        (goods_detail.goods_weight * dn_detail_list[i].goods_qty) / 1000, 4)
                    back_order_goods_cost = round(goods_detail.goods_price * dn_detail_list[i].goods_qty, 2)
                    back_order_list.append(DnDetailModel(dn_code=back_order_dn_code,
                                                         dn_status=2,
                                                         customer=qs.customer,
                                                         goods_code=dn_detail_list[i].goods_code,
                                                         goods_desc=dn_detail_list[i].goods_desc,
                                                         goods_qty=dn_detail_list[i].goods_qty,
                                                         goods_weight=back_order_goods_weight,
                                                         goods_volume=back_order_goods_volume,
                                                         goods_cost=back_order_goods_cost,
                                                         creater=str(staff_name),
                                                         back_order_label=True,
                                                         openid=self.request.auth.openid,
                                                         create_time=dn_detail_list[i].create_time))
                    back_order_list_label = 1
                    total_weight = total_weight - back_order_goods_weight
                    total_volume = total_volume - back_order_goods_volume
                    total_cost = total_cost - back_order_goods_cost
                    back_order_goods_weight_list.append(back_order_goods_weight)
                    back_order_goods_volume_list.append(back_order_goods_volume)
                    back_order_goods_cost_list.append(back_order_goods_cost)
                    dn_detail_list[i].is_delete = True
                    dn_detail_list[i].save()
                    goods_qty_change.save()
                else:
                    continue
            else:
                continue
        if picking_list_label == 1:
            if back_order_list_label == 2:
                back_order_total_volume = sumOfList(back_order_goods_volume_list,
                                                    len(back_order_goods_volume_list))
                back_order_total_weight = sumOfList(back_order_goods_weight_list,
                                                    len(back_order_goods_weight_list))
                back_order_total_cost = sumOfList(back_order_goods_cost_list,
                                                  len(back_order_goods_cost_list))
                customer_city = customer.objects.filter(
                                                        customer_name=str(qs.customer),
                                                        is_delete=False).first().customer_city
                warehouse_city = warehouse.objects.filter(
                    openid=self.request.auth.openid).first().warehouse_city
                transportation_fee = transportation.objects.filter(
                    Q(openid=self.request.auth.openid, send_city__icontains=warehouse_city,
                      receiver_city__icontains=customer_city,
                      is_delete=False) | Q(openid='init_data', send_city__icontains=warehouse_city,
                                           receiver_city__icontains=customer_city,
                                           is_delete=False))
                transportation_res = {
                    "detail": []
                }
                transportation_back_order_res = {
                    "detail": []
                }
                if len(transportation_fee) >= 1:
                    transportation_list = []
                    transportation_back_order_list = []
                    for k in range(len(transportation_fee)):
                        transportation_cost = transportation_calculate(total_weight,
                                                                       total_volume,
                                                                       transportation_fee[k].weight_fee,
                                                                       transportation_fee[k].volume_fee,
                                                                       transportation_fee[k].min_payment)
                        transportation_back_order_cost = transportation_calculate(back_order_total_weight,
                                                                                  back_order_total_volume,
                                                                                  transportation_fee[k].weight_fee,
                                                                                  transportation_fee[k].volume_fee,
                                                                                  transportation_fee[k].min_payment)
                        transportation_detail = {
                            "transportation_supplier": transportation_fee[k].transportation_supplier,
                            "transportation_cost": transportation_cost
                        }
                        transportation_back_order_detail = {
                            "transportation_supplier": transportation_fee[k].transportation_supplier,
                            "transportation_cost": transportation_back_order_cost
                        }
                        transportation_list.append(transportation_detail)
                        transportation_back_order_list.append(transportation_back_order_detail)
                    transportation_res['detail'] = transportation_list
                    transportation_back_order_res['detail'] = transportation_back_order_list
                DnListModel.objects.create(openid=self.request.auth.openid,
                                           dn_code=back_order_dn_code,
                                           dn_status=2,
                                           total_weight=back_order_total_weight,
                                           total_volume=back_order_total_volume,
                                           total_cost=back_order_total_cost,
                                           customer=qs.customer,
                                           creater=str(staff_name),
                                           bar_code=bar_code,
                                           back_order_label=True,
                                           transportation_fee=transportation_back_order_res,
                                           create_time=qs.create_time)
                scanner.objects.create(openid=self.request.auth.openid, mode="DN", code=back_order_dn_code,
                                       bar_code=bar_code)
                PickingListModel.objects.bulk_create(picking_list, batch_size=100)
                DnDetailModel.objects.bulk_create(back_order_list, batch_size=100)
                qs.total_weight = total_weight
                qs.total_volume = total_volume
                qs.total_cost = total_cost
                qs.transportation_fee = transportation_res
                qs.dn_status = 3
                qs.save()
            elif back_order_list_label == 0:
                PickingListModel.objects.bulk_create(picking_list, batch_size=100)
                qs.dn_status = 3
                qs.save()
        elif picking_list_label == 0:
            if back_order_list_label == 2:
                DnDetailModel.objects.bulk_create(back_order_list, batch_size=100)
                DnListModel.objects.create(openid=self.request.auth.openid,
                                           dn_code=back_order_dn_code,
                                           dn_status=2,
                                           total_weight=qs.total_weight,
                                           total_volume=qs.total_volume,
                                           total_cost=qs.total_cost,
                                           customer=qs.customer,
                                           creater=str(staff_name),
                                           bar_code=bar_code,
                                           back_order_label=True,
                                           transportation_fee=qs.transportation_fee,
                                           create_time=qs.create_time)
                scanner.objects.create(openid=self.request.auth.openid, mode="DN", code=back_order_dn_code,
                                       bar_code=bar_code)
                qs.is_delete = True
                qs.dn_status = 3
                qs.save()
        return Response({"detail": "success"}, status=200)

    def update(self, request, pk):
        qs = self.get_object()
        if qs.openid != self.request.auth.openid:
            raise APIException({"detail": "Cannot Release Order Data Which Not Yours"})
        else:
            if qs.dn_status == 2:
                staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                                  id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
                dn_detail_list = DnDetailModel.objects.filter(openid=self.request.auth.openid,
                                                              dn_code=qs.dn_code,
                                                              dn_status=2, is_delete=False)
                picking_list = []
                picking_list_label = 0
                back_order_list = []
                back_order_list_label = 0
                back_order_goods_weight_list = []
                back_order_goods_volume_list = []
                back_order_goods_cost_list = []
                back_order_base_code = DnListModel.objects.filter(is_delete=False).order_by('-id').first().dn_code
                dn_last_code = re.findall(r'\d+', str(back_order_base_code), re.IGNORECASE)
                back_order_dn_code = 'DN' + str(int(dn_last_code[0]) + 1).zfill(8)
                bar_code = Md5.md5(back_order_dn_code)
                total_weight = qs.total_weight
                total_volume = qs.total_volume
                total_cost = qs.total_cost
                for i in range(len(dn_detail_list)):
                    goods_detail = goods.objects.filter(
                                                        goods_code=str(dn_detail_list[i].goods_code),
                                                        is_delete=False).first()
                    if stocklist.objects.filter(openid=self.request.auth.openid,
                                                goods_code=str(dn_detail_list[i].goods_code)).exists():
                        pass
                    else:
                        stocklist.objects.create(openid=self.request.auth.openid,
                                                 goods_code=str(goods_detail.goods_code),
                                                 goods_desc=goods_detail.goods_desc,
                                                 dn_stock=int(dn_detail_list[i].goods_qty))
                    goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                                goods_code=str(
                                                                    dn_detail_list[i].goods_code)).first()
                    goods_bin_stock_list = stockbin.objects.filter(openid=self.request.auth.openid,
                                                                   goods_code=str(dn_detail_list[i].goods_code),
                                                                   bin_property="Normal", goods_qty__gt=0).order_by('bin_level')
                    can_pick_qty = goods_qty_change.onhand_stock - \
                                   goods_qty_change.inspect_stock - \
                                   goods_qty_change.hold_stock - \
                                   goods_qty_change.damage_stock - \
                                   goods_qty_change.pick_stock
                    if can_pick_qty > 0:
                        if dn_detail_list[i].goods_qty > can_pick_qty:
                            if qs.back_order_label is False:
                                dn_pick_qty = dn_detail_list[i].pick_qty
                                for j in range(len(goods_bin_stock_list)):
                                    bin_can_pick_qty = goods_bin_stock_list[j].goods_qty - \
                                                       goods_bin_stock_list[j].pick_qty
                                    if bin_can_pick_qty > 0:
                                        goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[
                                                                               j].pick_qty + bin_can_pick_qty
                                        goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                        goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                        picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                             dn_code=dn_detail_list[i].dn_code,
                                                                             bin_name=goods_bin_stock_list[j].bin_name,
                                                                             goods_code=goods_bin_stock_list[
                                                                                 j].goods_code,
                                                                             pick_qty=bin_can_pick_qty,
                                                                             creater=str(staff_name),
                                                                             t_code=goods_bin_stock_list[j].t_code))
                                        picking_list_label = 1
                                        dn_pick_qty = dn_pick_qty + bin_can_pick_qty
                                        goods_qty_change.save()
                                        goods_bin_stock_list[j].save()
                                    elif bin_can_pick_qty == 0:
                                        continue
                                    else:
                                        continue
                                dn_detail_list[i].pick_qty = dn_pick_qty
                                dn_back_order_qty = dn_detail_list[i].goods_qty - \
                                                   dn_detail_list[i].pick_qty
                                goods_qty_change.back_order_stock = dn_detail_list[i].goods_qty - can_pick_qty
                                dn_detail_list[i].goods_qty = dn_pick_qty
                                dn_detail_list[i].dn_status = 3
                                back_order_goods_volume = round(goods_detail.unit_volume * dn_back_order_qty, 4)
                                back_order_goods_weight = round(
                                    (goods_detail.goods_weight * dn_back_order_qty) / 1000, 4)
                                back_order_goods_cost = round(goods_detail.goods_price * dn_back_order_qty, 2)
                                back_order_list.append(DnDetailModel(dn_code=back_order_dn_code,
                                                                     dn_status=2,
                                                                     customer=qs.customer,
                                                                     goods_code=dn_detail_list[i].goods_code,
                                                                     goods_desc=dn_detail_list[i].goods_desc,
                                                                     goods_qty=dn_back_order_qty,
                                                                     goods_weight=back_order_goods_weight,
                                                                     goods_volume=back_order_goods_volume,
                                                                     goods_cost=back_order_goods_cost,
                                                                     creater=str(staff_name),
                                                                     back_order_label=True,
                                                                     openid=self.request.auth.openid,
                                                                     create_time=dn_detail_list[i].create_time))
                                back_order_list_label = 1
                                total_weight = total_weight - back_order_goods_weight
                                total_volume = total_volume - back_order_goods_volume
                                total_cost = total_cost - back_order_goods_cost
                                dn_detail_list[i].goods_weight = dn_detail_list[i].goods_weight - \
                                                                 back_order_goods_weight
                                dn_detail_list[i].goods_volume = dn_detail_list[i].goods_volume - \
                                                                 back_order_goods_volume
                                dn_detail_list[i].goods_cost = dn_detail_list[i].goods_cost - \
                                                                 back_order_goods_cost
                                back_order_goods_weight_list.append(back_order_goods_weight)
                                back_order_goods_volume_list.append(back_order_goods_volume)
                                back_order_goods_cost_list.append(back_order_goods_cost)
                                goods_qty_change.save()
                                dn_detail_list[i].save()
                            else:
                                dn_pick_qty = dn_detail_list[i].pick_qty
                                for j in range(len(goods_bin_stock_list)):
                                    bin_can_pick_qty = goods_bin_stock_list[j].goods_qty - \
                                                       goods_bin_stock_list[j].pick_qty
                                    if bin_can_pick_qty > 0:
                                        goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[
                                                                               j].pick_qty + bin_can_pick_qty
                                        goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                        goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                        goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                        goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                        picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                             dn_code=dn_detail_list[i].dn_code,
                                                                             bin_name=goods_bin_stock_list[j].bin_name,
                                                                             goods_code=goods_bin_stock_list[
                                                                                 j].goods_code,
                                                                             pick_qty=bin_can_pick_qty,
                                                                             creater=str(staff_name),
                                                                             t_code=goods_bin_stock_list[j].t_code))
                                        picking_list_label = 1
                                        dn_pick_qty = dn_pick_qty + bin_can_pick_qty
                                        goods_qty_change.save()
                                        goods_bin_stock_list[j].save()
                                    elif bin_can_pick_qty == 0:
                                        continue
                                    else:
                                        continue
                                dn_detail_list[i].pick_qty = dn_pick_qty
                                dn_back_order_qty = dn_detail_list[i].goods_qty - \
                                                    dn_detail_list[i].pick_qty
                                dn_detail_list[i].goods_qty = dn_pick_qty
                                dn_detail_list[i].dn_status = 3
                                back_order_goods_volume = round(goods_detail.unit_volume * dn_back_order_qty, 4)
                                back_order_goods_weight = round(
                                    (goods_detail.goods_weight * dn_back_order_qty) / 1000, 4)
                                back_order_goods_cost = round(goods_detail.goods_price * dn_back_order_qty, 2)
                                back_order_list.append(DnDetailModel(dn_code=back_order_dn_code,
                                                                     dn_status=2,
                                                                     customer=qs.customer,
                                                                     goods_code=dn_detail_list[i].goods_code,
                                                                     goods_desc=dn_detail_list[i].goods_desc,
                                                                     goods_qty=dn_back_order_qty,
                                                                     goods_weight=back_order_goods_weight,
                                                                     goods_volume=back_order_goods_volume,
                                                                     goods_cost=back_order_goods_cost,
                                                                     creater=str(staff_name),
                                                                     back_order_label=True,
                                                                     openid=self.request.auth.openid,
                                                                     create_time=dn_detail_list[i].create_time))
                                back_order_list_label = 1
                                total_weight = total_weight - back_order_goods_weight
                                total_volume = total_volume - back_order_goods_volume
                                total_cost = total_cost - back_order_goods_cost
                                dn_detail_list[i].goods_weight = dn_detail_list[i].goods_weight - \
                                                                 back_order_goods_weight
                                dn_detail_list[i].goods_volume = dn_detail_list[i].goods_volume - \
                                                                 back_order_goods_volume
                                dn_detail_list[i].goods_cost = dn_detail_list[i].goods_cost - \
                                                                 back_order_goods_cost
                                back_order_goods_weight_list.append(back_order_goods_weight)
                                back_order_goods_volume_list.append(back_order_goods_volume)
                                back_order_goods_cost_list.append(back_order_goods_cost)
                                dn_detail_list[i].save()
                        elif dn_detail_list[i].goods_qty == can_pick_qty:
                            for j in range(len(goods_bin_stock_list)):
                                bin_can_pick_qty = goods_bin_stock_list[j].goods_qty - goods_bin_stock_list[j].pick_qty
                                if bin_can_pick_qty > 0:
                                    dn_need_pick_qty = dn_detail_list[i].goods_qty - dn_detail_list[i].pick_qty
                                    if dn_need_pick_qty > bin_can_pick_qty:
                                        goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[
                                                                               j].pick_qty + bin_can_pick_qty
                                        if qs.back_order_label is True:
                                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                            goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                        goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                        goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                        picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                             dn_code=dn_detail_list[i].dn_code,
                                                                             bin_name=goods_bin_stock_list[j].bin_name,
                                                                             goods_code=goods_bin_stock_list[j].goods_code,
                                                                             pick_qty=bin_can_pick_qty,
                                                                             creater=str(staff_name),
                                                                             t_code=goods_bin_stock_list[j].t_code))
                                        picking_list_label = 1
                                        dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + bin_can_pick_qty
                                        goods_bin_stock_list[j].save()
                                        goods_qty_change.save()
                                    elif dn_need_pick_qty == bin_can_pick_qty:
                                        goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[
                                                                               j].pick_qty + bin_can_pick_qty
                                        if qs.back_order_label is True:
                                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                            goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                        goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                        goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                        picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                             dn_code=dn_detail_list[i].dn_code,
                                                                             bin_name=goods_bin_stock_list[j].bin_name,
                                                                             goods_code=goods_bin_stock_list[j].goods_code,
                                                                             pick_qty=bin_can_pick_qty,
                                                                             creater=str(staff_name),
                                                                             t_code=goods_bin_stock_list[j].t_code))
                                        picking_list_label = 1
                                        dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + bin_can_pick_qty
                                        dn_detail_list[i].dn_status = 3
                                        dn_detail_list[i].save()
                                        goods_bin_stock_list[j].save()
                                        goods_qty_change.save()
                                        break
                                    else:
                                        break
                                elif bin_can_pick_qty == 0:
                                    continue
                                else:
                                    continue
                        elif dn_detail_list[i].goods_qty < can_pick_qty:
                            for j in range(len(goods_bin_stock_list)):
                                bin_can_pick_qty = goods_bin_stock_list[j].goods_qty - \
                                                   goods_bin_stock_list[j].pick_qty
                                if bin_can_pick_qty > 0:
                                    dn_need_pick_qty = dn_detail_list[i].goods_qty - \
                                                       dn_detail_list[i].pick_qty
                                    if dn_need_pick_qty > bin_can_pick_qty:
                                        goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[j].pick_qty + \
                                                                           bin_can_pick_qty
                                        if qs.back_order_label is True:
                                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                            goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                        goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - \
                                                                         bin_can_pick_qty
                                        goods_qty_change.pick_stock = goods_qty_change.pick_stock + \
                                                                      bin_can_pick_qty
                                        picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                             dn_code=dn_detail_list[i].dn_code,
                                                                             bin_name=goods_bin_stock_list[j].bin_name,
                                                                             goods_code=goods_bin_stock_list[j].goods_code,
                                                                             pick_qty=bin_can_pick_qty,
                                                                             creater=str(staff_name),
                                                                             t_code=goods_bin_stock_list[j].t_code))
                                        picking_list_label = 1
                                        dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + \
                                                                     bin_can_pick_qty
                                        dn_detail_list[i].save()
                                        goods_bin_stock_list[j].save()
                                        goods_qty_change.save()
                                    elif dn_need_pick_qty == bin_can_pick_qty:
                                        goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[
                                                                               j].pick_qty + bin_can_pick_qty
                                        if qs.back_order_label is True:
                                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - bin_can_pick_qty
                                            goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - bin_can_pick_qty
                                        goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - bin_can_pick_qty
                                        goods_qty_change.pick_stock = goods_qty_change.pick_stock + bin_can_pick_qty
                                        picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                             dn_code=dn_detail_list[i].dn_code,
                                                                             bin_name=goods_bin_stock_list[j].bin_name,
                                                                             goods_code=goods_bin_stock_list[j].goods_code,
                                                                             pick_qty=bin_can_pick_qty,
                                                                             creater=str(staff_name),
                                                                             t_code=goods_bin_stock_list[j].t_code))
                                        picking_list_label = 1
                                        dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + bin_can_pick_qty
                                        dn_detail_list[i].dn_status = 3
                                        dn_detail_list[i].save()
                                        goods_bin_stock_list[j].save()
                                        goods_qty_change.save()
                                        break
                                    elif dn_need_pick_qty < bin_can_pick_qty:
                                        goods_bin_stock_list[j].pick_qty = goods_bin_stock_list[j].pick_qty + \
                                                                           dn_need_pick_qty
                                        if qs.back_order_label is True:
                                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - dn_need_pick_qty
                                            goods_qty_change.back_order_stock = goods_qty_change.back_order_stock - dn_need_pick_qty
                                        goods_qty_change.ordered_stock = goods_qty_change.ordered_stock - \
                                                                         dn_need_pick_qty
                                        goods_qty_change.pick_stock = goods_qty_change.pick_stock + \
                                                                      dn_need_pick_qty
                                        picking_list.append(PickingListModel(openid=self.request.auth.openid,
                                                                             dn_code=dn_detail_list[i].dn_code,
                                                                             bin_name=goods_bin_stock_list[j].bin_name,
                                                                             goods_code=goods_bin_stock_list[j].goods_code,
                                                                             pick_qty=dn_need_pick_qty,
                                                                             creater=str(staff_name),
                                                                             t_code=goods_bin_stock_list[j].t_code))
                                        picking_list_label = 1
                                        dn_detail_list[i].pick_qty = dn_detail_list[i].pick_qty + dn_need_pick_qty
                                        dn_detail_list[i].dn_status = 3
                                        dn_detail_list[i].save()
                                        goods_bin_stock_list[j].save()
                                        goods_qty_change.save()
                                        break
                                    else:
                                        break
                                elif bin_can_pick_qty == 0:
                                    continue
                                else:
                                    continue
                    elif can_pick_qty == 0:
                        if qs.back_order_label is False:
                            goods_qty_change.back_order_stock = goods_qty_change.back_order_stock + dn_detail_list[i].goods_qty
                            back_order_goods_volume = round(goods_detail.unit_volume * dn_detail_list[i].goods_qty, 4)
                            back_order_goods_weight = round((goods_detail.goods_weight * dn_detail_list[i].goods_qty) / 1000, 4)
                            back_order_goods_cost = round(goods_detail.goods_price * dn_detail_list[i].goods_qty, 2)
                            back_order_list.append(DnDetailModel(dn_code=back_order_dn_code,
                                                                 dn_status=2,
                                                                 customer=qs.customer,
                                                                 goods_code=dn_detail_list[i].goods_code,
                                                                 goods_desc=dn_detail_list[i].goods_desc,
                                                                 goods_qty=dn_detail_list[i].goods_qty,
                                                                 goods_weight=back_order_goods_weight,
                                                                 goods_volume=back_order_goods_volume,
                                                                 goods_cost=back_order_goods_cost,
                                                                 creater=str(staff_name),
                                                                 back_order_label=True,
                                                                 openid=self.request.auth.openid,
                                                                 create_time=dn_detail_list[i].create_time))
                            back_order_list_label = 1
                            total_weight = total_weight - back_order_goods_weight
                            total_volume = total_volume - back_order_goods_volume
                            total_cost = total_cost - back_order_goods_cost
                            back_order_goods_weight_list.append(back_order_goods_weight)
                            back_order_goods_volume_list.append(back_order_goods_volume)
                            back_order_goods_cost_list.append(back_order_goods_cost)
                            dn_detail_list[i].is_delete = True
                            dn_detail_list[i].save()
                            goods_qty_change.save()
                        else:
                            continue
                    else:
                        continue
                if picking_list_label == 1:
                    if back_order_list_label == 1:
                        back_order_total_volume = sumOfList(back_order_goods_volume_list,
                                                            len(back_order_goods_volume_list))
                        back_order_total_weight = sumOfList(back_order_goods_weight_list,
                                                            len(back_order_goods_weight_list))
                        back_order_total_cost = sumOfList(back_order_goods_cost_list,
                                                            len(back_order_goods_cost_list))
                        customer_city = customer.objects.filter(
                                                                customer_name=str(qs.customer),
                                                                is_delete=False).first().customer_city
                        warehouse_city = warehouse.objects.filter(
                            openid=self.request.auth.openid).first().warehouse_city
                        transportation_fee = transportation.objects.filter(
                            Q(openid=self.request.auth.openid, send_city__icontains=warehouse_city,
                              receiver_city__icontains=customer_city,
                              is_delete=False) | Q(openid='init_data', send_city__icontains=warehouse_city,
                                                   receiver_city__icontains=customer_city,
                                                   is_delete=False))
                        transportation_res = {
                            "detail": []
                        }
                        transportation_back_order_res = {
                            "detail": []
                        }
                        if len(transportation_fee) >= 1:
                            transportation_list = []
                            transportation_back_order_list = []
                            for k in range(len(transportation_fee)):
                                transportation_cost = transportation_calculate(total_weight,
                                                                               total_volume,
                                                                               transportation_fee[k].weight_fee,
                                                                               transportation_fee[k].volume_fee,
                                                                               transportation_fee[k].min_payment)
                                transportation_back_order_cost = transportation_calculate(back_order_total_weight,
                                                                               back_order_total_volume,
                                                                               transportation_fee[k].weight_fee,
                                                                               transportation_fee[k].volume_fee,
                                                                               transportation_fee[k].min_payment)
                                transportation_detail = {
                                    "transportation_supplier": transportation_fee[k].transportation_supplier,
                                    "transportation_cost": transportation_cost
                                }
                                transportation_back_order_detail = {
                                    "transportation_supplier": transportation_fee[k].transportation_supplier,
                                    "transportation_cost": transportation_back_order_cost
                                }
                                transportation_list.append(transportation_detail)
                                transportation_back_order_list.append(transportation_back_order_detail)
                            transportation_res['detail'] = transportation_list
                            transportation_back_order_res['detail'] = transportation_back_order_list
                        DnListModel.objects.create(openid=self.request.auth.openid,
                                                   dn_code=back_order_dn_code,
                                                   dn_status=2,
                                                   total_weight=back_order_total_weight,
                                                   total_volume=back_order_total_volume,
                                                   total_cost=back_order_total_cost,
                                                   customer=qs.customer,
                                                   creater=str(staff_name),
                                                   bar_code=bar_code,
                                                   back_order_label=True,
                                                   transportation_fee=transportation_back_order_res,
                                                   create_time=qs.create_time)
                        scanner.objects.create(openid=self.request.auth.openid, mode="DN", code=back_order_dn_code,
                                               bar_code=bar_code)
                        PickingListModel.objects.bulk_create(picking_list, batch_size=100)
                        DnDetailModel.objects.bulk_create(back_order_list, batch_size=100)
                        qs.total_weight = total_weight
                        qs.total_volume = total_volume
                        qs.total_cost = total_cost
                        qs.transportation_fee = transportation_res
                        qs.dn_status = 3
                        qs.save()
                    elif back_order_list_label == 0:
                        PickingListModel.objects.bulk_create(picking_list, batch_size=100)
                        qs.dn_status = 3
                        qs.save()
                elif picking_list_label == 0:
                    if back_order_list_label == 1:
                        DnDetailModel.objects.bulk_create(back_order_list, batch_size=100)
                        DnListModel.objects.create(openid=self.request.auth.openid,
                                                   dn_code=back_order_dn_code,
                                                   dn_status=2,
                                                   total_weight=qs.total_weight,
                                                   total_volume=qs.total_volume,
                                                   total_cost=qs.total_cost,
                                                   customer=qs.customer,
                                                   creater=str(staff_name),
                                                   bar_code=bar_code,
                                                   back_order_label=True,
                                                   transportation_fee=qs.transportation_fee,
                                                   create_time=qs.create_time)
                        scanner.objects.create(openid=self.request.auth.openid, mode="DN", code=back_order_dn_code,
                                               bar_code=bar_code)
                        qs.is_delete = True
                        qs.dn_status = 3
                        qs.save()
                return Response({"detail": "success"}, status=200)
            else:
                raise APIException({"detail": "This Order Does Not in Release Status"})


class DnPickingListViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Picklist for pk
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

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
            query_dict = {'id': id}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            return DnListModel.objects.filter(**query_dict)
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return serializers.DNListGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def retrieve(self, request, pk):
        qs = self.get_object()
        if qs.dn_status < 3:
            raise APIException({"detail": "No Picking List Been Created"})
        else:
            u = Users.objects.filter(vip=9).first()
            if u is None:
                superopenid = None
            else:
                superopenid = u.openid
            openid = {}
            if self.request.auth.openid != superopenid:
                openid['openid'] = self.request.auth.openid
            picking_qs = PickingListModel.objects.filter(**openid, dn_code=qs.dn_code)
            serializer = serializers.DNPickingListGetSerializer(picking_qs, many=True)
            return Response(serializer.data, status=200)

class DnPickingSumFilterViewSet(viewsets.ModelViewSet):
    """
        list:
            Picklist for Filter
    """
    pagination_class = MyPageNumberPaginationPicking
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnPickingSumFilter

    def get_queryset(self):
        if self.request.user:
            u = Users.objects.filter(vip=9).first()
            if u is None:
                superopenid = None
            else:
                superopenid = u.openid
            query_dict = {}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            return PickingSumModel.objects.filter(**query_dict)
        else:
            return PickingSumModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.DNPickingSumGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)




class DnPickingListFilterViewSet(viewsets.ModelViewSet):
    """
        list:
            Picklist for Filter
    """
    pagination_class = MyPageNumberPaginationPicking
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnPickingListFilter

    def get_queryset(self):
        if self.request.user:
            u = Users.objects.filter(vip=9).first()
            if u is None:
                superopenid = None
            else:
                superopenid = u.openid
            query_dict = {}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            return PickingListModel.objects.filter(**query_dict)
        else:
            return PickingListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.DNPickingCheckGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)


class PickerOneAllocateViewSet(viewsets.ModelViewSet):
    """
        list:
            Picklist for Filter
    """
    pagination_class = MyPageNumberPaginationPicking
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnPickingListFilter

    def get_queryset(self):
        if self.request.user:
            u = Users.objects.filter(vip=9).first()
            if u is None:
                superopenid = None
            else:
                superopenid = u.openid
            query_dict = {'have_mian_dan': True}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            return PickingListModel.objects.filter(**query_dict)
        else:
            return PickingListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DNPickingCheckGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        data = self.request.data
        bin_data = data.get("bin_data")
        staff_list = staff.objects.filter(openid=self.request.auth.openid, staff_name=data['staff_name'])
        staff_list.update(picking_task=1,bin_data=bin_data)
        for obj in staff_list:
            obj.save()
        for i in range(len(qs)):
            PickingSumModel.objects.filter(txnid=qs[i].txnid).update(picker=data['staff_name'], picking_status=1)
        qs.update(picker=data['staff_name'], picking_status=1)
        return Response({"Detail": "success"}, status=200)


class PickerMoreAllocateViewSet(viewsets.ModelViewSet):
    """
        list:
            Picklist for Filter
    """
    pagination_class = MyPageNumberPaginationPicking
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnPickingListFilter

    def get_queryset(self):
        if self.request.user:
            u = Users.objects.filter(vip=9).first()
            if u is None:
                superopenid = None
            else:
                superopenid = u.openid
            query_dict = {'have_mian_dan': True}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            return PickingListModel.objects.filter(**query_dict)
        else:
            return PickingListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DNPickingCheckGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        data = self.request.data
        staff.objects.filter(openid=self.request.auth.openid, staff_name=data['staff_name']).update(picking_task=1)
        for i in range(len(qs)):
            PickingSumModel.objects.filter(txnid=qs[i].txnid).update(picker=data['staff_name'], picking_status=1)
        qs.update(picker=data['staff_name'], picking_status=1)
        return Response({"Detail": "success"}, status=200)

class DnPickedViewSet(viewsets.ModelViewSet):
    """
        create:
            Finish Picked
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

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
            return DnListModel.objects.filter(**query_dict)
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return serializers.DNListUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, pk):
        qs = self.get_object()
        delete_data = stockbin.objects.filter(openid=self.request.auth.openid,
                                              goods_qty=0,
                                              pick_qty=0,
                                              picked_qty=0)
        if delete_data.exists():
            for i in delete_data:
                i.delete()
        if qs.dn_status != 3:
            raise APIException({"detail": "This dn Status Not Pre Pick"})
        else:
            data = self.request.data
            for i in range(len(data['goodsData'])):
                pick_qty_change = PickingListModel.objects.filter(dn_code=str(data['dn_code']),
                                                                  picking_status=0,
                                                                  t_code=str(data['goodsData'][i].get('t_code'))).first()
                if int(data['goodsData'][i].get('pick_qty')) < 0:
                    raise APIException({"detail": str(data['goodsData'][i].get('goods_code')) + " Picked Qty Must >= 0"})
                else:
                    if int(data['goodsData'][i].get('pick_qty')) > pick_qty_change.pick_qty:
                        raise APIException({"detail": str(data['goodsData'][i].get('goods_code')) + " Picked Qty Must Less Than Pick Qty"})
                    else:
                        continue
            qs.dn_status = 4
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            for j in range(len(data['goodsData'])):
                goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                            goods_code=str(data['goodsData'][j].get('goods_code'))).first()
                dn_detail = DnDetailModel.objects.filter(openid=self.request.auth.openid,
                                                         dn_code=str(data['dn_code']),
                                                         customer=str(data['customer']),
                                                         goods_code=str(data['goodsData'][j].get('goods_code'))).first()
                bin_qty_change = stockbin.objects.filter(openid=self.request.auth.openid,
                                                         t_code=str(data['goodsData'][j].get('t_code'))).first()
                pick_qty_change = PickingListModel.objects.filter(openid=self.request.auth.openid,
                                                                  dn_code=str(data['dn_code']),
                                                                  picking_status=0,
                                                                  t_code=str(data['goodsData'][j].get('t_code'))).first()
                qtychangerecorder.objects.create(openid=self.request.auth.openid,
                                                 mode_code=dn_detail.dn_code,
                                                 bin_name=bin_qty_change.bin_name,
                                                 goods_code=bin_qty_change.goods_code,
                                                 goods_desc=bin_qty_change.goods_desc,
                                                 goods_qty=0 - int(data['goodsData'][j].get('pick_qty')),
                                                 creater=str(staff_name)
                                                 )
                cur_date = timezone.now().date()
                bin_stock = stockbin.objects.filter(openid=self.request.auth.openid,
                                                    bin_name=bin_qty_change.bin_name,
                                                    goods_code=bin_qty_change.goods_code,
                                                    ).aggregate(sum=Sum('goods_qty'))["sum"]
                cycle_qty = bin_stock - int(data['goodsData'][j].get('pick_qty'))
                cyclecount.objects.filter(openid=self.request.auth.openid,
                                          bin_name=bin_qty_change.bin_name,
                                          goods_code=bin_qty_change.goods_code,
                                          create_time__gte=cur_date).update(goods_qty=cycle_qty)
                if int(data['goodsData'][j].get('pick_qty')) == pick_qty_change.pick_qty:
                    goods_qty_change.onhand_stock = goods_qty_change.onhand_stock - int(data['goodsData'][j].get('pick_qty'))
                    goods_qty_change.pick_stock = goods_qty_change.pick_stock - int(data['goodsData'][j].get('pick_qty'))
                    goods_qty_change.picked_stock = goods_qty_change.picked_stock + int(data['goodsData'][j].get('pick_qty'))

                    pick_qty_change.picked_qty = int(data['goodsData'][j].get('pick_qty'))
                    pick_qty_change.picking_status = 1
                    bin_qty_change.goods_qty = bin_qty_change.goods_qty - int(data['goodsData'][j].get('pick_qty'))
                    bin_qty_change.pick_qty = bin_qty_change.pick_qty - int(data['goodsData'][j].get('pick_qty'))
                    bin_qty_change.picked_qty = bin_qty_change.picked_qty + int(data['goodsData'][j].get('pick_qty'))
                    goods_qty_change.save()
                    pick_qty_change.save()
                    bin_qty_change.save()
                elif int(data['goodsData'][j].get('pick_qty')) < pick_qty_change.pick_qty:
                    goods_qty_change.onhand_stock = goods_qty_change.onhand_stock - int(data['goodsData'][j].get('pick_qty'))
                    goods_qty_change.pick_stock = goods_qty_change.pick_stock - dn_detail.pick_qty
                    goods_qty_change.picked_stock = goods_qty_change.picked_stock + int(data['goodsData'][j].get('pick_qty'))
                    goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + (int(pick_qty_change.pick_qty) - int(
                        data['goodsData'][j].get('pick_qty')))
                    pick_qty_change.picked_qty = int(data['goodsData'][j].get('pick_qty'))
                    pick_qty_change.picking_status = 1
                    bin_qty_change.goods_qty = bin_qty_change.goods_qty - int(data['goodsData'][j].get('pick_qty'))
                    bin_qty_change.pick_qty = bin_qty_change.pick_qty - pick_qty_change.pick_qty
                    bin_qty_change.picked_qty = bin_qty_change.picked_qty + int(data['goodsData'][j].get('pick_qty'))
                    goods_qty_change.save()
                    pick_qty_change.save()
                    bin_qty_change.save()
                dn_detail.picked_qty = dn_detail.picked_qty + int(data['goodsData'][j].get('pick_qty'))
                if dn_detail.dn_status == 3:
                    dn_detail.dn_status = 4
                if dn_detail.pick_qty > 0:
                    dn_detail.pick_qty = 0
                dn_detail.save()
            if DnDetailModel.objects.filter(openid=self.request.auth.openid, dn_code=str(data['dn_code']),
                                            dn_status=3).exists() is False:
                qs.save()
                qs_set = DnListModel.objects.filter(is_delete=False)
                order_day = str(timezone.now().strftime('%Y%m%d'))
                if len(qs_set) > 0:
                    dn_last_code = qs_set.order_by('-id').first().dn_code
                    if dn_last_code[2:10] == order_day:
                        order_create_no = str(int(dn_last_code[10:]) + 1)
                        new_dn_code = 'DN' + order_day + order_create_no
                    else:
                        new_dn_code = 'DN' + order_day + '1'
                else:
                    new_dn_code = 'DN' + order_day + '1'
                new_bar_code = Md5.md5(str(new_dn_code))
                qs_dn_list_detail = DnDetailModel.objects.filter(openid=self.request.auth.openid, dn_code=str(data['dn_code']),
                                                                 dn_status=4)
                post_data_list = []
                for v in qs_dn_list_detail:
                    check_data = v.goods_qty - v.picked_qty
                    if check_data > 0:
                        post_data_list.append(DnDetailModel(dn_code=new_dn_code,
                                                            dn_status=2,
                                                            customer=qs.customer,
                                                            goods_code=v.goods_code,
                                                            goods_desc=v.goods_desc,
                                                            goods_qty=check_data,
                                                            goods_weight=0,
                                                            goods_volume=0,
                                                            goods_cost=0,
                                                            creater=str(staff_name),
                                                            back_order_label=True,
                                                            openid=self.request.auth.openid,
                                                            create_time=v.create_time))
                        stock_list = stocklist.objects.filter(openid=self.request.auth.openid, goods_code=v.goods_code).first()
                        stock_list.ordered_stock = stock_list.ordered_stock + check_data
                        stock_list.back_order_stock = stock_list.back_order_stock + check_data
                        stock_list.save()
                if len(post_data_list) > 0:
                    DnDetailModel.objects.bulk_create(post_data_list, batch_size=100)
                    DnListModel.objects.create(dn_code=new_dn_code,
                                               dn_status=2,
                                               customer=qs.customer,
                                               creater=str(staff_name),
                                               bar_code=new_bar_code,
                                               back_order_label=True,
                                               openid=self.request.auth.openid,
                                               warehouse_id=qs.warehouse_id,
                                               comments=qs.comments,
                                               create_time=qs.create_time
                                               )
            return Response({"Detail": "success"}, status=200)

    def update(self, request, *args, **kwargs):
        delete_data = stockbin.objects.filter(openid=self.request.auth.openid,
                                              goods_qty=0,
                                              pick_qty=0,
                                              picked_qty=0)
        if delete_data.exists():
            for i in delete_data:
                i.delete()
        data = self.request.data
        qs_query = DnListModel.objects.filter(openid=self.request.auth.openid, dn_code=data['dn_code'], is_delete=False)
        if qs_query.exists() is False:
            raise APIException({"detail": self.request.auth.openid + data['goodsData'][0].get('txnid', '') + "订单号没找到"})
        else:
            qs = qs_query.first()
            if qs.dn_status != 3:
                raise APIException({"detail": "This dn Status Not Pre Pick"})
            else:
                for i in range(len(data['goodsData'])):
                    pick_qty_change = PickingListModel.objects.filter(openid=self.request.auth.openid,
                                                                      dn_code=str(data['dn_code']),
                                                                      picking_status=1,
                                                                      t_code=str(
                                                                          data['goodsData'][i].get('t_code'))).first()
                    if int(data['goodsData'][i].get('picked_qty')) < 0:
                        raise APIException(
                            {"detail": str(data['goodsData'][i].get('goods_code')) + " Picked Qty Must >= 0"})
                    else:
                        if int(data['goodsData'][i].get('picked_qty')) > pick_qty_change.pick_qty:
                            raise APIException(
                                {"detail": str(
                                    data['goodsData'][i].get('goods_code')) + " Picked Qty Must Less Than Pick Qty"})
                        else:
                            continue
                qs.dn_status = 4
                staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                                  id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
                for j in range(len(data['goodsData'])):
                    goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                                goods_code=str(
                                                                    data['goodsData'][j].get('goods_code'))).first()
                    dn_detail = DnDetailModel.objects.filter(openid=self.request.auth.openid,
                                                             dn_code=str(data['dn_code']),
                                                             goods_code=str(data['goodsData'][j].get('goods_code'))).first()
                    bin_qty_change = stockbin.objects.filter(openid=self.request.auth.openid,
                                                             t_code=str(data['goodsData'][j].get('t_code'))).first()
                    pick_qty_change = PickingListModel.objects.filter(openid=self.request.auth.openid,
                                                                      dn_code=str(data['dn_code']),
                                                                      picking_status=1,
                                                                      t_code=str(
                                                                          data['goodsData'][j].get('t_code'))).first()
                    pick_sum_change = PickingSumModel.objects.filter(openid=self.request.auth.openid,
                                                                      dn_code=str(data['dn_code']),
                                                                      picking_status=1,
                                                                      )
                    qtychangerecorder.objects.create(openid=self.request.auth.openid,
                                                     mode_code=dn_detail.dn_code,
                                                     bin_name=bin_qty_change.bin_name,
                                                     goods_code=bin_qty_change.goods_code,
                                                     goods_desc=bin_qty_change.goods_desc,
                                                     goods_qty=0 - int(data['goodsData'][j].get('picked_qty')),
                                                     creater=str(staff_name)
                                                     )
                    cur_date = timezone.now().date()
                    bin_stock = stockbin.objects.filter(openid=self.request.auth.openid,
                                                        bin_name=bin_qty_change.bin_name,
                                                        goods_code=bin_qty_change.goods_code,
                                                        ).aggregate(sum=Sum('goods_qty'))["sum"]
                    cycle_qty = bin_stock - int(data['goodsData'][j].get('picked_qty'))
                    cyclecount.objects.filter(openid=self.request.auth.openid,
                                              bin_name=bin_qty_change.bin_name,
                                              goods_code=bin_qty_change.goods_code,
                                              create_time__gte=cur_date).update(goods_qty=cycle_qty)
                    if int(data['goodsData'][j].get('picked_qty')) == pick_qty_change.pick_qty:
                        goods_qty_change.onhand_stock = goods_qty_change.onhand_stock - int(
                            data['goodsData'][j].get('pick_qty'))
                        goods_qty_change.pick_stock = goods_qty_change.pick_stock - int(
                            data['goodsData'][j].get('picked_qty'))
                        goods_qty_change.picked_stock = goods_qty_change.picked_stock + int(
                            data['goodsData'][j].get('picked_qty'))
                        pick_qty_change.picked_qty = int(data['goodsData'][j].get('picked_qty'))
                        pick_qty_change.picking_status = 2
                        bin_qty_change.goods_qty = bin_qty_change.goods_qty - int(data['goodsData'][j].get('pick_qty'))
                        bin_qty_change.pick_qty = bin_qty_change.pick_qty - int(data['goodsData'][j].get('picked_qty'))
                        bin_qty_change.picked_qty = bin_qty_change.picked_qty + int(data['goodsData'][j].get('picked_qty'))
                        if pick_sum_change.exists():
                            pick_sum_change.first().picking_status = 2
                            pick_sum_change.first().save()
                        goods_qty_change.save()
                        pick_qty_change.save()
                        bin_qty_change.save()
                    elif int(data['goodsData'][j].get('picked_qty')) < pick_qty_change.pick_qty:
                        goods_qty_change.onhand_stock = goods_qty_change.onhand_stock - int(
                            data['goodsData'][j].get('pick_qty'))
                        goods_qty_change.pick_stock = goods_qty_change.pick_stock - dn_detail.pick_qty
                        goods_qty_change.picked_stock = goods_qty_change.picked_stock + int(
                            data['goodsData'][j].get('picked_qty'))
                        goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + (
                                    int(pick_qty_change.pick_qty) - int(
                                data['goodsData'][j].get('pick_qty')))
                        pick_qty_change.picked_qty = int(data['goodsData'][j].get('picked_qty'))
                        pick_qty_change.picking_status = 2
                        bin_qty_change.goods_qty = bin_qty_change.goods_qty - int(data['goodsData'][j].get('pick_qty'))
                        bin_qty_change.pick_qty = bin_qty_change.pick_qty - pick_qty_change.pick_qty
                        bin_qty_change.picked_qty = bin_qty_change.picked_qty + int(data['goodsData'][j].get('picked_qty'))
                        if pick_sum_change.exists():
                            pick_sum_change.first().picking_status = 2
                            pick_sum_change.first().save()
                        goods_qty_change.save()
                        pick_qty_change.save()
                        bin_qty_change.save()
                    dn_detail.picked_qty = dn_detail.picked_qty + int(data['goodsData'][j].get('picked_qty'))
                    if dn_detail.dn_status == 3:
                        dn_detail.dn_status = 4
                    if dn_detail.pick_qty > 0:
                        dn_detail.pick_qty = 0
                    dn_detail.save()
                if DnDetailModel.objects.filter(openid=self.request.auth.openid, dn_code=str(data['dn_code']),
                                                dn_status=3).exists() is False:
                    qs.save()
                return Response({"Detail": "success"}, status=200)


class DnPickedSumViewSet(viewsets.ModelViewSet):
    """
        create:
            Finish Picked
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

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
            return DnListModel.objects.filter(**query_dict)
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return serializers.DNListUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)


    def create(self, request, *args, **kwargs):
        delete_data = stockbin.objects.filter(openid=self.request.auth.openid,
                                              goods_qty=0,
                                              pick_qty=0,
                                              picked_qty=0)
        if delete_data.exists():
            for i in delete_data:
                i.delete()
        data = self.request.data
        qs_query = DnListModel.objects.filter(openid=self.request.auth.openid, dn_code=data['dn_code'], is_delete=False)
        if qs_query.exists() is False:
            raise APIException({"detail": data[0].get('txnid', '') + "订单号没找到"})
        else:
            qs = qs_query.first()
            if qs.dn_status != 3:
                raise APIException({"detail": "This dn Status Not Pre Pick"})
            else:
                qs.dn_status = 4
                staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                                  id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
                detail_data = PickingListModel.objects.filter(openid=self.request.auth.openid,
                                                              dn_code=str(data['dn_code']),
                                                              picking_status=1)
                for j in range(len(detail_data)):
                    goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                                goods_code=str(
                                                                    detail_data[j].goods_code)).first()
                    dn_detail = DnDetailModel.objects.filter(openid=self.request.auth.openid,
                                                             dn_code=str(data['dn_code']),
                                                             goods_code=str(detail_data[j].goods_code)).first()
                    bin_qty_change = stockbin.objects.filter(openid=self.request.auth.openid,
                                                             t_code=str(detail_data[j].t_code)).first()
                    pick_qty_change = PickingListModel.objects.filter(openid=self.request.auth.openid,
                                                                      dn_code=str(data['dn_code']),
                                                                      picking_status=1,
                                                                      t_code=str(
                                                                          detail_data[j].t_code)).first()
                    pick_sum_change = PickingSumModel.objects.filter(openid=self.request.auth.openid,
                                                                      dn_code=str(data['dn_code']),
                                                                      picking_status=1,
                                                                      )
                    qtychangerecorder.objects.create(openid=self.request.auth.openid,
                                                     mode_code=dn_detail.dn_code,
                                                     bin_name=bin_qty_change.bin_name,
                                                     goods_code=bin_qty_change.goods_code,
                                                     goods_desc=bin_qty_change.goods_desc,
                                                     goods_qty=0 - int(detail_data[j].picked_qty),
                                                     creater=str(staff_name)
                                                     )
                    cur_date = timezone.now().date()
                    bin_stock = stockbin.objects.filter(openid=self.request.auth.openid,
                                                        bin_name=bin_qty_change.bin_name,
                                                        goods_code=bin_qty_change.goods_code,
                                                        ).aggregate(sum=Sum('goods_qty'))["sum"]
                    cycle_qty = bin_stock - int(detail_data[j].picked_qty)
                    cyclecount.objects.filter(openid=self.request.auth.openid,
                                              bin_name=bin_qty_change.bin_name,
                                              goods_code=bin_qty_change.goods_code,
                                              create_time__gte=cur_date).update(goods_qty=cycle_qty)
                    if int(detail_data[j].picked_qty) == pick_qty_change.pick_qty:
                        goods_qty_change.onhand_stock = goods_qty_change.onhand_stock - int(
                            detail_data[j].pick_qty)
                        goods_qty_change.pick_stock = goods_qty_change.pick_stock - int(
                            detail_data[j].picked_qty)
                        goods_qty_change.picked_stock = goods_qty_change.picked_stock + int(
                            detail_data[j].picked_qty)
                        pick_qty_change.picked_qty = int(detail_data[j].picked_qty)
                        pick_qty_change.picking_status = 2
                        pick_qty_change.save()
                        bin_qty_change.goods_qty = bin_qty_change.goods_qty - int(detail_data[j].pick_qty)
                        bin_qty_change.pick_qty = bin_qty_change.pick_qty - int(detail_data[j].picked_qty)
                        bin_qty_change.picked_qty = bin_qty_change.picked_qty + int(detail_data[j].picked_qty)
                        if pick_sum_change.exists():
                            pick_sum_change.first().picking_status = 2
                            pick_sum_change.first().save()
                        goods_qty_change.save()
                        pick_qty_change.save()
                        bin_qty_change.save()
                    elif int(detail_data[j].picked_qty) < pick_qty_change.pick_qty:
                        goods_qty_change.onhand_stock = goods_qty_change.onhand_stock - int(
                            detail_data[j].pick_qty)
                        goods_qty_change.pick_stock = goods_qty_change.pick_stock - dn_detail.pick_qty
                        goods_qty_change.picked_stock = goods_qty_change.picked_stock + int(
                            detail_data[j].picked_qty)
                        goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + (
                                    int(pick_qty_change.pick_qty) - int(
                                detail_data[j].pick_qty))
                        pick_qty_change.picked_qty = int(detail_data[j].picked_qty)
                        pick_qty_change.picking_status = 2
                        pick_qty_change.save()
                        bin_qty_change.goods_qty = bin_qty_change.goods_qty - int(detail_data[j].pick_qty)
                        bin_qty_change.pick_qty = bin_qty_change.pick_qty - pick_qty_change.pick_qty
                        bin_qty_change.picked_qty = bin_qty_change.picked_qty + int(detail_data[j].picked_qty)
                        if pick_sum_change.exists():
                            pick_sum_change.first().picking_status = 2
                            pick_sum_change.first().save()
                        goods_qty_change.save()
                        pick_qty_change.save()
                        bin_qty_change.save()
                    dn_detail.picked_qty = dn_detail.picked_qty + int(detail_data[j].picked_qty)
                    if dn_detail.dn_status == 3:
                        dn_detail.dn_status = 4
                    if dn_detail.pick_qty > 0:
                        dn_detail.pick_qty = 0
                    dn_detail.save()
                if DnDetailModel.objects.filter(openid=self.request.auth.openid, dn_code=str(data['dn_code']),
                                                dn_status=3).exists() is False:
                    qs.save()
                return Response({"Detail": "success"}, status=200)

class DnDispatchViewSet(viewsets.ModelViewSet):
    """
        create:
            Confirm Dispatch
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

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
            query_dict['id'] = id
            return DnListModel.objects.filter(**query_dict)
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DNListUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, pk):
        qs = self.get_object()
        if qs.dn_status != 4:
            raise APIException({"detail": "This DN Status Not Picked"})
        else:
            qs.dn_status = 5
            data = self.request.data
            dn_detail = DnDetailModel.objects.filter(openid=self.request.auth.openid,
                                                     dn_code=str(data['dn_code']),
                                                     dn_status=4, customer=qs.customer,
                                                     )
            pick_qty_change = PickingListModel.objects.filter(openid=self.request.auth.openid,
                                                              dn_code=str(data['dn_code']),
                                                              picking_status=2)
            pick_sum_change = PickingSumModel.objects.filter(openid=self.request.auth.openid,
                                                             dn_code=str(data['dn_code']),
                                                             picking_status=2)
            for i in range(len(dn_detail)):
                goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                            goods_code=dn_detail[i].goods_code).first()
                goods_qty_change.goods_qty = goods_qty_change.goods_qty - dn_detail[i].picked_qty
                goods_qty_change.picked_stock = goods_qty_change.picked_stock - dn_detail[i].picked_qty
                dn_detail[i].dn_status = 5
                dn_detail[i].intransit_qty = dn_detail[i].picked_qty
                dn_detail[i].save()
                goods_qty_change.save()
                if goods_qty_change.goods_qty == 0 and goods_qty_change.back_order_stock == 0:
                    goods_qty_change.delete()
            for j in range(len(pick_qty_change)):
                bin_qty_change = stockbin.objects.filter(openid=self.request.auth.openid,
                                                         goods_code=pick_qty_change[j].goods_code,
                                                         bin_name=pick_qty_change[j].bin_name,
                                                         t_code=pick_qty_change[j].t_code).first()
                bin_qty_change.picked_qty = bin_qty_change.picked_qty - pick_qty_change[j].picked_qty
                bin_qty_change.save()
                bin_stock_check = stockbin.objects.filter(openid=self.request.auth.openid,
                                                          goods_code=pick_qty_change[j].goods_code,
                                                          bin_name=pick_qty_change[j].bin_name,
                                                          t_code=pick_qty_change[j].t_code).first()
                if bin_stock_check.goods_qty == 0 and bin_stock_check.pick_qty == 0 and bin_stock_check.picked_qty == 0:
                    bin_stock_check.delete()
                    if stockbin.objects.filter(openid=self.request.auth.openid,
                                               bin_name=bin_stock_check.bin_name,
                                               goods_qty__gt=0).exists() is False:
                        binset.objects.filter(openid=self.request.auth.openid,
                                              bin_name=pick_qty_change[j].bin_name).update(empty_label=True)
            pick_qty_change.update(picking_status=3)
            pick_sum_change.update(picking_status=3)
            qs.save()
            return Response({"detail": "success"}, status=200)


class DnCommentsViewSet(viewsets.ModelViewSet):
    """
        create:
            Confirm Dispatch
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

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
            query_dict['id'] = id
            return DnListModel.objects.filter(**query_dict)
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DNListUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, pk):
        qs = self.get_object()
        data = self.request.data
        qs.comments = data['comments']
        qs.save()
        return Response({"detail": "success"}, status=200)

class DnPODViewSet(viewsets.ModelViewSet):
    """
        create:
            Confirm Dispatch
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

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
            query_dict['id'] = id
            return DnListModel.objects.filter(**query_dict)
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DNListUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, pk):
        qs = self.get_object()
        if qs.dn_status != 5:
            raise APIException({"detail": "This DN Status Not Intran-Sit"})
        else:
            qs.dn_status = 6
            data = self.request.data
            for i in range(len(data['goodsData'])):
                delivery_damage_qty = data['goodsData'][i].get('delivery_damage_qty')
                delivery_actual_qty = data['goodsData'][i].get('intransit_qty')
                if delivery_actual_qty < 0:
                    raise APIException({"detail": "Delivery Actual QTY Must >= 0"})
                else:
                    if delivery_damage_qty < 0:
                        raise APIException({"detail": "Delivery Damage QTY Must >= 0"})
            dn_detail = DnDetailModel.objects.filter(openid=self.request.auth.openid,
                                                     dn_code=str(data['dn_code']),
                                                     dn_status=5, customer=qs.customer,
                                                     )
            for j in range(len(data['goodsData'])):
                delivery_damage_qty = data['goodsData'][j].get('delivery_damage_qty')
                delivery_actual_qty = data['goodsData'][j].get('intransit_qty')
                goods_code = data['goodsData'][j].get('goods_code')
                if delivery_damage_qty > 0:
                    goods_detail = dn_detail.filter(goods_code=goods_code).first()
                    if delivery_actual_qty > goods_detail.intransit_qty:
                        goods_detail.delivery_actual_qty = delivery_actual_qty
                        goods_detail.delivery_more_qty = delivery_actual_qty - goods_detail.intransit_qty
                        goods_detail.delivery_damage_qty = delivery_damage_qty
                        goods_detail.intransit_qty = 0
                        goods_detail.dn_status = 6
                    elif delivery_actual_qty < goods_detail.intransit_qty:
                        goods_detail.delivery_actual_qty = delivery_actual_qty
                        goods_detail.delivery_shortage_qty = goods_detail.intransit_qty - delivery_actual_qty
                        goods_detail.delivery_damage_qty = delivery_damage_qty
                        goods_detail.intransit_qty = 0
                        goods_detail.dn_status = 6
                    elif delivery_actual_qty == goods_detail.intransit_qty:
                        goods_detail.delivery_actual_qty = delivery_actual_qty
                        goods_detail.delivery_damage_qty = delivery_damage_qty
                        goods_detail.intransit_qty = 0
                        goods_detail.dn_status = 6
                    else:
                        continue
                    goods_detail.save()
                elif delivery_damage_qty == 0:
                    goods_detail = dn_detail.filter(goods_code=goods_code).first()
                    if delivery_actual_qty > goods_detail.intransit_qty:
                        goods_detail.delivery_actual_qty = delivery_actual_qty
                        goods_detail.delivery_more_qty = delivery_actual_qty - goods_detail.intransit_qty
                        goods_detail.intransit_qty = 0
                        goods_detail.dn_status = 6
                    elif delivery_actual_qty < goods_detail.intransit_qty:
                        goods_detail.delivery_actual_qty = delivery_actual_qty
                        goods_detail.delivery_shortage_qty = goods_detail.intransit_qty - delivery_actual_qty
                        goods_detail.intransit_qty = 0
                        goods_detail.dn_status = 6
                    elif delivery_actual_qty == goods_detail.intransit_qty:
                        goods_detail.delivery_actual_qty = delivery_actual_qty
                        goods_detail.intransit_qty = 0
                        goods_detail.dn_status = 6
                    else:
                        continue
                    goods_detail.save()
            qs.save()
            return Response({"detail": "success"}, status=200)

class FileListDownloadView(viewsets.ModelViewSet):
    renderer_classes = (FileListRenderCN, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnListFilter

    def get_project(self):
        try:
            id = self.kwargs.get('pk')
            return id
        except:
            return None

    def get_queryset(self):
        id = self.get_project()
        if self.request.user:
            empty_qs = DnListModel.objects.filter(
                Q(openid=self.request.auth.openid, dn_status=1, is_delete=False) & Q(customer=''))
            cur_date = timezone.now()
            date_check = relativedelta(day=1)
            if len(empty_qs) > 0:
                for i in range(len(empty_qs)):
                    if empty_qs[i].create_time <= cur_date - date_check:
                        empty_qs[i].delete()
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
            return DnListModel.objects.filter(Q(**query_dict) & ~Q(customer=''))
        else:
            return DnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.FileListRenderSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')
        if lang:
            if lang == 'zh-hans':
                return FileListRenderCN().render(data)
            else:
                return FileListRenderEN().render(data)
        else:
            return FileListRenderEN().render(data)

    def list(self, request, *args, **kwargs):
        from datetime import datetime
        dt = datetime.now()
        data = (
            FileListRenderSerializer(instance).data
            for instance in self.filter_queryset(self.get_queryset())
        )
        renderer = self.get_lang(data)
        response = StreamingHttpResponse(
            renderer,
            content_type="text/csv"
        )
        response['Content-Disposition'] = "attachment; filename='dnlist_{}.csv'".format(str(dt.strftime('%Y%m%d%H%M%S%f')))
        return response

class FileDetailDownloadView(viewsets.ModelViewSet):
    renderer_classes = (FileDetailRenderCN, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
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
        if self.action in ['list']:
            return serializers.FileDetailRenderSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')
        if lang:
            if lang == 'zh-hans':
                return FileDetailRenderCN().render(data)
            else:
                return FileDetailRenderEN().render(data)
        else:
            return FileDetailRenderEN().render(data)

    def list(self, request, *args, **kwargs):
        from datetime import datetime
        dt = datetime.now()
        data = (
            FileDetailRenderSerializer(instance).data
            for instance in self.filter_queryset(self.get_queryset())
        )
        renderer = self.get_lang(data)
        response = StreamingHttpResponse(
            renderer,
            content_type="text/csv"
        )
        response['Content-Disposition'] = "attachment; filename='dndetail_{}.csv'".format(str(dt.strftime('%Y%m%d%H%M%S%f')))
        return response


class PickListDownloadView(viewsets.ModelViewSet):
    renderer_classes = (FileListRenderCN, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = DnPickingListFilter

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
            query_dict = {"picking_status": 1}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            return PickingListModel.objects.filter(**query_dict)
        else:
            return PickingListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.DNPickingListGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')
        if lang:
            if lang == 'zh-hans':
                return PickListRenderCN().render(data)
            else:
                return PickListRenderEN().render(data)
        else:
            return FileListRenderEN().render(data)

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset()).order_by('bin_name').values('bin_name','goods_code').annotate(pick_qty=Sum('pick_qty')).values('bin_name','goods_code','picker','pick_qty','picked_qty')
        from datetime import datetime
        dt = datetime.now()
        data = (
            serializers.DNPickingListGetSerializer(instance).data
            for instance in qs
        )
        renderer = self.get_lang(data)
        response = StreamingHttpResponse(
            renderer,
            content_type="text/csv"
        )
        response['Content-Disposition'] = "attachment; filename='picklist_{}.csv'".format(str(dt.strftime('%Y%m%d%H%M%S%f')))
        return response


import requests, base64
from django.conf import settings
def get_mian_dan(request):
    if request.method.lower() == 'post':
        dn_list = DnListModel.objects.filter(openid=request.META.get('HTTP_TOKEN'), mian_dan='')
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'APItoken': 'e7d82-0913c-5fe10-603c2-be99e-a42e9-a837'
        }
        for i in range(len((dn_list))):
            try:
                res = requests.get('https://api.teapplix.com/api2/Shipment?ReturnLabel=1&TxnId=' + dn_list[i].txnid,
                                   headers=headers).json().get('Items', '')
                if len(res) > 0:
                    dn_list[i].carrier = res[0].get('TrackingInfo', '').get('CarrierName').strip()
                    dn_list[i].trackingnumber = str(res[0].get('TrackingInfo', '').get('TrackingNumber')).strip()
                    dn_list[i].mian_dan = res[0].get('LabelData', '').strip()
                    dn_list[i].have_mian_dan = True
                    if CarrierList.objects.filter(carrier=res[0].get('TrackingInfo', '').get('CarrierName')).exists() is False:
                        CarrierList.objects.create(
                            carrier=res[0].get('TrackingInfo', '').get('CarrierName').strip()
                        )
                    DnDetailModel.objects.filter(txnid=dn_list[i].txnid).update(
                        carrier=res[0].get('TrackingInfo', '').get('CarrierName').strip(),
                        trackingnumber=str(res[0].get('TrackingInfo', '').get('TrackingNumber')).strip(),
                        mian_dan=res[0].get('LabelData', '').strip(),
                        have_mian_dan=True
                    )
                    scanner.objects.create(openid='SCANGOODS', mode="MD",
                                           code=str(res[0].get('TrackingInfo', '').get('TrackingNumber')).strip(),
                                           bar_code=str(res[0].get('TrackingInfo', '').get('TrackingNumber')).strip())
                    dn_list[i].save()
                    # decoded_data = base64.b64decode(res[0].get('LabelData', '').strip())
                    # path = str(settings.BASE_DIR) + '/media/miandan/' + str(dn_list[i].txnid) + '.pdf'
                    # with open(path, 'wb') as file:
                    #     file.write(decoded_data)
                else:
                    continue
            except:
                continue
            finally:
                pass
        return JsonResponse({"detail": "success"}, status=200)

class confirmOrdersViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）
    """
    pagination_class = MyPageNumberPaginationDNDetail
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
            query_dict = {'dn_status': 1, 'is_delete': False}
            if self.request.auth.openid != superopenid:
                query_dict['openid'] = self.request.auth.openid
            if id is not None:
                query_dict['id'] = id
            return DnDetailModel.objects.filter(**query_dict)
        else:
            return DnDetailModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DNDetailGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        qs_list = self.filter_queryset(self.get_queryset())
        for i in range(len(qs_list)):
            qs = qs_list[i]
            if qs.openid != self.request.auth.openid:
                raise APIException({"detail": "不能确认非你仓库的订单"})
            else:
                DnListModel.objects.filter(openid=self.request.auth.openid, dn_code=qs.dn_code,
                                           dn_status=1, is_delete=False).update(dn_status=2)
                qs.dn_status = 2
                if stocklist.objects.filter(openid=self.request.auth.openid,
                                            goods_code=str(qs.goods_code)).exists():
                    pass
                else:
                    goods_detail = goods.objects.filter(goods_code=str(qs.goods_code)).first()
                    stocklist.objects.create(openid=self.request.auth.openid,
                                             goods_code=str(qs.goods_code),
                                             goods_desc=goods_detail.goods_desc,
                                             supplier=goods_detail.goods_supplier)
                goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                            goods_code=str(
                                                                qs.goods_code)).first()
                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - qs.goods_qty
                goods_qty_change.ordered_stock = goods_qty_change.ordered_stock + qs.goods_qty
                goods_qty_change.dn_stock = goods_qty_change.dn_stock - qs.goods_qty
                if goods_qty_change.can_order_stock < 0:
                    goods_qty_change.can_order_stock = 0
                goods_qty_change.save()
                qs.save()
        return Response({'detail': 'success'}, status=200)