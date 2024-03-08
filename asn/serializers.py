from django.db.models import Sum
from rest_framework import serializers
from .models import AsnListModel, AsnDetailModel
from utils import datasolve
from warehouse.models import ListModel as warehouse


class ASNListGetSerializer(serializers.ModelSerializer):
    asn_code = serializers.CharField(read_only=True, required=False)
    asn_status = serializers.IntegerField(read_only=True, required=False)
    supplier = serializers.CharField(read_only=True, required=False)
    patch_number = serializers.CharField(read_only=True, required=False)
    box_number = serializers.CharField(read_only=True, required=False)
    warehouse_id = serializers.SerializerMethodField()
    bar_code = serializers.CharField(read_only=True, required=False)
    creater = serializers.CharField(read_only=True, required=False)
    confirm_time = serializers.DateField(read_only=True, format='%Y/%m/%d')
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = AsnListModel
        exclude = ['openid', 'is_delete', ]
        read_only_fields = ['id', 'openid', ]

    def get_warehouse_id(self, obj):
        return warehouse.objects.filter(pk=obj.warehouse_id).first().warehouse_id

    def get_total_quantity(self, obj):
        # data = AsnDetailModel.objects.filter(asn_code=obj.asn_code).aggregate(
            # sum_total_quantity=Sum('goods_qty'))
        data = AsnDetailModel.objects.filter(asn_code=obj.asn_code).exclude(is_delete=1).aggregate(
            sum_total_quantity=Sum('goods_qty'))
        if data:
            return data.get('sum_total_quantity')
        return 0


class ASNListPostSerializer(serializers.ModelSerializer):
    openid = serializers.CharField(read_only=False, required=False, validators=[datasolve.openid_validate])
    asn_code = serializers.CharField(read_only=False, required=True, validators=[datasolve.asn_data_validate])
    supplier = serializers.CharField(read_only=False, required=False)
    patch_number = serializers.CharField(read_only=False, required=False)
    box_number = serializers.CharField(read_only=False, required=False)
    warehouse_id = serializers.IntegerField(read_only=False, required=False, validators=[datasolve.warehouse_validate])
    bar_code = serializers.CharField(read_only=False, required=True)
    creater = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])

    class Meta:
        model = AsnListModel
        exclude = ['is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]


class ASNListPartialUpdateSerializer(serializers.ModelSerializer):
    asn_code = serializers.CharField(read_only=False, required=True, validators=[datasolve.asn_data_validate])

    class Meta:
        model = AsnListModel
        exclude = ['is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]


class ASNListUpdateSerializer(serializers.ModelSerializer):
    asn_code = serializers.CharField(read_only=False, required=True, validators=[datasolve.asn_data_validate])

    class Meta:
        model = AsnListModel
        exclude = ['is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]


class ASNDetailGetSerializer(serializers.ModelSerializer):
    asn_code = serializers.CharField(read_only=True, required=False)
    supplier = serializers.CharField(read_only=True, required=False)
    goods_code = serializers.CharField(read_only=True, required=False)
    goods_desc = serializers.CharField(read_only=True, required=False)
    goods_qty = serializers.IntegerField(read_only=True, required=False)
    goods_actual_qty = serializers.IntegerField(read_only=True, required=False)
    sorted_qty = serializers.IntegerField(read_only=True, required=False)
    goods_shortage_qty = serializers.IntegerField(read_only=True, required=False)
    goods_more_qty = serializers.IntegerField(read_only=True, required=False)
    goods_damage_qty = serializers.IntegerField(read_only=True, required=False)
    patch_number = serializers.CharField(read_only=True, required=False)
    warehouse_id = serializers.SerializerMethodField()
    box_number = serializers.CharField(read_only=True, required=False)
    creater = serializers.CharField(read_only=True, required=False)
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = AsnDetailModel
        exclude = ['openid', 'is_delete', ]
        read_only_fields = ['id', 'openid']

    def get_warehouse_id(self, obj):
        return warehouse.objects.filter(pk=obj.warehouse_id).first().warehouse_id


class ASNDetailPostSerializer(serializers.ModelSerializer):
    openid = serializers.CharField(read_only=False, required=False, validators=[datasolve.openid_validate])
    asn_code = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    supplier = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    goods_code = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    goods_desc = serializers.CharField(read_only=False, required=False)
    goods_qty = serializers.IntegerField(read_only=False, required=True, validators=[datasolve.qty_0_data_validate])
    patch_number = serializers.CharField(read_only=False, required=False)
    box_number = serializers.CharField(read_only=False, required=False)
    warehouse_id = serializers.IntegerField(read_only=False, required=True, validators=[datasolve.warehouse_validate])
    creater = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])

    class Meta:
        model = AsnDetailModel
        exclude = ['is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]


class ASNSortedPostSerializer(serializers.ModelSerializer):
    openid = serializers.CharField(read_only=False, required=False, validators=[datasolve.openid_validate])
    asn_code = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    supplier = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    goods_code = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    goods_desc = serializers.CharField(read_only=False, required=False)
    goods_qty = serializers.IntegerField(read_only=False, required=True, validators=[datasolve.qty_data_validate])
    creater = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])

    class Meta:
        model = AsnDetailModel
        exclude = ['is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]


class ASNDetailUpdateSerializer(serializers.ModelSerializer):
    asn_code = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    supplier = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    goods_code = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    goods_desc = serializers.CharField(read_only=False, required=False)
    goods_qty = serializers.IntegerField(read_only=False, required=True, validators=[datasolve.qty_0_data_validate])
    patch_number = serializers.CharField(read_only=False, required=False)
    box_number = serializers.CharField(read_only=False, required=False)
    warehouse_id = serializers.IntegerField(read_only=False, required=True, validators=[datasolve.warehouse_validate])
    creater = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])

    class Meta:
        model = AsnDetailModel
        exclude = ['openid', 'is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]


class ASNDetailPartialUpdateSerializer(serializers.ModelSerializer):
    asn_code = serializers.CharField(read_only=False, required=False, validators=[datasolve.data_validate])
    supplier = serializers.CharField(read_only=False, required=False, validators=[datasolve.data_validate])
    goods_code = serializers.CharField(read_only=False, required=False, validators=[datasolve.data_validate])
    goods_desc = serializers.CharField(read_only=False, required=False)
    goods_qty = serializers.IntegerField(read_only=False, required=False, validators=[datasolve.qty_0_data_validate])
    patch_number = serializers.CharField(read_only=False, required=False)
    box_number = serializers.CharField(read_only=False, required=False)
    warehouse_id = serializers.IntegerField(read_only=False, required=True, validators=[datasolve.warehouse_validate])
    creater = serializers.CharField(read_only=False, required=False, validators=[datasolve.data_validate])

    class Meta:
        model = AsnDetailModel
        exclude = ['openid', 'is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]


class MoveToBinSerializer(serializers.ModelSerializer):
    bin_name = serializers.CharField(read_only=False, required=True, validators=[datasolve.data_validate])
    qty = serializers.IntegerField(read_only=False, required=True, validators=[datasolve.qty_0_data_validate])

    class Meta:
        model = AsnDetailModel
        ref_name = 'AsnMoveToBin'
        exclude = ['openid', 'is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]


class FileListRenderSerializer(serializers.ModelSerializer):
    asn_code = serializers.CharField(read_only=False, required=False)
    asn_status = serializers.IntegerField(read_only=False, required=False)
    total_weight = serializers.FloatField(read_only=False, required=False)
    total_volume = serializers.FloatField(read_only=False, required=False)
    total_cost = serializers.FloatField(read_only=False, required=False)
    supplier = serializers.CharField(read_only=False, required=False)
    patch_number = serializers.CharField(read_only=False, required=False)
    box_number = serializers.CharField(read_only=False, required=False)
    warehouse_id = serializers.IntegerField(read_only=False, required=False)
    creater = serializers.CharField(read_only=False, required=False)
    transportation_fee = serializers.JSONField(read_only=False, required=False)
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = AsnListModel
        ref_name = 'ASNFileListRenderSerializer'
        exclude = ['openid', 'is_delete', ]


class FileDetailRenderSerializer(serializers.ModelSerializer):
    asn_code = serializers.CharField(read_only=False, required=False)
    asn_status = serializers.IntegerField(read_only=False, required=False)
    goods_code = serializers.CharField(read_only=False, required=False)
    goods_desc = serializers.CharField(read_only=False, required=False)
    goods_qty = serializers.IntegerField(read_only=False, required=False)
    goods_actual_qty = serializers.IntegerField(read_only=False, required=False)
    sorted_qty = serializers.IntegerField(read_only=False, required=False)
    goods_shortage_qty = serializers.IntegerField(read_only=False, required=False)
    goods_more_qty = serializers.IntegerField(read_only=False, required=False)
    goods_damage_qty = serializers.IntegerField(read_only=False, required=False)
    goods_weight = serializers.FloatField(read_only=False, required=False)
    goods_volume = serializers.FloatField(read_only=False, required=False)
    goods_cost = serializers.FloatField(read_only=False, required=False)
    supplier = serializers.CharField(read_only=False, required=False)
    patch_number = serializers.CharField(read_only=False, required=False)
    warehouse_id = serializers.IntegerField(read_only=False, required=False)
    creater = serializers.CharField(read_only=False, required=False)
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = AsnDetailModel
        ref_name = 'ASNFileDetailRenderSerializer'
        exclude = ['openid', 'is_delete', ]
