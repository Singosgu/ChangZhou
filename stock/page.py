from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from userprofile.models import Users

class MyPageNumberPaginationStaff(PageNumberPagination):
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 1000
    page_query_param = 'page'

    def get_paginated_response(self, data):
        data[0]['vip'] = Users.objects.filter(openid=self.request.auth.openid).first().vip
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
