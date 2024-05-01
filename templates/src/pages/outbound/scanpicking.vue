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
      >
         <template v-slot:top>
           <q-btn-group push>
             <q-btn :label="$t('refresh')" icon="refresh" @click="reFresh()">
               <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">
                 {{ $t('refreshtip') }}
               </q-tooltip>
             </q-btn>
<!--             <q-btn color="secondary" glossy :label="$t('outbound.confirm')" @click="confirmData()" />-->
           </q-btn-group>
           <q-space />
<!--           <q-input outlined rounded dense debounce="50000" color="primary" v-model="filter" :placeholder="$t('search')" @blur="getSearchList()" @keyup.enter="getSearchList()">-->
<!--             <template v-slot:append>-->
<!--               <q-icon name="search" @click="getSearchList()"/>-->
<!--             </template>-->
<!--           </q-input>-->
         </template>
         <template v-slot:body="props">
           <q-tr :props="props">
               <q-td key="txnid" :props="props">
                 {{ props.row.txnid }}
               </q-td>
               <q-td key="bin_name" :props="props">
                 {{ props.row.bin_name }}
               </q-td>
               <q-td key="goods_code" :props="props">
                 {{ props.row.goods_code }}
               </q-td>
               <q-td key="pick_qty" :props="props">
                 {{ props.row.pick_qty }}
               </q-td>
             <q-td key="picked_qty" :props="props">
               {{ props.row.picked_qty }}
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
        <div class="q-pa-lg flex flex-center">
          <q-pagination
            v-show="page_count!==0"
            v-model="current"
            color="purple"
            :max="Math.ceil(page_count / 5000 ) "
            :max-pages="5000"
            boundary-numbers
            direction-links
            @click="getList()"
          />
          <q-btn v-show="page_count===0" flat push color="dark" :label="$t('no_data')"></q-btn>
        </div>
      </template>
      <q-dialog v-model="submitForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>确认发货</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section
          style="max-height: 325px; width: 400px"
          class="scroll"
        >该操作不可逆
        </q-card-section
        >
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="InitData()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="submitData()">{{
              $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    </div>

</template>
    <router-view />

<script>
import { getauth, putauth } from 'boot/axios_request'
import axios from 'axios'
import {LocalStorage} from "quasar";

export default {
  name: 'Pagednprepick',
  data () {
    return {
      current: 1,
      page_count: 0,
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'dn/pickinglistfilter/',
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
        { name: 'bin_name', label: this.$t('warehouse.view_binset.bin_name'), field: 'bin_name', align: 'center' },
        { name: 'goods_code', label: this.$t('goods.view_goodslist.goods_code'), field: 'goods_code', align: 'center' },
        { name: 'pick_qty', label: this.$t('stock.view_stocklist.pick_stock'), field: 'pick_qty', align: 'center' },
        { name: 'picked_qty', label: this.$t('stock.view_stocklist.picked_stock'), field: 'picked_qty', align: 'center' },
        { name: 'creater', label: this.$t('creater'), field: 'creater', align: 'center' },
        { name: 'create_time', label: this.$t('createtime'), field: 'create_time', align: 'center' },
        { name: 'update_time', label: this.$t('updatetime'), field: 'update_time', align: 'center' }
      ],
      filter: '',
      pagination: {
        page: 1,
        rowsPerPage: '5000'
      },
      scanData: [],
      resData: '',
      resMode: '',
      submitForm: false,
      scan_detail: []
    }
  },
  methods: {
    getList (e) {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        getauth(_this.pathname + '?order_line=1&page=' + this.current + '&dn_code=' + '' + e + '&max_page=5000&picking_status=0', {
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
    getSearchList () {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        getauth(_this.pathname + '?dn_code__icontains=' + _this.filter + '&page=' + this.current, {
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
        getauth(_this.pathname_next, {}).then(res => {
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
      }
    },
    confirmData () {
      this.submitForm = true
    },
    getScanData (e) {
      axios.get('scanner/list/' + e + '/',
        {
          headers: {
            'Content-Type': 'application/json, charset="utf-8"',
            token: 'SCANGOODS',
            language: this.$q.localStorage.getItem('lang'),
            operator: this.$q.localStorage.getItem('login_id')
          }
        }).then(res => {
        if (!res.data.detail) {
          this.resData = res.data.code
          this.resMode = res.data.mode
          if (this.resMode === 'DN') {
            this.getList(this.resData)
          } else if (this.resMode === 'GOODS') {
            this.PickChange()
          } else {
            this.$q.notify({
              message: e + '编码不存在',
              icon: 'close',
              color: 'negative'
            })
          }
        }
      }).catch(err => {
        this.$q.notify({
          type: 'negative',
          message: err.detail
        })
      })
    },
    PickChange () {
      try {
        this.table_list.forEach((item, index) => {
          if (item.goods_code === this.resData) {
            if (item.pick_qty > 0) {
              item.picked_qty += 1
              item.pick_qty -= 1
              this.scan_detail.splice(index + 1, 1)
              this.table_list.unshift(item)
              this.table_list.splice(index + 1, 1)
              this.submitRes(item)
              throw new Error('success')
            } else {
              if (index + 1 === this.table_list.length) {
                this.$q.notify({
                  type: 'negative',
                  icon: 'close',
                  message: 'Can Not Pick More'
                })
              }
            }
          }
        })
      } catch (e) {
        console.log(e)
      } finally {
        console.log('error')
      }
    },
    submitData () {
      var dn_code = this.table_list[0].dn_code
      getauth('dn/list/?dn_code=' + dn_code, {}).then((res) => {
        if (!res.detail) {
          this.submitRes(res.results[0])
        } else {
          this.$q.notify({
            type: 'negative',
            icon: 'close',
            message: this.$t('notice.mobile_scan.notice1')
          })
        }
      })
        .catch((err) => {
          this.$q.notify({
            type: 'negative',
            icon: 'close',
            message: this.$t('notice.mobile_scan.notice3')
          })
        })
    },
    submitRes (e) {
      console.log(e)
      const resData = {
        creater: this.login_name,
        customer: e.customer,
        dn_code: e.dn_code,
        goodsData: this.scan_detail
      }
      putauth('dn/picked/' + e.id + '/', resData, {
      })
        .then((res) => {
          if (!res.detail) {
            this.scan_detail = []
            getauth('http://127.0.0.1:8008/print/' + this.$q.localStorage.getItem('printer') + '/' + e.txnid + '/', { data: e.miandan }).then((res) => {
              this.$q.notify({
                message: '面单打印成功'
              })
            })
            this.$q.notify({
              message: this.$t('拣货成功')
            })
          }
          this.InitData('')
        })
        .catch((err) => {
          this.$q.notify({
            message: this.$t('notice.network_error')
          })
        })
    },
    reFresh () {
      var _this = this
      _this.getList('')
    },
    KeyDown (e) {
      if (e.key === 'Enter' || e.keyCode === 13) {
        this.getScanData(this.scanData.join(''))
        this.scanData = []
      } else if (e.key === 'Shift' || e.keyCode === 16) {
      } else if (e.key === 'Tab' || e.keyCode === 9) {
      } else {
        this.scanData.push(e.key)
      }
    },
    InitData () {
      this.submitForm = false
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
      _this.getList('')
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
    window.addEventListener('keydown', this.KeyDown, true)
  },
  updated () {
  },
  destroyed () {
  }
}
</script>
