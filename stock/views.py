from rest_framework import viewsets
from .models import StockListModel, StockBinModel
from . import serializers
from utils.page import MyPageNumberPagination
from utils.md5 import Md5
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .filter import StockListFilter, StockBinFilter
from rest_framework.exceptions import APIException
from stock.models import StockListModel as stocklist
from binset.models import ListModel as binset
from .serializers import FileListRenderSerializer, FileBinListRenderSerializer
from django.http import StreamingHttpResponse
from .files import FileListRenderCN, FileListRenderEN, FileBinListRenderCN, FileBinListRenderEN
from rest_framework.settings import api_settings
from userprofile.models import Users
from django.db.models import Q

class StockListViewSet(viewsets.ModelViewSet):
    """
        list:
            Response a data list（all）
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = StockListFilter

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
            if self.request.GET.get('search'):
                return StockListModel.objects.filter(openid=self.request.auth.openid, goods_code__icontains=self.request.GET.get('search'))
            return StockListModel.objects.filter(**query_dict)
        else:
            return StockListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.StockListGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

class StockBinViewSet(viewsets.ModelViewSet):
    """
        list:
            Response a data list（all）
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = StockBinFilter

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
            if self.request.GET.get('search'):
                return StockBinModel.objects.filter(Q(openid=self.request.auth.openid, goods_code__icontains=self.request.GET.get('search')) | Q(openid=self.request.auth.openid, bin_name__icontains=self.request.GET.get('search')))
            return StockBinModel.objects.filter(**query_dict)
        else:
            return StockBinModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.StockBinGetSerializer
        elif self.action in ['create', 'update']:
            return serializers.StockBinPostSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, pk):
        qs = self.get_object()
        if qs.openid != self.request.auth.openid:
            raise APIException({"detail": "Cannot update data which not yours"})
        else:
            data = self.request.data
            if 'bin_name' not in data and 'move_to_bin' not in data:
                raise APIException({"detail": "Please Enter The Bin Name"})
            else:
                current_bin_detail = binset.objects.filter(openid=self.request.auth.openid,
                                                   bin_name=str(data['bin_name'])).first()
                move_to_bin_detail = binset.objects.filter(openid=self.request.auth.openid,
                                                   bin_name=str(data['move_to_bin'])).first()
                goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                            goods_code=str(data['goods_code'])).first()
                if int(data['move_qty']) <= 0:
                    raise APIException({"detail": "Move QTY Must > 0"})
                else:
                    bin_move_qty_res = qs.goods_qty - qs.pick_qty - int(data['move_qty'])
                    try:
                        bin_level = int(move_to_bin_detail.bin_name.split('-')[2]) + 1
                    except:
                        bin_level = 1
                    if bin_move_qty_res > 0:
                        qs.goods_qty = qs.pick_qty + bin_move_qty_res
                        if current_bin_detail.bin_property == 'Damage':
                            if move_to_bin_detail.bin_property == 'Damage':
                                pass
                            elif move_to_bin_detail.bin_property == 'Inspection':
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data['move_qty'])
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Holding':
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data['move_qty'])
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data['move_qty'])
                            else:
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data['move_qty'])
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(data['move_qty'])
                        elif current_bin_detail.bin_property == 'Inspection':
                            if move_to_bin_detail.bin_property == 'Damage':
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(data['move_qty'])
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Inspection':
                                pass
                            elif move_to_bin_detail.bin_property == 'Holding':
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(data['move_qty'])
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data['move_qty'])
                            else:
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(data['move_qty'])
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(data['move_qty'])
                        elif current_bin_detail.bin_property == 'Holding':
                            if move_to_bin_detail.bin_property == 'Damage':
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data['move_qty'])
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Inspection':
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data['move_qty'])
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Holding':
                                pass
                            else:
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data['move_qty'])
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(data['move_qty'])
                        else:
                            if move_to_bin_detail.bin_property == 'Damage':
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(data['move_qty'])
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Inspection':
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(data['move_qty'])
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Holding':
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(data['move_qty'])
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data['move_qty'])
                            else:
                                pass
                        StockBinModel.objects.create(openid=self.request.auth.openid,
                                                     bin_name=str(data['move_to_bin']),
                                                     goods_code=str(data['goods_code']),
                                                     goods_desc=goods_qty_change.goods_desc,
                                                     goods_qty=int(data['move_qty']),
                                                     bin_size=move_to_bin_detail.bin_size,
                                                     bin_property=move_to_bin_detail.bin_property,
                                                     bin_level=bin_level,
                                                     t_code=Md5.md5(str(data['goods_code'])),
                                                     create_time=qs.create_time
                                                     )
                        if move_to_bin_detail.empty_label is True:
                            move_to_bin_detail.empty_label = False
                            move_to_bin_detail.save()
                        goods_qty_change.save()
                        qs.save()
                        delete_data = StockBinModel.objects.filter(openid=self.request.auth.openid,
                                                                   goods_qty=0,
                                                                   pick_qty=0,
                                                                   picked_qty=0)
                        if delete_data.exists():
                            for i in delete_data:
                                i.delete()
                    elif bin_move_qty_res == 0:
                        qs.goods_qty = qs.pick_qty
                        if current_bin_detail.bin_property == 'Damage':
                            if move_to_bin_detail.bin_property == 'Damage':
                                pass
                            elif move_to_bin_detail.bin_property == 'Inspection':
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data['move_qty'])
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Holding':
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data['move_qty'])
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data['move_qty'])
                            else:
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data['move_qty'])
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(data['move_qty'])
                        elif current_bin_detail.bin_property == 'Inspection':
                            if move_to_bin_detail.bin_property == 'Damage':
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(data['move_qty'])
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Inspection':
                                pass
                            elif move_to_bin_detail.bin_property == 'Holding':
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(data['move_qty'])
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data['move_qty'])
                            else:
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(data['move_qty'])
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(data['move_qty'])
                        elif current_bin_detail.bin_property == 'Holding':
                            if move_to_bin_detail.bin_property == 'Damage':
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data['move_qty'])
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Inspection':
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data['move_qty'])
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Holding':
                                pass
                            else:
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data['move_qty'])
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(data['move_qty'])
                        else:
                            if move_to_bin_detail.bin_property == 'Damage':
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(data['move_qty'])
                                goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Inspection':
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(data['move_qty'])
                                goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(data['move_qty'])
                            elif move_to_bin_detail.bin_property == 'Holding':
                                goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(data['move_qty'])
                                goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data['move_qty'])
                            else:
                                pass
                        StockBinModel.objects.create(openid=self.request.auth.openid,
                                                     bin_name=str(data['move_to_bin']),
                                                     goods_code=str(data['goods_code']),
                                                     goods_desc=goods_qty_change.goods_desc,
                                                     goods_qty=int(data['move_qty']),
                                                     bin_size=move_to_bin_detail.bin_size,
                                                     bin_property=move_to_bin_detail.bin_property,
                                                     bin_level=bin_level,
                                                     t_code=Md5.md5(str(data['goods_code'])),
                                                     create_time=qs.create_time
                                                     )
                        if move_to_bin_detail.empty_label is True:
                            move_to_bin_detail.empty_label = False
                            move_to_bin_detail.save()
                        goods_qty_change.save()
                        qs.save()
                        delete_data = StockBinModel.objects.filter(openid=self.request.auth.openid,
                                                                   goods_qty=0,
                                                                   pick_qty=0,
                                                                   picked_qty=0)
                        if delete_data.exists():
                            for i in delete_data:
                                i.delete()
                        if StockBinModel.objects.filter(openid=self.request.auth.openid,
                                                        bin_name=str(data['bin_name'])).exists() is False:
                            current_bin_detail.empty_label = True
                        current_bin_detail.save()

                    elif bin_move_qty_res < 0:
                        raise APIException({"detail": "Move Qty must < Bin Goods Qty"})
                    else:
                        pass
                headers = self.get_success_headers(data)
                return Response(data, status=200, headers=headers)

    def update(self, request, *args, **kwargs):
        qs = StockBinModel.objects.filter(openid=self.request.auth.openid)
        data = self.request.data
        for i in range(len(data)):
            if 'bin_name' not in data[i] and 'move_to_bin' not in data[i]:
                raise APIException({"detail": "Please Enter The Bin Name"})
        for j in range(len(data)):
            current_bin_detail = binset.objects.filter(openid=self.request.auth.openid,
                                                       bin_name=str(data[j]['bin_name'])).first()
            move_to_bin_detail = binset.objects.filter(openid=self.request.auth.openid,
                                                       bin_name=str(data[j]['move_to_bin'])).first()
            goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                        goods_code=str(data[j]['goods_code'])).first()
            qs_project = qs.filter(t_code=data[j]['t_code']).first()
            if int(data[j]['move_qty']) <= 0:
                raise APIException({"detail": "Move QTY Must > 0"})
            else:
                bin_move_qty_res = qs_project.goods_qty - qs_project.pick_qty - int(
                    data[j]['move_qty'])
                try:
                    bin_level = int(move_to_bin_detail.bin_name.split('-')[2]) + 1
                except:
                    bin_level = 1
                if bin_move_qty_res > 0:
                    qs_project.goods_qty = qs_project.pick_qty + bin_move_qty_res
                    if current_bin_detail.bin_property == 'Damage':
                        if move_to_bin_detail.bin_property == 'Damage':
                            pass
                        elif move_to_bin_detail.bin_property == 'Inspection':
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data[j]['move_qty'])
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(
                                data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Holding':
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data[j]['move_qty'])
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data[j]['move_qty'])
                        else:
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data[j]['move_qty'])
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(
                                data[j]['move_qty'])
                    elif current_bin_detail.bin_property == 'Inspection':
                        if move_to_bin_detail.bin_property == 'Damage':
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Inspection':
                            pass
                        elif move_to_bin_detail.bin_property == 'Holding':
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data[j]['move_qty'])
                        else:
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(
                                data[j]['move_qty'])
                    elif current_bin_detail.bin_property == 'Holding':
                        if move_to_bin_detail.bin_property == 'Damage':
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data[j]['move_qty'])
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Inspection':
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data[j]['move_qty'])
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(
                                data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Holding':
                            pass
                        else:
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data[j]['move_qty'])
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(
                                data[j]['move_qty'])
                    else:
                        if move_to_bin_detail.bin_property == 'Damage':
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Inspection':
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(
                                data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Holding':
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data[j]['move_qty'])
                        else:
                            pass
                    StockBinModel.objects.create(openid=self.request.auth.openid,
                                                 bin_name=str(data[j]['move_to_bin']),
                                                 goods_code=str(data[j]['goods_code']),
                                                 goods_desc=goods_qty_change.goods_desc,
                                                 goods_qty=int(data[j]['move_qty']),
                                                 bin_size=move_to_bin_detail.bin_size,
                                                 bin_property=move_to_bin_detail.bin_property,
                                                 bin_level=bin_level,
                                                 t_code=Md5.md5(str(data[j]['goods_code'])),
                                                 create_time=qs_project.create_time
                                                 )
                    if move_to_bin_detail.empty_label is True:
                        move_to_bin_detail.empty_label = False
                        move_to_bin_detail.save()
                    goods_qty_change.save()
                    qs_project.save()
                    delete_data = StockBinModel.objects.filter(openid=self.request.auth.openid,
                                                               goods_qty=0,
                                                               pick_qty=0,
                                                               picked_qty=0)
                    if delete_data.exists():
                        for i in delete_data:
                            i.delete()
                elif bin_move_qty_res == 0:
                    qs_project.goods_qty = qs_project.pick_qty
                    if current_bin_detail.bin_property == 'Damage':
                        if move_to_bin_detail.bin_property == 'Damage':
                            pass
                        elif move_to_bin_detail.bin_property == 'Inspection':
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data[j]['move_qty'])
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(
                                data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Holding':
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data[j]['move_qty'])
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data[j]['move_qty'])
                        else:
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock - int(data[j]['move_qty'])
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(
                                data[j]['move_qty'])
                    elif current_bin_detail.bin_property == 'Inspection':
                        if move_to_bin_detail.bin_property == 'Damage':
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Inspection':
                            pass
                        elif move_to_bin_detail.bin_property == 'Holding':
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data[j]['move_qty'])
                        else:
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(
                                data[j]['move_qty'])
                    elif current_bin_detail.bin_property == 'Holding':
                        if move_to_bin_detail.bin_property == 'Damage':
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data[j]['move_qty'])
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Inspection':
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data[j]['move_qty'])
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(
                                data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Holding':
                            pass
                        else:
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock - int(data[j]['move_qty'])
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock + int(
                                data[j]['move_qty'])
                    else:
                        if move_to_bin_detail.bin_property == 'Damage':
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.damage_stock = goods_qty_change.damage_stock + int(data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Inspection':
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.inspect_stock = goods_qty_change.inspect_stock + int(
                                data[j]['move_qty'])
                        elif move_to_bin_detail.bin_property == 'Holding':
                            goods_qty_change.can_order_stock = goods_qty_change.can_order_stock - int(
                                data[j]['move_qty'])
                            goods_qty_change.hold_stock = goods_qty_change.hold_stock + int(data[j]['move_qty'])
                        else:
                            pass
                    StockBinModel.objects.create(openid=self.request.auth.openid,
                                                 bin_name=str(data[j]['move_to_bin']),
                                                 goods_code=str(data[j]['goods_code']),
                                                 goods_desc=goods_qty_change.goods_desc,
                                                 goods_qty=int(data[j]['move_qty']),
                                                 bin_size=move_to_bin_detail.bin_size,
                                                 bin_property=move_to_bin_detail.bin_property,
                                                 bin_level=bin_level,
                                                 t_code=Md5.md5(str(data[j]['goods_code'])),
                                                 create_time=qs_project.create_time
                                                 )
                    if move_to_bin_detail.empty_label is True:
                        move_to_bin_detail.empty_label = False
                        move_to_bin_detail.save()
                    goods_qty_change.save()
                    qs_project.save()
                    delete_data = StockBinModel.objects.filter(openid=self.request.auth.openid,
                                                               goods_qty=0,
                                                               pick_qty=0,
                                                               picked_qty=0)
                    if delete_data.exists():
                        for i in delete_data:
                            i.delete()
                    if StockBinModel.objects.filter(openid=self.request.auth.openid,
                                                    bin_name=str(data[j]['bin_name'])).exists() is False:
                        current_bin_detail.empty_label = True
                    current_bin_detail.save()

                elif bin_move_qty_res < 0:
                    raise APIException({"detail": "Move Qty must < Bin Goods Qty"})
                else:
                    pass
        headers = self.get_success_headers(data)
        return Response(data, status=200, headers=headers)

class FileListDownloadView(viewsets.ModelViewSet):
    renderer_classes = (FileListRenderCN, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = StockListFilter

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
            return StockListModel.objects.filter(**query_dict)
        else:
            return StockListModel.objects.none()

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
        response['Content-Disposition'] = "attachment; filename='stocklist_{}.csv'".format(str(dt.strftime('%Y%m%d%H%M%S%f')))
        return response

class FileBinListDownloadView(viewsets.ModelViewSet):
    renderer_classes = (FileBinListRenderCN, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = StockBinFilter

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
            return StockBinModel.objects.filter(**query_dict)
        else:
            return StockBinModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.FileBinListRenderSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')
        if lang:
            if lang == 'zh-hans':
                return FileBinListRenderCN().render(data)
            else:
                return FileBinListRenderEN().render(data)
        else:
            return FileBinListRenderEN().render(data)

    def list(self, request, *args, **kwargs):
        from datetime import datetime
        dt = datetime.now()
        data = (
            FileBinListRenderSerializer(instance).data
            for instance in self.filter_queryset(self.get_queryset())
        )
        renderer = self.get_lang(data)
        response = StreamingHttpResponse(
            renderer,
            content_type="text/csv"
        )
        response['Content-Disposition'] = "attachment; filename='stockbinlist_{}.csv'".format(str(dt.strftime('%Y%m%d%H%M%S%f')))
        return response
