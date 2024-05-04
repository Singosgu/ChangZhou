<template>
    <div>
      <transition appear enter-active-class="animated fadeIn">
      <q-table
        class="my-sticky-header-column-table shadow-24"
        :data="table_list"
        row-key="id"
        :separator="separator"
        :loading="loading"
        :filter="filter"
        :columns="columns"
        hide-bottom
        :pagination.sync="pagination"
        no-data-label="No data"
        no-results-label="No data you want"
        :table-style="{ height: height }"
        flat
        bordered
      >
         <template v-slot:top>
           <q-btn-group push>
             <q-btn :label="$t('refresh')" icon="refresh" @click="reFresh()">
               <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">
                 {{ $t('refreshtip') }}
               </q-tooltip>
             </q-btn>
             <q-btn label="生成拣货单" icon="confirmation_number" @click="orderreleaseAllData()">
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >全部生成拣货单
              </q-tooltip
              >
            </q-btn>
           </q-btn-group>
           <q-input
            v-model="filterData.txnid"
            filled
            autogrow
            label="TxnId"
          />
          <q-select v-model="filterData.order_type" outlined :options="order_type_list" label="发货方式" style="width: 150px"/>
          <q-select v-model="filterData.order_line" outlined :options="order_line_list" label="订单行" style="width: 150px"/>
          <q-select v-model="filterData.carrier" outlined :options="carrier_list" label="承运人" style="width: 150px"/>
          <q-input
            v-model="filterData.sku"
            filled
            autogrow
            label="SKU"
            style="width: 150px"
          />
          <q-btn label="筛选" @click="sortData()"></q-btn>
          <q-btn label="清空" @click="filterDataClear()"></q-btn>
         </template>
         <template v-slot:body="props">
           <q-tr :props="props">
               <q-td key="txnid" :props="props">
                 {{ props.row.txnid }}
               </q-td>
               <q-td key="order_type" :props="props">
                 {{ props.row.order_type }}
               </q-td>
               <q-td key="trackingnumber" :props="props">
                 {{ props.row.trackingnumber }}
               </q-td>
               <q-td key="carrier" :props="props">
                 {{ props.row.carrier }}
               </q-td>
               <q-td key="goods_code" :props="props">
                 {{ props.row.goods_code }}
               </q-td>
               <q-td key="goods_desc" :props="props">
                 {{ props.row.goods_desc }}
               </q-td>
               <q-td key="goods_qty" :props="props">
                 {{ props.row.goods_qty }}
               </q-td>
               <q-td key="goods_weight" :props="props">
                 {{ props.row.goods_weight }}
               </q-td>
             <q-td key="goods_volume" :props="props">
               {{ props.row.goods_volume }}
             </q-td>
             <q-td key="customer" :props="props">
               {{ props.row.customer }}
             </q-td>
             <q-td key="creater" :props="props">
               {{ props.row.creater }}
             </q-td>
             <q-td key="create_time" :props="props">
               {{ props.row.create_time }}
             </q-td>
             <q-td key="update_time" :props="props">
               {{ props.row.update_time }}
             </q-td>
             <q-td key="action" :props="props" style="width: 50px">
               <q-btn round flat push color="dark" icon="delete">
                 <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">
                   {{ $t('deletebackorder') }}
                </q-tooltip>
               </q-btn>
             </q-td>
           </q-tr>
         </template>
      </q-table>
        </transition>
      <template>
        <div class="q-pa-lg flex flex-center">
          <q-btn v-show="page_count===0" flat push color="dark" :label="$t('no_data')"></q-btn>
          <q-pagination
            v-show="page_count!==0"
            v-model="current"
            color="purple"
            :max="Math.ceil(page_count / 30 ) "
            :max-pages="30"
            boundary-numbers
            direction-links
            @click="getList()"
          />
        </div>
      </template>
    </div>
</template>
    <router-view />

<script>
import { getauth, postauth } from 'boot/axios_request'

export default {
  name: 'Pagednneworder',
  data () {
    return {
      current: 1,
      page_count: 0,
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'dn/detail/?dn_status=2',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      table_list: [],
      bin_size_list: [],
      bin_property_list: [],
      warehouse_list: [],
      columns: [
        { name: 'txnid', required: true, label: 'TxnId', align: 'left', field: 'txnid' },
        { name: 'order_type', required: true, label: 'Method', align: 'left', field: 'order_type' },
        { name: 'trackingnumber', required: true, label: '面单', align: 'left', field: 'trackingnumber' },
        { name: 'carrier', required: true, label: '承运人', align: 'left', field: 'carrier' },
        { name: 'goods_code', label: this.$t('goods.view_goodslist.goods_code'), field: 'goods_code', align: 'center' },
        { name: 'goods_desc', label: this.$t('goods.view_goodslist.goods_desc'), field: 'goods_desc', align: 'center' },
        { name: 'goods_qty', label: this.$t('outbound.view_dn.goods_qty'), field: 'goods_qty', align: 'center' },
        { name: 'goods_weight', label: this.$t('outbound.view_dn.total_weight'), field: 'goods_weight', align: 'center' },
        { name: 'goods_volume', label: this.$t('outbound.view_dn.total_volume'), field: 'empty_label', align: 'center' },
        { name: 'customer', label: this.$t('baseinfo.view_customer.customer_name'), field: 'customer', align: 'center' },
        { name: 'creater', label: this.$t('creater'), field: 'creater', align: 'center' },
        { name: 'create_time', label: this.$t('createtime'), field: 'create_time', align: 'center' },
        { name: 'update_time', label: this.$t('updatetime'), field: 'update_time', align: 'center' },
        { name: 'action', label: this.$t('action'), align: 'right' }
      ],
      filter: '',
      filterData: {
        txnid: '',
        order_type: '',
        order_line: '单件',
        carrier: '',
        sku: ''
      },
      pagination: {
        page: 1,
        rowsPerPage: '30'
      },
      order_type_list: [],
      order_line_list: ['单件', '多件'],
      carrier_list: [],
      txnid_list_data: [],
      order_type_data: '',
      order_line: '单件',
      carrier_data: '',
      sku_list_data: []
    }
  },
  methods: {
    filterDataClear () {
      this.filterData = {
        txnid: [],
        order_type: '',
        order_line: '单件',
        carrier: '',
        sku: []
      }
      this.txnid_list_data = []
      this.order_type_data = ''
      this.order_line = '单件'
      this.carrier_data = ''
      this.sku_list_data = []
      this.getList()
    },
    sortData () {
      var _this = this
      if (this.filterData.txnid.length > 0) {
        console.log(this.filterData.txnid)
        _this.txnid_list_data = this.filterData.txnid.split('\n')
      } else {
        _this.txnid_list_data = []
      }
      if (this.filterData.sku.length > 0) {
        _this.sku_list_data = this.filterData.sku.split('\n')
      } else {
        _this.sku_list_data = []
      }
      this.order_type_data = this.filterData.order_type
      if (this.filterData.order_line === '单件') {
        this.order_line = 1
      } else {
        this.order_line = 2
      }
      this.carrier_data = this.filterData.carrier
      _this.getList()
    },
    getList () {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        if (this.order_line === '单件') {
          this.order_line = 1
        } else {
          this.order_line = 2
        }
        getauth(_this.pathname + '&page=' + this.current + '&txnid__in=' + this.txnid_list_data + '&order_type=' + this.order_type_data + '&carrier=' + this.carrier_data + '&order_line=' + this.order_line + '&goods_code__in=' + this.sku_list_data, {
        }).then(res => {
          _this.page_count = res.count
          _this.table_list = res.results
          _this.pathname_previous = res.previous
          _this.pathname_next = res.next
          _this.warehouse_list = res.warehouse_list
          _this.order_type_list = res.order_type_list
          _this.carrier_list = res.carrier_list
        }).catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
      } else {
      }
    },
    getListPrevious () {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        getauth(_this.pathname_previous, {
        }).then(res => {
          _this.table_list = res.results
          _this.pathname_previous = res.previous
          _this.pathname_next = res.next
        }).catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
      } else {
      }
    },
    getListNext () {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        getauth(_this.pathname_next, {
        }).then(res => {
          _this.table_list = res.results
          _this.pathname_previous = res.previous
          _this.pathname_next = res.next
        }).catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
      } else {
      }
    },
    orderreleaseAllData () {
      var _this = this
      // this.$q.loading.show({ message: '确认中' })
      postauth(_this.pathname + 'orderrelease/', {})
        .then((res) => {
          _this.table_list = []
          _this.getList()
          _this.$q.notify({
            message: '全部生成拣货单成功',
            icon: 'check',
            color: 'green'
          })
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    reFresh () {
      var _this = this
      _this.getList()
    }
  },
  created () {
    var _this = this
    if (_this.$q.localStorage.has('openid')) {
      _this.openid = _this.$q.localStorage.getItem('openid')
    } else {
      _this.openid = ''
      _this.$q.localStorage.set('openid', '')
    }
    if (_this.$q.localStorage.has('login_name')) {
      _this.login_name = _this.$q.localStorage.getItem('login_name')
    } else {
      _this.login_name = ''
      _this.$q.localStorage.set('login_name', '')
    }
    if (_this.$q.localStorage.has('auth')) {
      _this.authin = '1'
      _this.filterDataClear()
    } else {
      _this.authin = '0'
    }
  },
  mounted () {
    var _this = this
    if (_this.$q.platform.is.electron) {
      _this.height = String(_this.$q.screen.height - 290) + 'px'
    } else {
      _this.height = _this.$q.screen.height - 290 + '' + 'px'
    }
  },
  updated () {
  },
  destroyed () {
  }
}
</script>
