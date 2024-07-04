from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from userprofile.models import Users
from binset.models import ListModel as binset

class MyPageNumberPaginationStaff(PageNumberPagination):
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 1000
    page_query_param = 'page'

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
        if len(data):
            data[0]['vip'] = Users.objects.filter(openid=self.request.auth.openid).first().vip
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('bin_list', bin_list),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
