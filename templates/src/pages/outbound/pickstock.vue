<template>
  <div>
    <transition appear enter-active-class="animated fadeIn">
      <q-table
        id="table"
        class="my-sticky-header-column-table shadow-24"
        :data="table_list"
        row-key="id"
        :separator="separator"
        :loading="loading"
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
              <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('refreshtip') }}</q-tooltip>
            </q-btn>
          </q-btn-group>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
              <q-td key="staff_name" :props="props">{{ props.row.staff_name }}</q-td>
            <q-td key="create_time" :props="props">{{ props.row.create_time }}</q-td>
            <q-td key="update_time" :props="props">{{ props.row.update_time }}</q-td>
            <template>
              <q-td key="action" :props="props" style="width: 50px">
                <q-btn
                  round
                  flat
                  push
                  color="black"
                  icon="download"
                  @click="downloadPickingList(props.row)"
                >
                  <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">
                    下载这个仓管员的拣货单
                  </q-tooltip>
                </q-btn>
              </q-td>
            </template>
          </q-tr>
        </template>
      </q-table>
    </transition>
    <template>
      <div class="q-pa-lg flex flex-center">
        <q-btn v-show="pathname_previous" flat push color="purple" :label="$t('previous')" icon="navigate_before" @click="getListPrevious()">
          <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('previous') }}</q-tooltip>
        </q-btn>
        <q-btn v-show="pathname_next" flat push color="purple" :label="$t('next')" icon-right="navigate_next" @click="getListNext()">
          <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('next') }}</q-tooltip>
        </q-btn>
        <q-btn v-show="!pathname_previous && !pathname_next" flat push color="dark" :label="$t('no_data')"></q-btn>
      </div>
    </template>
  </div>
</template>
<router-view />

<script>
import { getauth, baseurl } from 'boot/axios_request'
import { LocalStorage } from 'quasar'

export default {
  name: 'Pagestafflist',
  data () {
    return {
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'staff/?picking_task=1',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      table_list: [],
      staff_type_list: [],
      columns: [
        { name: 'staff_name', required: true, label: this.$t('staff.view_staff.staff_name'), align: 'left', field: 'staff_name' },
        { name: 'create_time', label: this.$t('createtime'), field: 'create_time', align: 'center' },
        { name: 'update_time', label: this.$t('updatetime'), field: 'update_time', align: 'center' },
        { name: 'action', label: this.$t('action'), align: 'right' }
      ],
      pagination: {
        page: 1,
        rowsPerPage: '30'
      }
    }
  },
  methods: {
    getList () {
      var _this = this
      getauth(_this.pathname, {})
        .then(res => {
          _this.table_list = res.results
          if (LocalStorage.getItem('lang') === 'zh-hans') {
            _this.table_list.forEach((item, index) => {
              if (item.staff_type === 'Admin') {
                item.staff_type = '管理员'
              } else if (item.staff_type === 'Customer') {
                item.staff_type = '客户'
              } else if (item.staff_type === 'Supplier') {
                item.staff_type = '供应商'
              } else if (item.staff_type === 'Manager') {
                item.staff_type = '经理'
              } else if (item.staff_type === 'Supervisor') {
                item.staff_type = '主管'
              } else if (item.staff_type === 'Inbound') {
                item.staff_type = '收货组'
              } else if (item.staff_type === 'Outbound') {
                item.staff_type = '发货组'
              } else if (item.staff_type === 'StockControl') {
                item.staff_type = '库存管理'
              }
            })
          }
          _this.pathname_previous = res.previous
          _this.pathname_next = res.next
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    getSearchList () {
      var _this = this
      _this.filter = _this.filter.replace(/\s+/g, '')
      getauth(_this.pathname + '?staff_name__icontains=' + _this.filter, {})
        .then(res => {
          _this.table_list = res.results
          if (LocalStorage.getItem('lang') === 'zh-hans') {
            _this.table_list.forEach((item, index) => {
              if (item.staff_type === 'Admin') {
                item.staff_type = '管理员'
              } else if (item.staff_type === 'Customer') {
                item.staff_type = '客户'
              } else if (item.staff_type === 'Supplier') {
                item.staff_type = '供应商'
              } else if (item.staff_type === 'Manager') {
                item.staff_type = '经理'
              } else if (item.staff_type === 'Supervisor') {
                item.staff_type = '主管'
              } else if (item.staff_type === 'Inbound') {
                item.staff_type = '收货组'
              } else if (item.staff_type === 'Outbound') {
                item.staff_type = '发货组'
              } else if (item.staff_type === 'StockControl') {
                item.staff_type = '库存管理'
              }
            })
          }
          _this.pathname_previous = res.previous
          _this.pathname_next = res.next
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    getListPrevious () {
      var _this = this
      getauth(_this.pathname_previous, {})
        .then(res => {
          _this.table_list = res.results
          if (LocalStorage.getItem('lang') === 'zh-hans') {
            _this.table_list.forEach((item, index) => {
              if (item.staff_type === 'Admin') {
                item.staff_type = '管理员'
              } else if (item.staff_type === 'Customer') {
                item.staff_type = '客户'
              } else if (item.staff_type === 'Supplier') {
                item.staff_type = '供应商'
              } else if (item.staff_type === 'Manager') {
                item.staff_type = '经理'
              } else if (item.staff_type === 'Supervisor') {
                item.staff_type = '主管'
              } else if (item.staff_type === 'Inbound') {
                item.staff_type = '收货组'
              } else if (item.staff_type === 'Outbound') {
                item.staff_type = '发货组'
              } else if (item.staff_type === 'StockControl') {
                item.staff_type = '库存管理'
              }
            })
          }
          _this.pathname_previous = res.previous
          _this.pathname_next = res.next
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    getListNext () {
      var _this = this
      getauth(_this.pathname_next, {})
        .then(res => {
          _this.table_list = res.results
          if (LocalStorage.getItem('lang') === 'zh-hans') {
            _this.table_list.forEach((item, index) => {
              if (item.staff_type === 'Admin') {
                item.staff_type = '管理员'
              } else if (item.staff_type === 'Customer') {
                item.staff_type = '客户'
              } else if (item.staff_type === 'Supplier') {
                item.staff_type = '供应商'
              } else if (item.staff_type === 'Manager') {
                item.staff_type = '经理'
              } else if (item.staff_type === 'Supervisor') {
                item.staff_type = '主管'
              } else if (item.staff_type === 'Inbound') {
                item.staff_type = '收货组'
              } else if (item.staff_type === 'Outbound') {
                item.staff_type = '发货组'
              } else if (item.staff_type === 'StockControl') {
                item.staff_type = '库存管理'
              }
            })
          }
          _this.pathname_previous = res.previous
          _this.pathname_next = res.next
        })
        .catch(err => {
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
    },
    downloadPickingList (e) {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(baseurl + 'dn/picklistdownload/?lang=' + LocalStorage.getItem('lang') + '&picker=' + e.staff_name + '&picking_status=1&order_line=1', {}).then(res => {
          console.log(res.results)
          console.log(baseurl + res.results)
          getauth(baseurl + res.results, {}).then(res => {
            _this.$q.notify({
              message: '下载成功',
              color: 'green',
              icon: 'check'
            })
          })
        })
      } else {
        _this.$q.notify({
          message: _this.$t('notice.loginerror'),
          color: 'negative',
          icon: 'warning'
        })
      }
    }
  },
  created () {
    var _this = this
    if (LocalStorage.has('openid')) {
      _this.openid = LocalStorage.getItem('openid')
    } else {
      _this.openid = ''
      LocalStorage.set('openid', '')
    }
    if (LocalStorage.has('login_name')) {
      _this.login_name = LocalStorage.getItem('login_name')
    } else {
      _this.login_name = ''
      LocalStorage.set('login_name', '')
    }
    if (LocalStorage.has('auth')) {
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
    if (LocalStorage.getItem('lang') === 'zh-hans') {
      _this.staff_type_list = ['经理', '主管', '收货组', '发货组', '库存控制', '客户', '供应商']
    } else {
      _this.staff_type_list = ['Manager', 'Supervisor', 'Inbount', 'Outbound', 'StockControl', 'Customer', 'Supplier']
    }
  },
  updated () {
  },
  destroyed () {
  }
}
</script>
