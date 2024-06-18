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
            <q-btn label="批量确认订单" icon="recommend" @click="confirmOrders()">
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >批量确认订单
              </q-tooltip
              >
            </q-btn>
           </q-btn-group>
           <q-space />
           <div class="row no-wrap">
            <q-input
              outlined
              v-model="filterData.txnid"
              label="TxnId"
              style="padding-right:20px;width:200px"
              class="q-field--dense q-field__native"
            />
            <q-select
              outlined
              v-model="filterData.order_type"
              :options="order_type_list"
              style="padding-right:20px;width:400px;"
              label="发货方式"
              class="q-field__native q-field--dense"
            />
             <q-select
              outlined
              v-model="filterData.order_line"
              :options="order_line_list"
              style="padding-right:20px;width:200px"
              label="订单行"
              class="q-field__native q-field--dense"
            />
             <q-select
              outlined
              v-model="filterData.carrier"
              :options="carrier_list"
              style="padding-right:20px;width:200px"
              label="承运人"
              class="q-field__native q-field--dense"
            />
             <q-input
              outlined
              v-model="filterData.sku"
              label="SKU"
              style="padding-right:20px;width:200px"
              class="q-field--dense q-field__native"
            />
          </div>
           <div>
            <q-btn
              style="height: 40px;margin-right:10px;"
              unelevated
              color="primary"
              label="查询"
              @click="sortData()"
            />
            <q-btn
              style="height: 40px;margin-right:10px;"
              unelevated
              color="red"
              label="重置"
              @click="filterDataClear()"
            />
          </div>
<!--           <q-input-->
<!--            v-model="filterData.txnid"-->
<!--            filled-->
<!--            autogrow-->
<!--            label="TxnId"-->
<!--          />-->
<!--          <q-select v-model="filterData.order_type" outlined :options="order_type_list" label="发货方式" style="width: 150px"/>-->
<!--          <q-select v-model="filterData.order_line" outlined :options="order_line_list" label="订单行" style="width: 150px"/>-->
<!--          <q-select v-model="filterData.carrier" outlined :options="carrier_list" label="承运人" style="width: 150px"/>-->
<!--          <q-input-->
<!--            v-model="filterData.sku"-->
<!--            filled-->
<!--            autogrow-->
<!--            label="SKU"-->
<!--            style="width: 150px"-->
<!--          />-->
<!--          <q-btn label="筛选" @click="sortData()"></q-btn>-->
<!--          <q-btn label="清空" @click="filterDataClear()"></q-btn>-->
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
           </q-tr>
         </template>
      </q-table>
        </transition>
      <template>
<!--        <div class="q-pa-lg flex flex-center">-->
<!--          <q-btn v-show="page_count===0" flat push color="dark" :label="$t('no_data')"></q-btn>-->
<!--          <q-pagination-->
<!--            v-show="page_count!==0"-->
<!--            v-model="current"-->
<!--            color="purple"-->
<!--            :max="Math.ceil(page_count / 30 ) "-->
<!--            :max-pages="30"-->
<!--            boundary-numbers-->
<!--            direction-links-->
<!--            @click="getList()"-->
<!--          />-->
<!--        </div>-->
        <div class="q-pa-lg flex flex-center">
        <q-select outlined v-model="max_page_data" :options="max_page" label="每页数量" class="q-field__native q-field--dense" style="width: 100px" />
        <q-btn
          v-show="page_count===0"
          flat
          push
          color="dark"
          :label="$t('no_data')"
        ></q-btn>
        <q-pagination
          v-show="page_count!==0"
          v-model="current"
          color="black"
          :max="Math.ceil(page_count / max_page_data ) "
          :max-pages="5"
          boundary-numbers
          direction-links
          @click="getList()"
        />
        <div style="margin-left:20px"> Total:  {{ page_count }} </div>
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
      pathname: 'dn/detail/?dn_status=1',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      max_page_data: 30,
      max_page: [30, 100, 500, 1000],
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
        { name: 'update_time', label: this.$t('updatetime'), field: 'update_time', align: 'center' }
      ],
      filter: '',
      filterData: {
        txnid: '',
        order_type: '',
        order_line: '',
        carrier: '',
        sku: ''
      },
      pagination: {
        page: 1,
        rowsPerPage: '1000'
      },
      order_type_list: [],
      order_line_list: ['单件', '多件'],
      carrier_list: [],
      txnid_list_data: [],
      order_type_data: '',
      order_line: '',
      carrier_data: '',
      sku_list_data: []
    }
  },
  methods: {
    filterDataClear () {
      this.filterData = {
        txnid: [],
        order_type: '',
        order_line: '',
        carrier: '',
        sku: []
      }
      this.txnid_list_data = []
      this.order_type_data = ''
      this.order_line = ''
      this.carrier_data = ''
      this.sku_list_data = []
      this.getList()
    },
    sortData () {
      var _this = this
      if (this.filterData.txnid.length > 0) {
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
          if (this.order_line === 1) {
            this.order_line = 1
          } else if (this.order_line === 2) {
            this.order_line = 2
          } else {
            this.order_line = ''
          }
        }
        getauth(_this.pathname + '&max_page=' + _this.max_page_data + '&page=' + this.current + '&txnid__in=' + this.txnid_list_data + '&order_type=' + this.order_type_data + '&carrier=' + this.carrier_data + '&order_line=' + this.order_line + '&goods_code__in=' + this.sku_list_data, {
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
    confirmOrders () {
      var _this = this
      if (this.order_line === '单件') {
        this.order_line = 1
      } else {
        if (this.order_line === 1) {
          this.order_line = 1
        } else {
          this.order_line = 2
        }
      }
      postauth('dn/confirmorders/?dn_status=1' + '&page=' + this.current + '&txnid__in=' + this.txnid_list_data + '&order_type=' + this.order_type_data + '&carrier=' + this.carrier_data + '&order_line=' + this.order_line + '&goods_code__in=' + this.sku_list_data, {})
        .then((res) => {
          this.$q.notify({
            message: '确认订单完成',
            color: 'green',
            icon: 'check'
          })
          this.getList()
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
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
  watch: {
    max_page_data (max_page_data) {
      var _this = this
      _this.getList()
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
