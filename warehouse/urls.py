from django.urls import path, re_path
from . import views

urlpatterns = [
path(r'', views.APIViewSet.as_view({"get": "list", "post": "create"}), name="warehouse"),
re_path(r'^(?P<pk>\d+)/$', views.APIViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}), name="warehouse_1"),
path(r'getallwarehouse/', views.GetAllViewSet.as_view({"get": "list"}), name="getallwarehouse"),
path(r'getorder/', views.GetOrderViewSet.as_view({"post": "create"}), name="getorder")
]
