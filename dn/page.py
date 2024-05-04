from collections import OrderedDict
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

from customer.models import ListModel as customer
from warehouse.models import ListModel as warehouse
from .models import OrderTypeList as ordertype
from .models import CarrierList as carrierlist
from binset.models import ListModel as binset
from staff.models import ListModel as staff

class MyPageNumberPaginationDNList(PageNumberPagination):
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 10000
    page_query_param = 'page'

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        ssl_check = str(self.request.META.get('HTTP_ORIGIN')).split('://')[0]
        url_combine = str(url).split('://')
        if len(str(url).split('://')) == 2:
            url = ssl_check + '://' + url_combine[1]
            if page_number == 1:
                return remove_query_param(url, self.page_query_param)
            return replace_query_param(url, self.page_query_param, page_number)
        elif len(str(url).split('://')) == 3:
            url = ssl_check + '://' + url_combine[1] + ':' + url_combine[2]
            if page_number == 1:
                return remove_query_param(url, self.page_query_param)
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            raise APIException({"detail": "Wrong API Url"})

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        ssl_check = str(self.request.META.get('HTTP_ORIGIN')).split('://')[0]
        url_combine = str(url).split('://')
        if len(str(url).split('://')) == 2:
            url = ssl_check + '://' + url_combine[1]
            return replace_query_param(url, self.page_query_param, page_number)
        elif len(str(url).split('://')) == 3:
            url = ssl_check + '://' + url_combine[1] + ':' + url_combine[2]
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            raise APIException({"detail": "Wrong API Url"})

    def get_paginated_response(self, data):
        customer_list_data = customer.objects.filter(is_delete=False)
        customer_list = []
        for i in range(len(customer_list_data)):
            customer_list.append(customer_list_data[i].customer_name)
        warehouse_list_data = warehouse.objects.filter(is_delete=False)
        warehouse_list = []
        for i in range(len(warehouse_list_data)):
            warehouse_dict = {
                "id": warehouse_list_data[i].pk,
                "warehosue_name": warehouse_list_data[i].warehouse_name,
                "warehouse_id": warehouse_list_data[i].warehouse_id
            }
            warehouse_list.append(warehouse_dict)
        order_type_list_data = ordertype.objects.all()
        order_type_list = []
        for i in range(len(order_type_list_data)):
            order_type_list.append(order_type_list_data[i].order_type)
        carrier_list_data = carrierlist.objects.all()
        carrier_list = []
        for i in range(len(carrier_list_data)):
            carrier_list.append(carrier_list_data[i].carrier)
        return Response(OrderedDict([
            ('carrier_list', carrier_list),
            ('order_type_list', order_type_list),
            ('customer_list', customer_list),
            ('warehouse_list', warehouse_list),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

class MyPageNumberPaginationDNDetail(PageNumberPagination):
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 10000
    page_query_param = 'page'

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        ssl_check = str(self.request.META.get('HTTP_ORIGIN')).split('://')[0]
        url_combine = str(url).split('://')
        if len(str(url).split('://')) == 2:
            url = ssl_check + '://' + url_combine[1]
            if page_number == 1:
                return remove_query_param(url, self.page_query_param)
            return replace_query_param(url, self.page_query_param, page_number)
        elif len(str(url).split('://')) == 3:
            url = ssl_check + '://' + url_combine[1] + ':' + url_combine[2]
            if page_number == 1:
                return remove_query_param(url, self.page_query_param)
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            raise APIException({"detail": "Wrong API Url"})

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        ssl_check = str(self.request.META.get('HTTP_ORIGIN')).split('://')[0]
        url_combine = str(url).split('://')
        if len(str(url).split('://')) == 2:
            url = ssl_check + '://' + url_combine[1]
            return replace_query_param(url, self.page_query_param, page_number)
        elif len(str(url).split('://')) == 3:
            url = ssl_check + '://' + url_combine[1] + ':' + url_combine[2]
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            raise APIException({"detail": "Wrong API Url"})

    def get_paginated_response(self, data):
        customer_list_data = customer.objects.filter(is_delete=False)
        customer_list = []
        for i in range(len(customer_list_data)):
            customer_list.append(customer_list_data[i].customer_name)
        warehouse_list_data = warehouse.objects.filter(is_delete=False)
        warehouse_list = []
        for i in range(len(warehouse_list_data)):
            warehouse_dict = {
                "id": warehouse_list_data[i].pk,
                "warehosue_name": warehouse_list_data[i].warehouse_name,
                "warehouse_id": warehouse_list_data[i].warehouse_id
            }
            warehouse_list.append(warehouse_dict)
        order_type_list_data = ordertype.objects.all()
        order_type_list = []
        for i in range(len(order_type_list_data)):
            order_type_list.append(order_type_list_data[i].order_type)
        carrier_list_data = carrierlist.objects.all()
        carrier_list = []
        for i in range(len(carrier_list_data)):
            carrier_list.append(carrier_list_data[i].carrier)
        return Response(OrderedDict([
            ('carrier_list', carrier_list),
            ('order_type_list', order_type_list),
            ('customer_list', customer_list),
            ('warehouse_list', warehouse_list),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

class MyPageNumberPaginationPicking(PageNumberPagination):
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 10000
    page_query_param = 'page'

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        ssl_check = str(self.request.META.get('HTTP_ORIGIN')).split('://')[0]
        url_combine = str(url).split('://')
        if len(str(url).split('://')) == 2:
            url = ssl_check + '://' + url_combine[1]
            if page_number == 1:
                return remove_query_param(url, self.page_query_param)
            return replace_query_param(url, self.page_query_param, page_number)
        elif len(str(url).split('://')) == 3:
            url = ssl_check + '://' + url_combine[1] + ':' + url_combine[2]
            if page_number == 1:
                return remove_query_param(url, self.page_query_param)
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            raise APIException({"detail": "Wrong API Url"})

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        ssl_check = str(self.request.META.get('HTTP_ORIGIN')).split('://')[0]
        url_combine = str(url).split('://')
        if len(str(url).split('://')) == 2:
            url = ssl_check + '://' + url_combine[1]
            return replace_query_param(url, self.page_query_param, page_number)
        elif len(str(url).split('://')) == 3:
            url = ssl_check + '://' + url_combine[1] + ':' + url_combine[2]
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            raise APIException({"detail": "Wrong API Url"})

    def get_paginated_response(self, data):
        bin_list_data = binset.objects.filter(openid=self.request.auth.openid, is_delete=False).order_by('bin_name')
        bin_list = []
        for i in range(len(bin_list_data)):
            try:
                bin_data = bin_list_data[i].bin_name.split('-')
                if bin_data[0] not in bin_list:
                    bin_list.append(bin_data[0])
            except:
                if bin_list_data[i].bin_name not in bin_list:
                    bin_list.append(bin_list_data[i].bin_name)
            finally:
                pass
        staff_list_data = staff.objects.filter(openid=self.request.auth.openid, is_delete=False, is_lock=False)
        staff_list = []
        for i in range(len(staff_list_data)):
            staff_list.append(staff_list_data[i].staff_name)
        return Response(OrderedDict([
            ('staff_list', staff_list),
            ('bin_list', bin_list),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))