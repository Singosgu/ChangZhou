<template>
    <div>
      <template>
        <div class="q-pa-lg flex flex-center">
          <q-input filled v-model="miandan" disable readonly label="面单号" style="width: 400px"/>
          <input v-model="scan_miandan" type="hidden" />
        </div>
      </template>
      <template>
        <audio ref="audioPlayer" src="/statics/mp3/Outbound_Success.mp3" hidden></audio>
      </template>
    </div>
</template>
    <router-view />

<script>
import { getauth, putauth } from 'boot/axios_request'

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
      scan_detail: [],
      miandan: '',
      scan_miandan: ''
    }
  },
  methods: {
    playAudio () {
      const audioPlayer = this.$refs.audioPlayer;
      audioPlayer.play();
    },
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
      var _this = this
      _this.miandan = e
      getauth('scanner/list/' + e + '/', {}).then(res => {
        if (!res.detail) {
          this.resData = res.code
          this.resMode = res.mode
          if (this.resMode === 'MD') {
            this.MDConfirm()
          } else {
            this.$q.notify({
              message: e + '编码不存在',
              icon: 'close',
              color: 'negative'
            })
          }
        }
      }).catch(err => {
        console.log(err)
      })
    },
    MDConfirm () {
      getauth('dn/list/?trackingnumber=' + this.miandan).then((res) => {
        if (res.results.length > 0) {
          if (res.results[0].dn_status === 4) {
            postauth('dn/dispatch/' + res.results[0].id + '/', res.results[0]).then((res) => {
              this.playAudio()
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
            getauth('http://127.0.0.1:8008/print/' + this.$q.localStorage.getItem('printer') + '/' + e.txnid + '/', {}).then((res) => {
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
      console.log(e.key, e.keyCode)
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
