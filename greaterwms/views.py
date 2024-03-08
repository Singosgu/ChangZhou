from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from wsgiref.util import FileWrapper
from rest_framework.exceptions import APIException
import mimetypes, os

def robots(request):
    path = settings.BASE_DIR + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def favicon(request):
    path = str(settings.BASE_DIR) + '/static/img/logo.png'
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def css(request):
    path = str(settings.BASE_DIR) + '/templates/dist/spa' + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def js(request):
    path = str(settings.BASE_DIR) + '/templates/dist/spa' + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def statics(request):
    path = str(settings.BASE_DIR) + '/templates/dist/spa' + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def fonts(request):
    path = str(settings.BASE_DIR) + '/templates/dist/spa' + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def myip(request):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    print(s.getsockname()[0])
    ip = s.getsockname()[0]
    s.close()
    return JsonResponse({"ip": ip})

def checkstock(request, t_code, qty):
    from stock.models import StockBinModel as sb
    stock_detail = sb.objects.filter(t_code=t_code).first()
    stock_detail.goods_qty = qty
    stock_detail.save()
    return JsonResponse({"detail": "success"})

def changetype(request, bin, type):
    from stock.models import StockBinModel as sb
    stock_detail = sb.objects.filter(bin_name=bin)
    stock_detail.update(bin_property=type)
    return JsonResponse({"detail": bin, "type": type})

def fixasn(request, openid, asn_code, status):
    from asn.models import AsnListModel, AsnDetailModel
    from scanner.models import ListModel as scanner
    from utils.md5 import Md5
    asn_list = AsnListModel.objects.filter(openid=openid, asn_code=asn_code)
    asn_detail = AsnDetailModel.objects.filter(openid=openid, asn_code=asn_code, asn_status=status)
    asn_detail.update(asn_code=asn_code + '1A')
    bar_code = Md5.md5(asn_code)
    scanner.objects.create(openid=asn_list.first().openid, mode="ASN", code=asn_code + '1A',
                           bar_code=bar_code)
    AsnListModel.objects.filter(openid=openid, asn_code=asn_code + '1A').delete()
    AsnListModel.objects.create(
        asn_code=asn_code + '1A',
        asn_status=3,
        total_weight=asn_list.first().total_weight,
        total_volume=asn_list.first().total_volume,
        total_cost=asn_list.first().total_cost,
        supplier=asn_list.first().supplier,
        patch_number=asn_list.first().patch_number,
        warehouse_id=asn_list.first().warehouse_id,
        creater=asn_list.first().creater,
        bar_code=bar_code,
        openid=asn_list.first().openid,
        box_number=asn_list.first().box_number
    )
    asn_list.update(asn_status=5)
    return JsonResponse({"detail": 'success'})


def changeasn(request):
    from asn.models import AsnListModel, AsnDetailModel
    from scanner.models import ListModel as scanner
    AsnListModel.objects.filter(asn_code='ASN2023101311A').update(asn_code='ASN2023101311')
    AsnDetailModel.objects.filter(asn_code='ASN2023101311A').update(asn_code='ASN2023101311')
    scanner.objects.filter(mode="ASN", code='ASN2023101311A').update(code='ASN2023101311')
    return JsonResponse({"detail": 'success'})

def changedn(request, oldvalue, newvalue):
    from dn.models import DnListModel, DnDetailModel, PickingListModel
    from scanner.models import ListModel as scanner
    DnListModel.objects.filter(dn_code=oldvalue, dn_status=3).update(dn_code=newvalue)
    DnDetailModel.objects.filter(dn_code=oldvalue, dn_status=3).update(dn_code=newvalue)
    PickingListModel.objects.filter(dn_code=oldvalue, picking_status=0).update(dn_code=newvalue)
    scanner.objects.filter(mode="DN", code=oldvalue).update(code=newvalue)
    return JsonResponse({"detail": 'success'})

def initW99(request):
    from stock.models import StockBinModel
    StockBinModel.objects.filter(bin_name='W99-01-9-L', bin_level__lt=10).update(bin_level=10)
    return JsonResponse({"detail": 'success'})