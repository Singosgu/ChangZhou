(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[54],{"5cb3":function(t,e,a){"use strict";var i=a("5d52"),s=a.n(i);e["default"]=s.a},"5d52":function(t,e){},"9b51":function(t,e,a){"use strict";a.r(e);var i=function(){var t=this,e=t._self._c;return e("div",[e("q-input",{staticStyle:{display:"none"},model:{value:t.scaneddata.request_time,callback:function(e){t.$set(t.scaneddata,"request_time",e)},expression:"scaneddata.request_time"}}),e("q-card",{directives:[{name:"show",rawName:"v-show",value:!t.fab,expression:"!fab"}],style:{width:t.width,height:t.height},attrs:{flat:""}},[e("q-card-section",[e("q-bar",{staticClass:"bg-white q-mb-sm shadow-1"},[e("q-input",{staticStyle:{"font-size":"12px",width:"100%"},attrs:{borderless:"","stack-label":"",label:t.$t("driver.view_driver.license_plate")},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.driverConfirm()},blur:function(e){return t.driverConfirm()}},model:{value:t.license_plate,callback:function(e){t.license_plate=e},expression:"license_plate"}})],1),e("q-bar",{staticClass:"bg-white q-mb-sm shadow-1"},[e("div",{staticStyle:{"font-size":"12px",width:"100%"}},[t._v(t._s(t.$t("driver.view_driver.driver_name"))+": "+t._s(t.driver_list.driver_name))])]),e("q-bar",{staticClass:"bg-white q-mb-sm shadow-1"},[e("div",{staticStyle:{"font-size":"12px",width:"100%"}},[t._v(t._s(t.$t("driver.view_driver.contact"))+": "+t._s(t.driver_list.contact))])]),e("q-btn-group",{attrs:{push:""}},[e("q-btn",{attrs:{color:"purple",label:t.$t("stock.view_stocklist.cyclecountresult")},on:{click:function(e){return t.dispatchDataCheck()}}})],1)],1),e("q-scroll-area",{ref:"scrollArea",style:{height:t.scroll_height,width:t.width},attrs:{"thumb-style":t.thumbStyle,"bar-style":t.barStyle}},[e("q-markup-table",[e("thead",[e("tr",[e("th",{staticClass:"text-center"},[t._v(t._s(t.scan_dn_code))]),e("th",{staticClass:"text-center"},[t._v(t._s(t.scan_goods_code))]),e("th",{staticClass:"text-center"},[t._v(t._s(t.order_qty))]),e("th",{staticClass:"text-center"},[t._v(t._s(t.picking_qty))])])]),e("tbody",[t._l(t.table_list,(function(a,i){return e("tr",{key:i,attrs:{id:"dom"+i}},[e("td",{staticClass:"text-center"},[t._v(t._s(a.dn_code))]),e("td",{staticClass:"text-center"},[t._v(t._s(a.goods_code))]),e("td",{staticClass:"text-center"},[t._v(t._s(a.goods_qty))]),e("td",{staticClass:"text-center"},[t._v(t._s(a.picked_qty))])])}))],2)])],1)],1)],1)},s=[],n=a("3004"),o=a("18d6"),r=a("09f9"),c={name:"Page_shipping",data(){return{openid:"",login_name:"",authin:"0",pathname:"dn/detail/?dn_status=4&picked_qty__gt=0&dn_code=",width:"",height:"",scroll_height:"",table_list:[],driver_list:"",dn_list:"",scan_dn_code:this.$t("outbound.view_dn.dn_code"),scan_goods_code:this.$t("scan.scan_goods_code"),order_qty:this.$t("outbound.view_dn.goods_qty"),picking_qty:this.$t("stock.view_stocklist.picked_stock"),thumbStyle:{right:"4px",borderRadius:"5px",backgroundColor:"#E0E0E0",width:"5px",opacity:.75},barStyle:{right:"2px",borderRadius:"9px",backgroundColor:"#EEEEEE",width:"9px",opacity:.2},bar_scanned:"",submitdata:{dn_code:"",driver:""},license_plate:""}},methods:{getDNList(t){var e=this;Object(n["e"])("dn/list/?dn_code="+t,{}).then((t=>{0===t.results.length?(navigator.vibrate(100),e.$q.notify({message:"No DN Data",position:"top",icon:"close",color:"negative"})):(e.dn_list=t.results[0],e.submitdata.dn_code=e.dn_list.dn_code)})).catch((t=>{navigator.vibrate(100),e.$q.notify({message:t.detail,position:"top",icon:"close",color:"negative"})}))},getDNDetailList(t){var e=this;Object(n["e"])(e.pathname+t,{}).then((t=>{0===t.results.length?(navigator.vibrate(100),e.$q.notify({message:"No DN Data",position:"top",icon:"close",color:"negative"})):e.table_list=t.results})).catch((t=>{navigator.vibrate(100),e.$q.notify({message:t.detail,position:"top",icon:"close",color:"negative"})}))},driverConfirm(){var t=this;""!==t.license_plate&&Object(n["e"])("driver/?license_plate="+t.license_plate,{}).then((e=>{0===e.results.length?(t.driver_list="",navigator.vibrate(100),t.$q.notify({message:"No Driver Data",position:"top",icon:"close",color:"negative"})):1===e.results.length?(t.driver_list=e.results[0],t.submitdata.driver=t.driver_list.driver_name):(t.driver_list="",navigator.vibrate(100),t.$q.notify({message:"Repeating Data",position:"top",icon:"close",color:"negative"}))})).catch((e=>{t.driver_list="",navigator.vibrate(100),t.$q.notify({message:e.detail,position:"top",icon:"close",color:"negative"})}))},dispatchDataCheck(){var t=this;""===t.dn_list?t.$q.notify({message:"Please Scan Your DN",position:"top",icon:"close",color:"negative"}):""===t.driver_list?t.$q.notify({message:"Please Confirm Your Driver Info",position:"top",icon:"close",color:"negative"}):t.dispatchDataSubmit()},dispatchDataSubmit(){var t=this;Object(n["i"])("dn/dispatch/"+t.dn_list.id+"/",t.submitdata).then((e=>{t.$q.notify({message:"Success Dispatch",position:"top",icon:"check",color:"green"}),setTimeout((function(){location.reload()}),1e3)})).catch((e=>{t.$q.notify({message:e.detail,position:"top",icon:"close",color:"negative"})}))}},computed:{fab:{get(){return this.$store.state.fabchange.fab}},scaneddata:{get(){return this.$store.state.scanedsolve.scaneddata}}},created(){var t=this;o["a"].has("openid")?t.openid=o["a"].getItem("openid"):(t.openid="",o["a"].set("openid","")),o["a"].has("login_name")?t.login_name=o["a"].getItem("login_name"):(t.login_name="",o["a"].set("login_name","")),o["a"].has("auth")?t.authin="1":t.authin="0"},mounted(){var t=this;t.width=1*r["a"].width+"px",t.height=r["a"].height-50+"px",t.scroll_height=r["a"].height-240+"px",t.bar_scanned=""},updated(){var t=this;""!==t.scaneddata&&t.bar_scanned!==t.scaneddata.request_time&&("DN"===t.scaneddata.mode?(t.bar_scanned=t.scaneddata.request_time,t.getDNList(t.scaneddata.code),t.getDNDetailList(t.scaneddata.code)):t.$q.notify({message:"No DN Query Data",position:"top",icon:"close",color:"negative"}))}},d=c,l=a("42e1"),_=a("5cb3"),h=a("27f9"),p=a("f09f"),u=a("a370"),v=a("d847"),g=a("e7a9"),b=a("9c40"),m=a("4983"),f=a("2bb1"),y=a("eebe"),q=a.n(y),w=Object(l["a"])(d,i,s,!1,null,null,null);"function"===typeof _["default"]&&Object(_["default"])(w);e["default"]=w.exports;q()(w,"components",{QInput:h["a"],QCard:p["a"],QCardSection:u["a"],QBar:v["a"],QBtnGroup:g["a"],QBtn:b["a"],QScrollArea:m["a"],QMarkupTable:f["a"]})}}]);