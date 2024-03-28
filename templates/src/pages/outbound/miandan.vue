<template>
  <q-page class="flex flex-center">
    {{ $route.path }}
    <q-pdfviewer
      v-model="show"
      type="html5"
      :src="updatedSrc"
      content-class="absolute"
    />
  </q-page>
</template>

<script>
import { baseurl } from 'boot/axios_request'
export default {
  data () {
    return {
      show: true,
      src: baseurl + '/media/miandan/'
    }
  },
  computed: {
    updatedSrc () {
      if (process.env.MODE === 'electron') {
        return '/' + this.src
      }
      return this.src
    }
  }
}
</script>
