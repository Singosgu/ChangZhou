from django.urls import path
from . import views

urlpatterns = [
path(r'goodslistfile/', views.GoodlistfileViewSet.as_view(), name="goodslistfile"),
path(r'supplierfile/', views.SupplierfileViewSet.as_view(), name="suppplierfile"),
path(r'customerfile/', views.CustomerfileViewSet.as_view(), name="customerfile"),
path(r'capitalfile/', views.CapitalfileViewSet.as_view(), name="capitalfile"),
path(r'freightfile/', views.FreightfileViewSet.as_view(), name="freightfile"),
path(r'stockfile/', views.StockInitViewSet.as_view(), name="stockfile"),
path(r'binfile/', views.BinViewSet.as_view(), name="binfile"),
path(r'goodslistfileadd/', views.GoodlistfileAddViewSet.as_view(), name="goodslistfileadd"),
path(r'supplierfileadd/', views.SupplierfileAddViewSet.as_view(), name="suppplierfileadd"),
path(r'customerfileadd/', views.CustomerfileAddViewSet.as_view(), name="customerfileadd"),
path(r'capitalfileadd/', views.CapitalfileAddViewSet.as_view(), name="capitalfileadd"),
path(r'freightfileadd/', views.FreightfileAddViewSet.as_view(), name="freightfileadd"),
path(r'asnlistfileadd/', views.AsnlistfileAddViewSet.as_view(), name="asnlistfileadd"),
path(r'dnlistfileadd/', views.DnlistfileaddViewSet.as_view(), name="dnlistfileadd")
]
