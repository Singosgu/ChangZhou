(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[110],{c2ce:function(t,a,e){"use strict";e.r(a);var o=function(){var t=this,a=t._self._c;return a("q-page",[a("router-view"),a("q-page-sticky",{attrs:{position:"bottom-left",offset:[18,18]}},[a("input",{directives:[{name:"model",rawName:"v-model",value:t.barscan,expression:"barscan"}],attrs:{id:"scannedBarcodes",type:"text",readonly:"",disabled:""},domProps:{value:t.barscan},on:{input:function(a){a.target.composing||(t.barscan=a.target.value)}}})]),a("q-page-sticky",{attrs:{position:"bottom-right",offset:[18,18]}},[a("q-fab",{attrs:{icon:"add",direction:"up",color:"accent","vertical-actions-align":"left"},model:{value:t.fab,callback:function(a){t.fab=a},expression:"fab"}},[a("q-fab-action",{style:{"margin-top":t.fab8.top,"margin-bottom":t.fab8.bottom,"margin-left":t.fab8.left,"margin-right":t.fab8.right,height:t.touchheight,width:t.touchwidth},attrs:{square:"",flat:"","external-label":"","label-position":"bottom","label-class":"text-black",label:t.$t("scan.scan_locationquery"),"label-style":"background-color:transparent",to:{name:"zebra_locationquery"}}},[a("q-img",{attrs:{src:"statics/stock/stocklist.png"}})],1),a("q-fab-action",{style:{"margin-top":t.fab7.top,"margin-bottom":t.fab7.bottom,"margin-left":t.fab7.left,"margin-right":t.fab7.right,height:t.touchheight,width:t.touchwidth},attrs:{square:"",flat:"","external-label":"","label-position":"bottom","label-class":"text-black",label:t.$t("scan.scan_goodsquery"),"label-style":"background-color:transparent",to:{name:"zebra_goodslist"}}},[a("q-img",{attrs:{src:"statics/goods/goodslist.png"}})],1),a("q-fab-action",{style:{"margin-top":t.fab6.top,"margin-bottom":t.fab6.bottom,"margin-left":t.fab6.left,"margin-right":t.fab6.right,height:t.touchheight,width:t.touchwidth},attrs:{square:"",flat:"","external-label":"","label-position":"bottom","label-class":"text-black",icon:"img:statics/stock/cyclecount.png",label:t.$t("scan.scan_inventory"),"label-style":"background-color:transparent",to:{name:"zebra_cyclecount"}}},[a("q-img",{attrs:{src:"statics/stock/cyclecount.png"}})],1),a("q-fab-action",{style:{"margin-top":t.fab5.top,"margin-bottom":t.fab5.bottom,"margin-left":t.fab5.left,"margin-right":t.fab5.right,height:t.touchheight,width:t.touchwidth},attrs:{square:"",flat:"","external-label":"","label-position":"bottom","label-class":"text-black",label:t.$t("scan.scan_movetobin"),"label-style":"background-color:transparent",to:{name:"zebra_movetobin"}}},[a("q-img",{attrs:{src:"statics/icons/movetobin.png"}})],1),a("q-fab-action",{style:{"margin-top":t.fab4.top,"margin-bottom":t.fab4.bottom,"margin-left":t.fab4.left,"margin-right":t.fab4.right,height:t.touchheight,width:t.touchwidth},attrs:{square:"",flat:"","external-label":"","label-position":"bottom","label-class":"text-black",label:t.$t("scan.scan_shipping"),"label-style":"background-color:transparent",to:{name:"zebra_shipping"}}},[a("q-img",{attrs:{src:"statics/icons/car.png"}})],1),a("q-fab-action",{style:{"margin-top":t.fab3.top,"margin-bottom":t.fab3.bottom,"margin-left":t.fab3.left,"margin-right":t.fab3.right,height:t.touchheight,width:t.touchwidth},attrs:{square:"",flat:"","external-label":"","label-position":"bottom","label-class":"text-black",label:t.$t("scan.scan_picking"),"label-style":"background-color:transparent",to:{name:"zebra_picking"}}},[a("q-img",{attrs:{src:"statics/outbound/picked.png"}})],1),a("q-fab-action",{style:{"margin-top":t.fab2.top,"margin-bottom":t.fab2.bottom,"margin-left":t.fab2.left,"margin-right":t.fab2.right,height:t.touchheight,width:t.touchwidth},attrs:{square:"",flat:"","external-label":"","label-position":"bottom","label-class":"text-black",label:t.$t("scan.scan_uptobin"),"label-style":"background-color:transparent",to:{name:"zebra_uptobin"}}},[a("q-img",{attrs:{src:"statics/inbound/presortstock.png"}})],1),a("q-fab-action",{style:{"margin-top":t.fab1.top,"margin-bottom":t.fab1.bottom,"margin-left":t.fab1.left,"margin-right":t.fab1.right,height:t.touchheight,width:t.touchwidth},attrs:{square:"",flat:"","external-label":"","label-position":"bottom","label-class":"text-black",label:t.$t("scan.scan_sorting"),"label-style":"background-color:transparent",to:{name:"zebra_sorting"}}},[a("q-img",{attrs:{src:"statics/inbound/preloadstock.png"}})],1)],1)],1)],1)},n=[],i=e("3004"),s=e("18d6"),r=e("09f9"),l=e("e302"),c="false",b={initialize:function(){this.bindEvents()},bindEvents:function(){document.addEventListener("deviceready",this.onDeviceReady,!1)},onDeviceReady:function(){b.receivedEvent("deviceready"),console.log(0,window.Media),m(),d()},onPause:function(){console.log("Paused"),f()},onResume:function(){console.log("Resumed"),m()},receivedEvent:function(t){console.log("Received Event: "+t)}};function d(){g("com.symbol.datawedge.api.GET_VERSION_INFO","")}function g(t,a){console.log("Sending Command: "+t+", "+JSON.stringify(a));var e={};e[t]=a,e.SEND_RESULT=c,window.plugins.intentShim.sendBroadcast({action:"com.symbol.datawedge.api.ACTION",extras:e},(function(){}),(function(){}))}function m(){window.plugins.intentShim.registerBroadcastReceiver({filterActions:["com.zebra.cordovademo.ACTION","com.symbol.datawedge.api.RESULT_ACTION"],filterCategories:["android.intent.category.DEFAULT"]},(function(t){if(console.log("Received Intent: "+JSON.stringify(t.extras)),t.extras.hasOwnProperty("RESULT_INFO")){var a=t.extras.RESULT+" ("+t.extras.COMMAND.substring(t.extras.COMMAND.lastIndexOf(".")+1,t.extras.COMMAND.length)+")";E(a.toLowerCase())}if(t.extras.hasOwnProperty("com.symbol.datawedge.api.RESULT_GET_VERSION_INFO")){var e=t.extras["com.symbol.datawedge.api.RESULT_GET_VERSION_INFO"];console.log("Version Info: "+JSON.stringify(e));var o=e.DATAWEDGE;o=o.padStart(5,"0"),console.log("Datawedge version: "+o),o>="006.3"&&h(),o>="006.4"&&p(),o>="006.5"&&u()}else if(t.extras.hasOwnProperty("com.symbol.datawedge.api.RESULT_ENUMERATE_SCANNERS")){var n=t.extras["com.symbol.datawedge.api.RESULT_ENUMERATE_SCANNERS"];w(n)}else if(t.extras.hasOwnProperty("com.symbol.datawedge.api.RESULT_GET_ACTIVE_PROFILE")){var i=t.extras["com.symbol.datawedge.api.RESULT_GET_ACTIVE_PROFILE"];_(i)}else t.extras.hasOwnProperty("RESULT_INFO")||x(t,(new Date).toLocaleString())}))}function f(){window.plugins.intentShim.unregisterBroadcastReceiver()}function h(){console.log("Datawedge 6.3 APIs are available"),g("com.symbol.datawedge.api.CREATE_PROFILE","ZebraCordovaDemo"),g("com.symbol.datawedge.api.GET_ACTIVE_PROFILE",""),g("com.symbol.datawedge.api.ENUMERATE_SCANNERS","")}function p(){console.log("Datawedge 6.4 APIs are available");var t={PROFILE_NAME:"wms",PROFILE_ENABLED:"true",CONFIG_MODE:"UPDATE",PLUGIN_CONFIG:{PLUGIN_NAME:"BARCODE",RESET_CONFIG:"true",PARAM_LIST:{}},APP_LIST:[{PACKAGE_NAME:"org.greaterwms.app",ACTIVITY_LIST:["*"]}]};g("com.symbol.datawedge.api.SET_CONFIG",t);var a={PROFILE_NAME:"wms",PROFILE_ENABLED:"true",CONFIG_MODE:"UPDATE",PLUGIN_CONFIG:{PLUGIN_NAME:"INTENT",RESET_CONFIG:"true",PARAM_LIST:{intent_output_enabled:"true",intent_action:"com.zebra.cordovademo.ACTION",intent_delivery:"2"}}};g("com.symbol.datawedge.api.SET_CONFIG",a),setTimeout((function(){g("com.symbol.datawedge.api.GET_ACTIVE_PROFILE","")}),1e3)}function u(){console.log("Datawedge 6.5 APIs are available"),c="true"}function E(t){console.log("commandReceived:",t)}function w(t){for(var a="",e=0;e<t.length;e++)console.log("Scanner found: name= "+t[e].SCANNER_NAME+", id="+t[e].SCANNER_INDEX+", connected="+t[e].SCANNER_CONNECTION_STATE),a+=t[e].SCANNER_NAME,e<t.length-1&&(a+=", ");console.log("enumerateScanners:",a)}function _(t){console.log("activeProfile:",t)}function x(t,a){var e=t.extras["com.symbol.datawedge.data_string"];console.log("scaned Data:"+e),document.getElementById("scannedBarcodes").value="",document.getElementById("scannedBarcodes").value=e,document.getElementById("scannedBarcodes").dispatchEvent(new Event("input"))}function v(){navigator.notification.beep(1)}b.initialize();var y={name:"Pagezebra_scanbase",data(){return{openid:"",login_name:"",authin:"0",pathname:"scan/",separator:"cell",loading:!1,width:"",height:"",scroll_height:"",table_list:[],thumbStyle:{right:"4px",borderRadius:"5px",backgroundColor:"#E0E0E0",width:"5px",opacity:.75},barStyle:{right:"2px",borderRadius:"9px",backgroundColor:"#EEEEEE",width:"9px",opacity:.2},touchheight:(r["a"].width-50)/5+"px",touchwidth:(r["a"].width-50)/5+"px",fab1:{top:"",bottom:"",left:"",right:""},fab2:{top:"",bottom:"",left:"",right:""},fab3:{top:"",bottom:"",left:"",right:""},fab4:{top:"",bottom:"",left:"",right:""},fab5:{top:"",bottom:"",left:"",right:""},fab6:{top:"",bottom:"",left:"",right:""},fab7:{top:"",bottom:"",left:"",right:""},fab8:{top:"",bottom:"",left:"",right:""}}},methods:{datachange(t){var a=this;""!==a.barscan&&Object(i["k"])("scanner/list/"+t+"/",{}).then((t=>{t.detail?(navigator.vibrate(100),a.$q.notify({message:t.detail,position:"top",icon:"close",color:"negative"})):(v(),a.scaneddata=t)})).catch((t=>{navigator.vibrate(100),console.log(t),a.$q.notify({message:t.detail,position:"top",icon:"close",color:"negative"})}))}},computed:{fab:{get(){return this.$store.state.fabchange.fab},set(t){this.$store.commit("bardata/barScanned",""),this.$store.commit("scanedsolve/scanedData",""),this.$store.commit("fabchange/fabChanged",t)}},barscan:{get(){return this.$store.state.bardata.barscan},set(t){this.$store.commit("bardata/barScanned",""),this.$store.commit("bardata/barScanned",t),this.datachange(t)}},scaneddata:{get(){return this.$store.state.scanedsolve.scaneddata},set(t){this.$store.commit("scanedsolve/scanedData",""),this.$store.commit("scanedsolve/scanedData",t)}}},created(){var t=this;s["a"].has("openid")?t.openid=s["a"].getItem("openid"):(t.openid="",s["a"].set("openid","")),s["a"].has("login_name")?t.login_name=s["a"].getItem("login_name"):(t.login_name="",s["a"].set("login_name","")),s["a"].has("auth")?t.authin="1":t.authin="0",t.datachange=Object(l["a"])(t.datachange,200)},mounted(){var t=this;window.plugins.insomnia.keepAwake(),t.fab1.top="0px",t.fab1.bottom=0-(r["a"].width-50)/5+"px",t.fab1.left=(r["a"].width-50)/6-r["a"].width/12*10+"px",t.fab1.right="0px",t.fab2.top="0px",t.fab2.bottom=0-(r["a"].width-50)/5+"px",t.fab2.left=((r["a"].width-50)/6-r["a"].width/12*10)/2+"px",t.fab2.right="0px",t.fab3.top="0px",t.fab3.bottom="0px",t.fab3.left="-0px",t.fab3.right="0px",t.fab4.top=(r["a"].width-50)/5+"px",t.fab4.bottom=0-(r["a"].width-50)/5+"px",t.fab4.left=(r["a"].width-50)/6-r["a"].width/12*10+"px",t.fab4.right="0px",t.fab5.top="0px",t.fab5.bottom=0-(r["a"].width-50)/5+"px",t.fab5.left=((r["a"].width-50)/6-r["a"].width/12*10)/2+"px",t.fab5.right="0px",t.fab6.top="0px",t.fab6.bottom="0px",t.fab6.left="0px",t.fab6.right="0px",t.fab7.top=(r["a"].width-50)/5+"px",t.fab7.bottom=0-(r["a"].width-50)/5+"px",t.fab7.left=(r["a"].width-50)/6-r["a"].width/12*10+"px",t.fab7.right="0px",t.fab8.top="0px",t.fab8.bottom=(r["a"].width-50)/8+"px",t.fab8.left=((r["a"].width-50)/6-r["a"].width/12*10)/2+"px",t.fab8.right="0px",t.barscan=""},beforeDestroy(){window.removeEventListener("deviceready",b.onDeviceReady,!1)},destroyed(){}},N=y,I=e("42e1"),A=e("9989"),R=e("de5e"),S=e("c294"),T=e("72db"),O=e("068f"),C=e("eebe"),k=e.n(C),L=Object(I["a"])(N,o,n,!1,null,null,null);a["default"]=L.exports;k()(L,"components",{QPage:A["a"],QPageSticky:R["a"],QFab:S["a"],QFabAction:T["a"],QImg:O["a"]})}}]);