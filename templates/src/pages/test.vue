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
              <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('refreshtip') }}</q-tooltip>
            </q-btn>
          </q-btn-group>
          <q-space />
          <q-input outlined rounded dense debounce="300" color="primary" v-model="filter" :placeholder="$t('search')" @input="getSearchList()" @keyup.enter="getSearchList()">
            <template v-slot:append>
              <q-icon name="search" @click="getSearchList()" />
            </template>
          </q-input>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="bin_name" :props="props">{{ props.row.bin_name }}</q-td>
            <q-td key="bin_size" :props="props">{{ props.row.bin_size }}</q-td>
            <q-td key="bin_property" :props="props">{{ props.row.bin_property }}</q-td>
            <q-td key="empty_label" :props="props">{{ props.row.empty_label }}</q-td>
            <q-td key="creater" :props="props">{{ props.row.creater }}</q-td>
            <q-td key="create_time" :props="props">{{ props.row.create_time }}</q-td>
            <q-td key="update_time" :props="props">{{ props.row.update_time }}</q-td>
              <q-td key="action" :props="props" style="width: 100px">
                <q-btn
                  round
                  flat
                  push
                  color="info"
                  icon="component_exchange"
                  @click="Move(props.row)"
                >
                  <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">AGV Move</q-tooltip>
                </q-btn>
              </q-td>
          </q-tr>
        </template>
      </q-table>
    </transition>
    <template>
        <div v-show="max !== 0" class="q-pa-lg flex flex-center">
           <div>{{ total }} </div>
          <q-pagination
            v-model="current"
            color="black"
            :max="max"
            :max-pages="6"
            boundary-links
            @click="getList()"
          />
          <div>
            <input
              v-model="paginationIpt"
              @blur="changePageEnter"
              @keyup.enter="changePageEnter"
              style="width: 60px; text-align: center"
            />
          </div>
        </div>
        <div v-show="max === 0" class="q-pa-lg flex flex-center">
          <q-btn flat push color="dark" :label="$t('no_data')"></q-btn>
        </div>
    </template>
    <q-dialog v-model="MoveForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ MoveFormData.from_bin }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-select
            dense
            outlined
            square
            v-model="MoveFormData.to_bin"
            :options="bin_list"
            transition-show="scale"
            transition-hide="scale"
            label="To Bin"
            :rules="[val => (val && val.length > 0) || error2]"
          />
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="newDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="newDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
  </div>

</template>
<router-view />

<script>
import { LocalStorage } from 'quasar'
import { baseurl, getauth, postauth } from 'boot/axios_request'

export default {
  name: 'Pagebinset',
  data () {
    return {
      bin_name: '',
      bin_property: '',
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'binset/',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      table_list: [],
      bin_list: [],
      bin_property_list: [],
      viewForm: false,
      printObj: {
        id: 'printMe',
        popTitle: this.$t('inbound.asn')
      },
      columns: [
        { name: 'bin_name', required: true, label: this.$t('warehouse.view_binset.bin_name'), align: 'left', field: 'bin_name' },
        { name: 'bin_size', label: this.$t('warehouse.view_binset.bin_size'), field: 'bin_size', align: 'center' },
        { name: 'bin_property', label: this.$t('warehouse.view_binset.bin_property'), field: 'bin_property', align: 'center' },
        { name: 'empty_label', label: this.$t('warehouse.view_binset.empty_label'), field: 'empty_label', align: 'center' },
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
      MoveForm: false,
      MoveFormData: {
        from_in: '',
        to_bin: '',
        creater: ''
      },
      error1: this.$t('warehouse.view_binset.error1'),
      error2: this.$t('warehouse.view_binset.error2'),
      error3: this.$t('warehouse.view_binset.error3'),
      current: 1,
      max: 0,
      total: 0,
      paginationIpt: 1
    }
  },
  methods: {
    getList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname + '?page=' + '' + _this.current, {})
          .then(res => {
            _this.table_list = res.results
            _this.total = res.count
            if (res.count === 0) {
              _this.max = 0
            } else {
              if (Math.ceil(res.count / 30) === 1) {
                _this.max = 0
              } else {
                _this.max = Math.ceil(res.count / 30)
              }
            }
            if (LocalStorage.getItem('lang') === 'zh-hans') {
              _this.table_list.forEach((item, index) => {
                if (item.bin_property === 'Damage') {
                  item.bin_property = '破损'
                } else if (item.bin_property === 'Inspection') {
                  item.bin_property = '质检'
                } else if (item.bin_property === 'Holding') {
                  item.bin_property = '锁货'
                } else if (item.bin_property === 'Normal') {
                  item.bin_property = '正常库位'
                }
                if (!item.empty_label) {
                  item.empty_label = '否'
                } else if (item.empty_label) {
                  item.empty_label = '是'
                }
              })
            }
            _this.bin_property_list = res.bin_property_list
            if (LocalStorage.getItem('lang') === 'zh-hans') {
              _this.bin_property_list.forEach((item, index) => {
                console.log(item)
                if (item === 'Damage') {
                  _this.bin_property_list[index] = '破损'
                } else if (item === 'Inspection') {
                  _this.bin_property_list[index] = '质检'
                } else if (item === 'Holding') {
                  _this.bin_property_list[index] = '锁货'
                } else if (item === 'Normal') {
                  _this.bin_property_list[index] = '正常库位'
                }
              })
            }
            _this.bin_list = res.bin_list
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
      }
    },
    changePageEnter (e) {
      if (Number(this.paginationIpt) < 1) {
        this.current = 1
        this.paginationIpt = 1
      } else if (Number(this.paginationIpt) > this.max) {
        this.current = this.max
        this.paginationIpt = this.max
      } else {
        this.current = Number(this.paginationIpt)
      }
      this.getList()
    },
    getSearchList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        _this.current = 1
        _this.paginationIpt = 1
        getauth(_this.pathname + '?bin_name__icontains=' + _this.filter + '&page=' + '' + _this.current, {})
          .then(res => {
            _this.table_list = res.results
            _this.total = res.count
            if (res.count === 0) {
              _this.max = 0
            } else {
              if (Math.ceil(res.count / 30) === 1) {
                _this.max = 0
              } else {
                _this.max = Math.ceil(res.count / 30)
              }
            }
            if (LocalStorage.getItem('lang') === 'zh-hans') {
              _this.table_list.forEach((item, index) => {
                if (item.bin_property === 'Damage') {
                  item.bin_property = '破损'
                } else if (item.bin_property === 'Inspection') {
                  item.bin_property = '质检'
                } else if (item.bin_property === 'Holding') {
                  item.bin_property = '锁货'
                } else if (item.bin_property === 'Normal') {
                  item.bin_property = '正常库位'
                }
                if (!item.empty_label) {
                  item.empty_label = '否'
                } else if (item.empty_label) {
                  item.empty_label = '是'
                }
              })
            }

            _this.bin_property_list = res.bin_property_list
            if (LocalStorage.getItem('lang') === 'zh-hans') {
              _this.bin_property_list.forEach((item, index) => {
                if (item === 'Damage') {
                  _this.bin_property_list[index] = '破损'
                } else if (item === 'Inspection') {
                  _this.bin_property_list[index] = '质检'
                } else if (item === 'Holding') {
                  _this.bin_property_list[index] = '锁货'
                } else if (item === 'Normal') {
                  _this.bin_property_list[index] = '正常库位'
                }
              })
            }
            _this.bin_list = res.bin_list
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
      } else {
      }
    },
    getListPrevious () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_previous, {})
          .then(res => {
            _this.table_list = res.results
            if (LocalStorage.getItem('lang') === 'zh-hans') {
              _this.table_list.forEach((item, index) => {
                if (item.bin_property === 'Damage') {
                  item.bin_property = '破损'
                } else if (item.bin_property === 'Inspection') {
                  item.bin_property = '质检'
                } else if (item.bin_property === 'Holding') {
                  item.bin_property = '锁货'
                } else if (item.bin_property === 'Normal') {
                  item.bin_property = '正常库位'
                }
                if (!item.empty_label) {
                  item.empty_label = '否'
                } else if (item.empty_label) {
                  item.empty_label = '是'
                }
              })
            }
            _this.bin_property_list = res.bin_property_list
            _this.bin_property_list.forEach((item, index) => {
              if (item === 'Damage') {
                _this.bin_property_list[index] = '破损'
              } else if (item === 'Inspection') {
                _this.bin_property_list[index] = '质检'
              } else if (item === 'Holding') {
                _this.bin_property_list[index] = '锁货'
              } else if (item === 'Normal') {
                _this.bin_property_list[index] = '正常库位'
              }
            })
            _this.bin_list = res.bin_list
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
      } else {
      }
    },
    getListNext () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_next, {})
          .then(res => {
            _this.table_list = res.results
            if (LocalStorage.getItem('lang') === 'zh-hans') {
              _this.table_list.forEach((item, index) => {
                if (item.bin_property === 'Damage') {
                  item.bin_property = '破损'
                } else if (item.bin_property === 'Inspection') {
                  item.bin_property = '质检'
                } else if (item.bin_property === 'Holding') {
                  item.bin_property = '锁货'
                } else if (item.bin_property === 'Normal') {
                  item.bin_property = '正常库位'
                }
                if (!item.empty_label) {
                  item.empty_label = '否'
                } else if (item.empty_label) {
                  item.empty_label = '是'
                }
              })
            }
            _this.bin_property_list = res.bin_property_list
            if (LocalStorage.getItem('lang') === 'zh-hans') {
              _this.bin_property_list.forEach((item, index) => {
                if (item === 'Damage') {
                  _this.bin_property_list[index] = '破损'
                } else if (item === 'Inspection') {
                  _this.bin_property_list[index] = '质检'
                } else if (item === 'Holding') {
                  _this.bin_property_list[index] = '锁货'
                } else if (item === 'Normal') {
                  _this.bin_property_list[index] = '正常库位'
                }
              })
            }
            _this.bin_list = res.bin_list
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
      } else {
      }
    },
    reFresh () {
      var _this = this
      _this.getList()
    },
    newDataSubmit () {
      var _this = this
      var binsets = []
      _this.table_list.forEach(i => {
        binsets.push(i.bin_name)
      })
      if (binsets.indexOf(_this.MoveFormData.from_bin) === -1 && _this.MoveFormData.to_bin.length !== 0) {
        _this.MoveFormData.creater = _this.login_name
        postauth(baseurl + 'tasklist/agvmove/', _this.MoveFormData)
          .then(res => {
            _this.getList()
            _this.newDataCancel()
            _this.$q.notify({
              message: 'Success Move',
              icon: 'check',
              color: 'green'
            })
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else if (binsets.indexOf(_this.MoveFormData.from_bin) !== -1) {
        _this.$q.notify({
          message: _this.$t('notice.warehouseerror.binseterror'),
          icon: 'close',
          color: 'negative'
        })
      } else if (_this.MoveFormData.from_bin.length === 0) {
        _this.$q.notify({
          message: _this.$t('warehouse.view_binset.error1'),
          icon: 'close',
          color: 'negative'
        })
      }
      binsets = []
    },
    newDataCancel () {
      var _this = this
      _this.MoveForm = false
      _this.MoveFormData = {
        from_bin: '',
        to_bin: '',
        creater: ''
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
  mounted() {
    var _this = this
    if (_this.$q.platform.is.electron) {
      _this.height = String(_this.$q.screen.height - 290) + 'px'
    } else {
      _this.height = _this.$q.screen.height - 290 + '' + 'px'
    }
  },
  updated() {
  },
  destroyed() {
  }
}
</script>
