from collections import OrderedDict

from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param

from supplier.models import ListModel as supplier
from warehouse.models import ListModel as warehouse

class MyPageNumberPaginationASNList(PageNumberPagination):
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
        supplier_list_data = supplier.objects.filter(is_delete=False)
        supplier_list = []
        for i in range(len(supplier_list_data)):
            supplier_list.append(supplier_list_data[i].supplier_name)
        warehouse_list_data = warehouse.objects.filter(openid=self.request.auth.openid, is_delete=False)
        warehouse_list = []
        for i in range(len(warehouse_list_data)):
            warehouse_dict = {
                "id": warehouse_list_data[i].pk,
                "warehosue_name": warehouse_list_data[i].warehouse_name,
                "warehouse_id": warehouse_list_data[i].warehouse_id
            }
            warehouse_list.append(warehouse_dict)
        return Response(OrderedDict([
            ('supplier_list', supplier_list),
            ('warehouse_list', warehouse_list),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
