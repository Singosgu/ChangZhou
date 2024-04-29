<template>
    <div>
      <template>
        <div class="q-pa-lg flex flex-center">
          <q-input filled v-model="miandan" disable readonly label="面单号" style="width: 400px"/>
          <input v-model="scan_miandan" type="hidden" />
        </div>
      </template>
    </div>
</template>
    <router-view />

<script>
import { date, exportFile, LocalStorage } from 'quasar'
import { getauth, postauth, putauth, deleteauth, getfile } from 'boot/axios_request'

export default {
  name: 'Pageprinter',
  data () {
    return {
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'binsize/',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      table_list: [],
      columns: [
        { name: 'bin_size', required: true, label: this.$t('warehouse.view_binsize.bin_size'), align: 'left', field: 'bin_size' },
        { name: 'bin_size_w', label: this.$t('warehouse.view_binsize.bin_size_w'), field: 'bin_size_w', align: 'center' },
        { name: 'bin_size_d', label: this.$t('warehouse.view_binsize.bin_size_d'), field: 'bin_size_d', align: 'center' },
        { name: 'bin_size_h', label: this.$t('warehouse.view_binsize.bin_size_h'), field: 'bin_size_h', align: 'center' },
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
      newForm: false,
      newFormData: {
        bin_size: '',
        bin_size_w: '',
        bin_size_d: '',
        bin_size_h: '',
        creater: ''
      },
      editid: 0,
      editFormData: {},
      editMode: false,
      deleteForm: false,
      deleteid: 0,
      error1: this.$t('warehouse.view_binsize.error1'),
      error2: this.$t('warehouse.view_binsize.error2'),
      error3: this.$t('warehouse.view_binsize.error3'),
      error4: this.$t('warehouse.view_binsize.error4'),
      printer: '',
      printer_options: [],
      miandan: '',
      scan_miandan: ''
    }
  },
  methods: {
    getList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth('http://127.0.0.1:8008/getprinter/', {
        }).then(res => {
          _this.printer_options = res.results
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
    setPrinter () {
      var _this = this
      if (LocalStorage.has('auth')) {
        _this.$q.localStorage.set('printer', _this.printer)
      }
    },
    getSearchList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname + '?bin_size__icontains=' + _this.filter, {
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
    getListPrevious () {
      var _this = this
      if (LocalStorage.has('auth')) {
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
      if (LocalStorage.has('auth')) {
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
    newDataSubmit () {
      var _this = this
      var binsizes = []
      _this.table_list.forEach(i => {
        binsizes.push(i.bin_size)
      })
      if (binsizes.indexOf(_this.newFormData.bin_size) === -1 && _this.newFormData.bin_size.length !== 0) {
        _this.newFormData.creater = _this.login_name
        postauth(_this.pathname, _this.newFormData).then(res => {
          _this.getList()
          _this.newDataCancel()
          _this.$q.notify({
            message: 'Success Create',
            icon: 'check',
            color: 'green'
          })
        }).catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
      } else if (binsizes.indexOf(_this.newFormData.bin_size) !== -1) {
        _this.$q.notify({
          message: _this.$t('notice.warehouseerror.binsizeerror'),
          icon: 'close',
          color: 'negative'
        })
      } else if (_this.newFormData.bin_size.length === 0) {
        _this.$q.notify({
          message: _this.$t('warehouse.view_binsize.error1'),
          icon: 'close',
          color: 'negative'
        })
      }
      binsizes = []
    },
    newDataCancel () {
      var _this = this
      _this.newForm = false
      _this.newFormData = {
        bin_size: '',
        bin_size_w: 0,
        bin_size_d: 0,
        bin_size_h: 0,
        creater: ''
      }
    },
    editData (e) {
      var _this = this
      _this.editMode = true
      _this.editid = e.id
      _this.editFormData = {
        bin_size: e.bin_size,
        bin_size_w: e.bin_size_w,
        bin_size_d: e.bin_size_d,
        bin_size_h: e.bin_size_h,
        creater: _this.login_name
      }
    },
    editDataSubmit () {
      var _this = this
      putauth(_this.pathname + _this.editid + '/', _this.editFormData).then(res => {
        _this.editDataCancel()
        _this.getList()
        _this.$q.notify({
          message: 'Success Edit Data',
          icon: 'check',
          color: 'green'
        })
      }).catch(err => {
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
    editDataCancel () {
      var _this = this
      _this.editMode = false
      _this.editid = 0
      _this.editFormData = {
        bin_size: '',
        bin_size_w: 0,
        bin_size_d: 0,
        bin_size_h: 0,
        creater: ''
      }
    },
    deleteData (e) {
      var _this = this
      _this.deleteForm = true
      _this.deleteid = e
    },
    deleteDataSubmit () {
      var _this = this
      deleteauth(_this.pathname + _this.deleteid + '/').then(res => {
        _this.deleteDataCancel()
        _this.getList()
        _this.$q.notify({
          message: 'Success Edit Data',
          icon: 'check',
          color: 'green'
        })
      }).catch(err => {
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
    deleteDataCancel () {
      var _this = this
      _this.deleteForm = false
      _this.deleteid = 0
    },
    downloadData () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getfile(_this.pathname + 'file/?lang=' + LocalStorage.getItem('lang')).then(res => {
          var timeStamp = Date.now()
          var formattedString = date.formatDate(timeStamp, 'YYYYMMDDHHmmssSSS')
          const status = exportFile(
            _this.pathname + formattedString + '.csv',
            '\uFEFF' + res.data,
            'text/csv'
          )
          if (status !== true) {
            _this.$q.notify({
              message: 'Browser denied file download...',
              color: 'negative',
              icon: 'warning'
            })
          }
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
      // _this.getList()
    } else {
      _this.authin = '0'
    }
  },
  mounted () {
    var _this = this
    if (_this.$q.localStorage.has('printer')) {
      _this.printer = _this.$q.localStorage.getItem('printer')
    } else {
      _this.printer = ''
      _this.$q.localStorage.set('printer', '')
    }
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
