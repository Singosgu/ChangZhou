(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[68],{"12ec":function(e,t,a){"use strict";var i=a("4a88"),n=a.n(i);t["default"]=n.a},"37de":function(e,t,a){"use strict";a.r(t);var i=function(){var e=this,t=e._self._c;return t("div",[[t("div",{staticClass:"q-pa-lg flex flex-center"},[t("q-input",{staticStyle:{width:"400px"},attrs:{filled:"",disable:"",readonly:"",label:"面单号"},model:{value:e.miandan,callback:function(t){e.miandan=t},expression:"miandan"}}),t("input",{directives:[{name:"model",rawName:"v-model",value:e.scan_miandan,expression:"scan_miandan"}],attrs:{type:"hidden"},domProps:{value:e.scan_miandan},on:{input:function(t){t.target.composing||(e.scan_miandan=t.target.value)}}})],1)]],2)},n=[],s=(a("d9e2"),a("3004")),o={name:"Pagednprepick",data(){return{current:1,page_count:0,openid:"",login_name:"",authin:"0",pathname:"dn/pickinglistfilter/",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],bin_size_list:[],bin_property_list:[],warehouse_list:[],columns:[{name:"txnid",required:!0,label:"TxnId",align:"left",field:"txnid"},{name:"bin_name",label:this.$t("warehouse.view_binset.bin_name"),field:"bin_name",align:"center"},{name:"goods_code",label:this.$t("goods.view_goodslist.goods_code"),field:"goods_code",align:"center"},{name:"pick_qty",label:this.$t("stock.view_stocklist.pick_stock"),field:"pick_qty",align:"center"},{name:"picked_qty",label:this.$t("stock.view_stocklist.picked_stock"),field:"picked_qty",align:"center"},{name:"creater",label:this.$t("creater"),field:"creater",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"center"}],filter:"",pagination:{page:1,rowsPerPage:"5000"},scanData:[],resData:"",resMode:"",submitForm:!1,scan_detail:[],miandan:"",scan_miandan:""}},methods:{getList(e){var t=this;t.$q.localStorage.has("auth")&&Object(s["e"])(t.pathname+"?order_line=1&page="+this.current+"&dn_code="+e+"&max_page=5000&picking_status=0",{}).then((e=>{t.page_count=e.count,t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getSearchList(){var e=this;e.$q.localStorage.has("auth")&&Object(s["e"])(e.pathname+"?dn_code__icontains="+e.filter+"&page="+this.current,{}).then((t=>{e.page_count=t.count,e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getListPrevious(){var e=this;e.$q.localStorage.has("auth")&&Object(s["e"])(e.pathname_previous,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getListNext(){var e=this;e.$q.localStorage.has("auth")&&Object(s["e"])(e.pathname_next,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},confirmData(){this.submitForm=!0},getScanData(e){var t=this;t.miandan=e,Object(s["e"])("scanner/list/"+e+"/",{}).then((t=>{t.detail||(this.resData=t.code,this.resMode=t.mode,"MD"===this.resMode?this.MDConfirm():this.$q.notify({message:e+"编码不存在",icon:"close",color:"negative"}))})).catch((e=>{console.log(e)}))},MDConfirm(){Object(s["e"])("dn/list/?trackingnumber="+this.miandan).then((e=>{e.results.length>0?4===e.results[0].dn_status?postauth("dn/dispatch/"+e.results[0].id+"/",e.results[0]).then((e=>{this.$q.notify({message:"发货成功",icon:"check",color:"green"})})):this.$q.notify({message:"订单已完成，或者还未到发货环节",icon:"close",color:"negative"}):this.$q.notify({message:"面单不存在",icon:"close",color:"negative"})}))},PickChange(){try{this.table_list.forEach(((e,t)=>{if(e.goods_code===this.resData){if(e.pick_qty>0)throw e.picked_qty+=1,e.pick_qty-=1,this.scan_detail.splice(t+1,1),this.table_list.unshift(e),this.table_list.splice(t+1,1),this.submitRes(e),new Error("success");t+1===this.table_list.length&&this.$q.notify({type:"negative",icon:"close",message:"Can Not Pick More"})}}))}catch(e){console.log(e)}finally{console.log("error")}},submitData(){var e=this.table_list[0].dn_code;Object(s["e"])("dn/list/?dn_code="+e,{}).then((e=>{e.detail?this.$q.notify({type:"negative",icon:"close",message:this.$t("notice.mobile_scan.notice1")}):this.submitRes(e.results[0])})).catch((e=>{this.$q.notify({type:"negative",icon:"close",message:this.$t("notice.mobile_scan.notice3")})}))},submitRes(e){const t={creater:this.login_name,customer:e.customer,dn_code:e.dn_code,goodsData:this.scan_detail};Object(s["j"])("dn/picked/"+e.id+"/",t,{}).then((t=>{t.detail||(this.scan_detail=[],Object(s["e"])("http://127.0.0.1:8008/print/"+this.$q.localStorage.getItem("printer")+"/"+e.txnid+"/",{}).then((e=>{this.$q.notify({message:"面单打印成功"})})),this.$q.notify({message:this.$t("拣货成功")})),this.InitData("")})).catch((e=>{this.$q.notify({message:this.$t("notice.network_error")})}))},reFresh(){var e=this;e.getList("")},KeyDown(e){console.log(e.key,e.keyCode),"Enter"===e.key||13===e.keyCode?(this.getScanData(this.scanData.join("")),this.scanData=[]):"Shift"===e.key||16===e.keyCode||"Tab"===e.key||9===e.keyCode||this.scanData.push(e.key)},InitData(){this.submitForm=!1}},created(){var e=this;e.$q.localStorage.has("openid")?e.openid=e.$q.localStorage.getItem("openid"):(e.openid="",e.$q.localStorage.set("openid","")),e.$q.localStorage.has("login_name")?e.login_name=e.$q.localStorage.getItem("login_name"):(e.login_name="",e.$q.localStorage.set("login_name","")),e.$q.localStorage.has("auth")?(e.authin="1",e.getList("")):e.authin="0"},mounted(){var e=this;e.$q.platform.is.electron?e.height=String(e.$q.screen.height-290)+"px":e.height=e.$q.screen.height-290+"px",window.addEventListener("keydown",this.KeyDown,!0)},updated(){},destroyed(){}},c=o,l=a("42e1"),r=a("12ec"),h=a("27f9"),d=a("eebe"),g=a.n(d),m=Object(l["a"])(c,i,n,!1,null,null,null);"function"===typeof r["default"]&&Object(r["default"])(m);t["default"]=m.exports;g()(m,"components",{QInput:h["a"]})},"4a88":function(e,t){}}]);