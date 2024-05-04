<template>
  <q-page class="flex flex-top">
<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md" style="max-width: 100%">
      <q-tabs
        v-model="detaillink"
      >
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="dn" :label="$t('outbound.dn')" icon="img:statics/outbound/dnlist.png" :to="{ name: 'dn' }" exact/>
        </transition>
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="neworder" label="发货单明细" icon="img:statics/outbound/order.png" :to="{ name: 'neworder' }" exact/>
        </transition>
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="freshorder" label="单件发货单" icon="img:statics/outbound/freshorder.png" :to="{ name: 'freshorder' }" exact/>
        </transition>
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="neworder" label="多件发货单" icon="img:statics/outbound/order.png" :to="{ name: 'neworder' }" exact/>
        </transition>
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="backorder" :label="$t('outbound.backorder')" icon="img:statics/outbound/backorder.png" :to="{ name: 'backorder' }" exact/>
        </transition>
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="pickstock" :label="$t('outbound.pickstock')" icon="img:statics/outbound/pickstock.png" :to="{ name: 'pickstock' }" exact/>
        </transition>
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="pickedstock" :label="$t('outbound.pickedstock')" icon="img:statics/outbound/picked.png" :to="{ name: 'pickedstock' }" exact/>
        </transition>
<!--        <transition appear enter-active-class="animated zoomIn">-->
<!--          <q-route-tab name="pickinglist" :label="$t('outbound.pickinglist')" icon="img:statics/outbound/pickinglist.png" :to="{ name: 'pickinglist' }" exact/>-->
<!--        </transition>-->
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="scanpicking" label="单件拣货单" icon="receipt_long" :to="{ name: 'scanpicking' }" exact/>
        </transition>
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="scanpicking" label="多件拣货单" icon="dvr" :to="{ name: 'scanpicking' }" exact/>
        </transition>
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="scanpicking" label="单件出库" icon="barcode_reader" :to="{ name: 'scanpicking' }" exact/>
        </transition>
        <transition appear enter-active-class="animated zoomIn">
          <q-route-tab name="scanpicking" label="多件出库" icon="qr_code_scanner" :to="{ name: 'scanpicking' }" exact/>
        </transition>
<!--        <transition appear enter-active-class="animated zoomIn">-->
<!--          <q-route-tab name="shippedstock" label="扫描出库" icon="img:statics/outbound/outbound.png" :to="{ name: 'shippedstock' }" exact/>-->
<!--        </transition>-->
<!--        <transition appear enter-active-class="animated zoomIn">-->
<!--          <q-route-tab name="pod" :label="$t('outbound.pod')" icon="img:statics/outbound/receiving.png" :to="{ name: 'pod' }" exact/>-->
<!--        </transition>-->
      </q-tabs>
    </div>
  </div>
</template>
    <div class="main-table">
      <router-view />
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'Pageoutbound',
  data () {
    return {
      detaillink: 'dn'
    }
  },
  methods: {
  }
}
</script>
