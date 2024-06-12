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
           </q-btn-group>
         </template>
         <template v-slot:body="props">
           <q-tr :props="props">
               <q-td key="txnid" :props="props">
                 {{ props.row.txnid }}
               </q-td>
               <q-td key="trackingnumber" :props="props">
                 {{ props.row.trackingnumber }}
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
    </div>

</template>
    <router-view />

<script>
import { baseurl, getauth, postauth } from 'boot/axios_request'
import axios from 'axios'

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
        { name: 'trackingnumber', label: '面单号', field: 'trackingnumber', align: 'center' },
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
      scan_detail: [],
      sendData: {},
      picking_status_list: [1,2]
    }
  },
  methods: {
    getList (e) {
      var _this = this
      if (_this.$q.localStorage.has('auth')) {
        getauth(_this.pathname + '?page=' + this.current + '&order_line=2&dn_code=' + '' + e + '&max_page=10000&picking_status=1', {
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
    getScanData (e) {
      axios.get(baseurl + 'scanner/list/' + e + '/',
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
          } else if (this.resMode === 'PSUM') {
            this.PickChange()
          } else if (this.resMode === 'MD') {
            this.MDConfirm(this.resData)
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
          if (item.txnid === this.resData && item.picking_status === 1) {
            item.picking_status = 2
            this.table_list.unshift(item)
            this.table_list.splice(index + 1, 1)
            this.sendData = item
            throw new Error('success')
          }
        })
      } catch (e) {
        console.log(e)
      } finally {
        console.log('error')
      }
    },
    submitSendData (e) {
      this.scan_detail = []
      this.scan_detail.push(e)
      this.submitRes(e)
    },
    submitRes (e) {
      const submitData = {
        creater: this.login_name,
        customer: e.customer,
        dn_code: e.dn_code,
        goodsData: this.scan_detail
      }
      postauth('dn/morepicked/' + e.id + '/', submitData, {
      })
        .then((res) => {
          if (!res.detail) {
            this.scan_detail = []
            postauth('http://127.0.0.1:8008/print/' + this.$q.localStorage.getItem('printer') + '/' + e.txnid + '/', { data: e.mian_dan }).then((res) => {
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
    MDConfirm (e) {
      getauth('dn/list/?trackingnumber=' + e).then((res) => {
        if (res.results.length > 0) {
          if (res.results[0].dn_status === 4) {
            postauth('dn/dispatch/' + res.results[0].id + '/', res.results[0]).then((res) => {
              this.table_list.splice(0, 1)
              this.$q.notify({
                message: '发货成功',
                icon: 'check',
                color: 'green'
              })
            })
          } else {
            this.$q.notify({
              message: '订单已完成，或者还未到发货环节',
              icon: 'close',
              color: 'negative'
            })
          }
        } else {
          this.$q.notify({
            message: '面单不存在',
            icon: 'close',
            color: 'negative'
          })
        }
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
  watch: {
    sendData (sendData) {
      var _this = this
      _this.submitSendData(sendData)
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
