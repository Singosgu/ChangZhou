(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[8],{d28a:function(t,e){},df00:function(t,e,a){"use strict";var s=a("d28a"),o=a.n(s);e["default"]=o.a},e5bc:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t._self._c;return e("div",[e("q-input",{staticStyle:{display:"none"},model:{value:t.scaneddata.request_time,callback:function(e){t.$set(t.scaneddata,"request_time",e)},expression:"scaneddata.request_time"}}),e("q-card",{directives:[{name:"show",rawName:"v-show",value:!t.fab,expression:"!fab"}],style:{width:t.width,height:t.height},attrs:{flat:""}},[e("q-card-section",[e("q-bar",{staticClass:"bg-white q-mb-sm shadow-1"},[e("div",{staticStyle:{"font-size":"12px",width:"100%"}},[t._v(t._s(t.$t("inbound.view_asn.asn_code"))+": "+t._s(t.asn_scan))])]),e("q-btn-group",{attrs:{push:""}},[e("q-btn",{attrs:{color:"purple",label:t.$t("stock.view_stocklist.cyclecountresult")},on:{click:function(e){return t.sortedSubmit()}}})],1)],1),e("q-scroll-area",{ref:"scrollArea",style:{height:t.scroll_height,width:t.width},attrs:{"thumb-style":t.thumbStyle,"bar-style":t.barStyle}},[e("q-markup-table",[e("thead",[e("tr",[e("th",{staticClass:"text-center"},[t._v(t._s(t.scan_goods_code))]),e("th",{staticClass:"text-center"},[t._v(t._s(t.goods_qty))]),e("th",{staticClass:"text-center"},[t._v(t._s(t.goods_actual_qty))])])]),e("tbody",[t._l(t.table_list,(function(a,s){return e("tr",{key:s,attrs:{id:"dom"+s}},[e("td",{class:{"scan-background text-center":a.goods_code===t.goods_scan,"text-center":a.goods_code!==t.goods_scan}},[t._v(t._s(a.goods_code))]),e("td",{class:{"scan-background text-center":a.goods_code===t.goods_scan,"text-center":a.goods_code!==t.goods_scan}},[t._v(t._s(a.goods_qty))]),e("td",{staticClass:"text-center"},[e("input",{directives:[{name:"model",rawName:"v-model.number",value:a.goods_actual_qty,expression:"item.goods_actual_qty",modifiers:{number:!0}}],attrs:{type:"number",label:t.goods_actual_qty},domProps:{value:a.goods_actual_qty},on:{input:function(e){e.target.composing||t.$set(a,"goods_actual_qty",t._n(e.target.value))},blur:function(e){return t.$forceUpdate()}}})])])}))],2)])],1)],1)],1)},o=[],n=(a("caad"),a("3004")),i=a("18d6"),c=a("09f9"),d={name:"Page_sorting",data(){return{openid:"",login_name:"",authin:"0",pathname:"asn/detail/?asn_status=3&asn_code=",width:"",height:"",scroll_height:"",table_list:[],scan_goods_code:this.$t("scan.scan_goods_code"),goods_qty:this.$t("inbound.view_asn.goods_qty"),goods_actual_qty:this.$t("inbound.view_asn.goods_actual_qty"),thumbStyle:{right:"4px",borderRadius:"5px",backgroundColor:"#E0E0E0",width:"5px",opacity:.75},barStyle:{right:"2px",borderRadius:"9px",backgroundColor:"#EEEEEE",width:"9px",opacity:.2},bar_scanned:"",asn_scan:"",goods_scan:"",error1:this.$t("scan.scan_goods_label_error"),error2:this.$t("scan.view_picking.picking_qty_error")}},methods:{getASNDetailList(t){var e=this;Object(n["e"])(e.pathname+t,{}).then((t=>{0===t.results.length?e.$q.notify({message:"No ASN Data",position:"top",icon:"close",color:"negative"}):(console.log(t),e.asn_scan=t.results[0].asn_code,e.table_list=t.results)})).catch((t=>{e.$q.notify({message:t.detail,position:"top",icon:"close",color:"negative"})}))},getGoodsList(t){var e=this;e.table_list.filter((a=>!a.goods_code.includes(t)||(e.goods_scan=t,a.goods_actual_qty+=1,!1)))},sortedSubmit(){var t=this,e={asn_code:t.asn_scan,goodsData:t.table_list,creater:t.login_name};t.sortedDataSubmit(e)},sortedDataSubmit(t){var e=this;Object(n["j"])("asn/sorted/",t).then((t=>{e.table_list=[],e.goods_scan="",e.dn_scan="",t.detail||e.$q.notify({message:"Success Confirm ASN Sorted List",position:"top",icon:"check",color:"green"})})).catch((t=>{e.$q.notify({message:t.detail,position:"top",icon:"close",color:"negative"})}))}},computed:{fab:{get(){return this.$store.state.fabchange.fab}},scaneddata:{get(){return this.$store.state.scanedsolve.scaneddata}}},created(){var t=this;i["a"].has("openid")?t.openid=i["a"].getItem("openid"):(t.openid="",i["a"].set("openid","")),i["a"].has("login_name")?t.login_name=i["a"].getItem("login_name"):(t.login_name="",i["a"].set("login_name","")),i["a"].has("auth")?t.authin="1":t.authin="0"},mounted(){var t=this;t.width=1*c["a"].width+"px",t.height=c["a"].height-50+"px",t.scroll_height=c["a"].height-225+"px"},updated(){var t=this;""!==t.scaneddata&&t.bar_scanned!==t.scaneddata.request_time&&("ASN"===t.scaneddata.mode?(t.bar_scanned=t.scaneddata.request_time,t.goods_scan="",t.asn_scan="",t.getASNDetailList(t.scaneddata.code)):"GOODS"===t.scaneddata.mode?(t.bar_scanned=t.scaneddata.request_time,t.getGoodsList(t.scaneddata.code)):t.$q.notify({message:"No Query Data",position:"top",icon:"close",color:"negative"}))},beforeDestroy(){}},r=d,l=a("42e1"),_=a("df00"),u=a("27f9"),g=a("f09f"),h=a("a370"),b=a("d847"),p=a("e7a9"),m=a("9c40"),f=a("4983"),y=a("2bb1"),v=a("eebe"),q=a.n(v),w=Object(l["a"])(r,s,o,!1,null,null,null);"function"===typeof _["default"]&&Object(_["default"])(w);e["default"]=w.exports;q()(w,"components",{QInput:u["a"],QCard:g["a"],QCardSection:h["a"],QBar:b["a"],QBtnGroup:p["a"],QBtn:m["a"],QScrollArea:f["a"],QMarkupTable:y["a"]})}}]);