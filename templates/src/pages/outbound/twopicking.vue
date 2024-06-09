<template>
    <div>
      <transition appear enter-active-class="animated fadeIn">
      <q-table
        class="my-sticky-header-table shadow-24"
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
        :selected-rows-label="getSelectedString"
        selection="multiple"
        :selected.sync="selected"
      >
         <template v-slot:top>
           <q-btn-group push>
             <q-btn :label="$t('refresh')" icon="refresh" @click="reFresh()">
               <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">
                 {{ $t('refreshtip') }}
               </q-tooltip>
             </q-btn>
             <q-btn round flat push icon="how_to_vote" @click="openStaff()">
                 <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">
                   把拣货单分配给拣货员
                 </q-tooltip>
              </q-btn>
           </q-btn-group>
           <q-space />
           <q-input outlined rounded dense debounce="300" color="primary" v-model="filter" :placeholder="$t('search')" @blur="getSearchList()" @keyup.enter="getSearchList()">
             <template v-slot:append>
               <q-icon name="search" @click="getSearchList()"/>
             </template>
           </q-input>
         </template>
         <template v-slot:body="props">
           <q-tr :props="props">
               <q-td key="txnid" :props="props">
                 {{ props.row.txnid }}
               </q-td>
<!--               <q-td key="bin_name" :props="props">-->
<!--                 {{ props.row.bin_name }}-->
<!--               </q-td>-->
<!--               <q-td key="goods_code" :props="props">-->
<!--                 {{ props.row.goods_code }}-->
<!--               </q-td>-->
<!--               <q-td key="pick_qty" :props="props">-->
<!--                 {{ props.row.pick_qty }}-->
<!--               </q-td>-->
<!--             <q-td key="picked_qty" :props="props">-->
<!--               {{ props.row.picked_qty }}-->
<!--             </q-td>-->
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
               <q-btn round flat push icon="how_to_vote" @click="allocateStaff(props.row)">
                 <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">
                   把拣货单分配给拣货员
                 </q-tooltip>
              </q-btn>
             </q-td>
           </q-tr>
         </template>
      </q-table>
        </transition>
      <template>
        <div class="q-pa-lg flex flex-center">
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
          <q-btn v-show="page_count===0" flat push color="dark" :label="$t('no_data')"></q-btn>
        </div>
      </template>
      <q-dialog v-model="allocte_form">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>分配拣货单</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-select
            filled
            use-input
            fill-input
            hide-selected
            input-debounce="0"
            dense
            outlined
            square
            v-model="filter_data.staff_name"
            :options="staff_list"
            label="拣货员"
            style="margin-bottom: 5px"
            :rules="[(val) => (val && val.length > 0) || '请选择拣货员']"
            @keyup.enter="allocateSubmit()"
          >
          </q-select>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="cancelSubmit()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn
            color="primary"
            @click="allocateSubmit()"
          >{{ $t("submit") }}
          </q-btn
          >
        </div>
      </q-card>
    </q-dialog>
    </div>
</template>
    <router-view />

<script>
import { getauth, postauth, baseurl } from 'boot/axios_request'

export default {
  name: 'Pagednmorepick',
  data () {
    return {
      current: 1,
      page_count: 0,
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'dn/pickingsumfilter/',
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
        // { name: 'bin_name', label: this.$t('warehouse.view_binset.bin_name'), field: 'bin_name', align: 'center' },
        // { name: 'goods_code', label: this.$t('goods.view_goodslist.goods_code'), field: 'goods_code', align: 'center' },
        // { name: 'pick_qty', label: this.$t('stock.view_stocklist.pick_stock'), field: 'pick_qty', align: 'center' },
        // { name: 'picked_qty', label: this.$t('stock.view_stocklist.picked_stock'), field: 'picked_qty', align: 'center' },
        { name: 'creater', label: this.$t('creater'), field: 'creater', align: 'center' },
        { name: 'create_time', label: this.$t('createtime'), field: 'create_time', align: 'center' },
        { name: 'update_time', label: this.$t('updatetime'), field: 'update_time', align: 'center' },
        { name: 'action', label: this.$t('action'), align: 'right' }
      ],
      filter: '',
      pagination: {
        page: 1,
        rowsPerPage: '30'
      },
      bin_list: [],
      staff_list: [],
      allocte_form: false,
      filter_data: {
        txnid: '',
        staff_name: '',
        dn_code: '',
        bar_code: '',
        picking_list: []
      },
      selected: []
    }
  },
  methods: {
    getList () {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        getauth('dn/pickinglistfilter/?txnid=TEST-2024053113', {}).then((res) => {
          console.log(res)
        })
        getauth(_this.pathname + '?page=' + this.current + '&picking_status=0&order_line=2', {
        }).then(res => {
          _this.page_count = res.count
          _this.table_list = res.results
          _this.pathname_previous = res.previous
          _this.pathname_next = res.next
          _this.bin_list = res.bin_list
          _this.staff_list = res.staff_list
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
    getSearchList () {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        getauth(_this.pathname + '?txnid__icontains=' + _this.filter + '&page=' + this.current, {
        }).then(res => {
          _this.page_count = res.count
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
    },
    openStaff () {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        _this.allocte_form = true
      } else {
        _this.$q.notify({
          message: _this.$t('no_auth'),
          icon: 'close',
          color: 'negative'
        })
      }
    },
    allocateStaff (e) {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        _this.filter_data.txnid = e.txnid
        _this.filter_data.dn_code = e.dn_code
        _this.filter_data.bar_code = e.bar_code
        _this.resSubmit()
      } else {
        _this.$q.notify({
          message: _this.$t('no_auth'),
          icon: 'close',
          color: 'negative'
        })
      }
    },
    allocateSubmit () {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        if (_this.filter_data.staff_name === '') {
          _this.$q.notify({
            message: '请选择拣货员',
            icon: 'close',
            color: 'negative'
          })
        } else {
          if (this.selected.length >= 1) {
            _this.selected.forEach((item, index) => {
              _this.allocateStaff(item)
            })
          }
        }
      }
    },
    cancelSubmit () {
      var _this = this
      _this.allocte_form = false
      _this.filter_data.txnid = ''
      _this.filter_data.dn_code = ''
      _this.filter_data.bar_code = ''
      _this.filter_data.picking_list = []
    },
    resSubmit () {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        postauth(baseurl + 'dn/morepicking/?page=' + this.current + '&picking_status=0&order_line=2&txnid=' + _this.filter_data.txnid, _this.filter_data).then(res => {
          getauth('dn/pickinglistfilter/?txnid=' + _this.filter_data.txnid).then((res) => {
            _this.filter_data.picking_list = res.results
            postauth('http://127.0.0.1:8008/print_picking/' + this.$q.localStorage.getItem('printer') + '/' + _this.filter_data.txnid + '/', _this.filter_data).then((result) => {
              _this.cancelSubmit()
              _this.getList()
              _this.$q.notify({
                message: '分配成功',
                icon: 'check',
                color: 'green'
              })
              this.$q.notify({
                message: '拣货单打印成功'
              })
            })
          })
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
    getSelectedString () {
      return this.selected.length === 0 ? '' : `${this.selected.length} record${this.selected.length > 1 ? 's' : ''} selected of ${this.data.length}`
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
      _this.getList()
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
