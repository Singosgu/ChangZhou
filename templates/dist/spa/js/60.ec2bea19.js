(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[60],{"4e97":function(e,t,a){"use strict";var n=a("a3cd"),i=a.n(n);t["default"]=i.a},"5e2a":function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e._self._c;return t("div",[t("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[t("q-table",{staticClass:"my-sticky-header-table shadow-24",attrs:{data:e.table_list,"row-key":"id",separator:e.separator,loading:e.loading,filter:e.filter,columns:e.columns,"hide-bottom":"",pagination:e.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:e.height},flat:"",bordered:""},on:{"update:pagination":function(t){e.pagination=t}},scopedSlots:e._u([{key:"top",fn:function(){return[t("q-btn-group",{attrs:{push:""}},[t("q-btn",{attrs:{label:e.$t("refresh"),icon:"refresh"},on:{click:function(t){return e.reFresh()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v("\n             "+e._s(e.$t("refreshtip"))+"\n           ")])],1)],1)]},proxy:!0},{key:"body",fn:function(a){return[t("q-tr",{attrs:{props:a}},[t("q-td",{key:"txnid",attrs:{props:a}},[e._v("\n             "+e._s(a.row.txnid)+"\n           ")]),t("q-td",{key:"trackingnumber",attrs:{props:a}},[e._v("\n           "+e._s(a.row.trackingnumber)+"\n         ")]),t("q-td",{key:"creater",attrs:{props:a}},[e._v("\n           "+e._s(a.row.creater)+"\n         ")]),t("q-td",{key:"create_time",attrs:{props:a}},[e._v("\n           "+e._s(a.row.create_time)+"\n         ")]),t("q-td",{key:"update_time",attrs:{props:a}},[e._v("\n           "+e._s(a.row.update_time)+"\n         ")])],1)]}}])})],1),[t("div",{staticClass:"q-pa-lg flex flex-center"},[t("q-pagination",{directives:[{name:"show",rawName:"v-show",value:0!==e.page_count,expression:"page_count!==0"}],attrs:{color:"purple",max:Math.ceil(e.page_count/5e3),"max-pages":5e3,"boundary-numbers":"","direction-links":""},on:{click:function(t){return e.getList()}},model:{value:e.current,callback:function(t){e.current=t},expression:"current"}}),t("q-btn",{directives:[{name:"show",rawName:"v-show",value:0===e.page_count,expression:"page_count===0"}],attrs:{flat:"",push:"",color:"dark",label:e.$t("no_data")}})],1)]],2)},i=[],s=a("3004"),o=a("bc3a"),r=a.n(o),l={name:"Pagednprepick",data(){return{current:1,page_count:0,openid:"",login_name:"",authin:"0",pathname:"dn/pickingsumfilter/",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],bin_size_list:[],bin_property_list:[],warehouse_list:[],columns:[{name:"txnid",required:!0,label:"TxnId",align:"left",field:"txnid"},{name:"trackingnumber",required:!0,label:"面单号",align:"center",field:"trackingnumber"},{name:"creater",label:this.$t("creater"),field:"creater",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"center"}],filter:"",pagination:{page:1,rowsPerPage:"10000"},scanData:[],resData:"",resMode:"",scan_detail:[]}},methods:{getList(e){var t=this;t.$q.localStorage.has("auth")&&Object(s["e"])(t.pathname+"?page="+this.current+"&order_line=2&dn_code="+e+"&max_page=10000&picking_status=1",{}).then((e=>{t.page_count=e.count,t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListPrevious(){var e=this;e.$q.localStorage.has("auth")&&Object(s["e"])(e.pathname_previous,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getListNext(){var e=this;e.$q.localStorage.has("auth")&&Object(s["e"])(e.pathname_next,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getScanData(e){r.a.get("scanner/list/"+e+"/",{headers:{"Content-Type":'application/json, charset="utf-8"',token:this.$q.localStorage.getItem("openid"),language:this.$q.localStorage.getItem("lang"),operator:this.$q.localStorage.getItem("login_id")}}).then((t=>{t.data.detail||(this.resData=t.data.code,this.resMode=t.data.mode,"PSUM"===this.resMode?this.getList(this.resData):"MD"===this.resMode?this.MDConfirm(this.resData):this.$q.notify({message:e+"编码不存在",icon:"close",color:"negative"}))})).catch((e=>{this.$q.notify({type:"negative",message:e.detail})}))},submitRes(e){const t={creater:this.login_name,customer:e.customer,dn_code:e.dn_code,goodsData:this.scan_detail};Object(s["j"])("dn/picked/"+e.id+"/",t,{}).then((t=>{t.detail||(this.scan_detail=[],Object(s["i"])("http://127.0.0.1:8008/print/"+this.$q.localStorage.getItem("printer")+"/"+e.txnid+"/",{data:e.mian_dan}).then((e=>{this.$q.notify({message:"面单打印成功"})})),this.$q.notify({message:this.$t("拣货成功")})),this.InitData("")})).catch((e=>{this.$q.notify({message:this.$t("notice.network_error")})}))},MDConfirm(e){Object(s["e"])("dn/list/?trackingnumber="+e).then((e=>{e.results.length>0?4===e.results[0].dn_status?Object(s["i"])("dn/dispatch/"+e.results[0].id+"/",e.results[0]).then((e=>{this.$q.notify({message:"发货成功",icon:"check",color:"green"})})):this.$q.notify({message:"订单已完成，或者还未到发货环节",icon:"close",color:"negative"}):this.$q.notify({message:"面单不存在",icon:"close",color:"negative"})}))},reFresh(){var e=this;e.getList("")},KeyDown(e){"Enter"===e.key||13===e.keyCode?(this.getScanData(this.scanData.join("")),this.scanData=[]):"Shift"===e.key||16===e.keyCode||"Tab"===e.key||9===e.keyCode||this.scanData.push(e.key)},InitData(){this.submitForm=!1}},created(){var e=this;e.$q.localStorage.has("openid")?e.openid=e.$q.localStorage.getItem("openid"):(e.openid="",e.$q.localStorage.set("openid","")),e.$q.localStorage.has("login_name")?e.login_name=e.$q.localStorage.getItem("login_name"):(e.login_name="",e.$q.localStorage.set("login_name","")),e.$q.localStorage.has("auth")?(e.authin="1",e.getList("")):e.authin="0"},mounted(){var e=this;e.$q.platform.is.electron?e.height=String(e.$q.screen.height-290)+"px":e.height=e.$q.screen.height-290+"px",window.addEventListener("keydown",this.KeyDown,!0)},updated(){},destroyed(){}},c=l,d=a("42e1"),h=a("4e97"),p=a("eaac"),g=a("e7a9"),u=a("9c40"),m=a("05c0"),_=a("bd08"),b=a("db86"),f=a("3b16"),q=a("eebe"),v=a.n(q),y=Object(d["a"])(c,n,i,!1,null,null,null);"function"===typeof h["default"]&&Object(h["default"])(y);t["default"]=y.exports;v()(y,"components",{QTable:p["a"],QBtnGroup:g["a"],QBtn:u["a"],QTooltip:m["a"],QTr:_["a"],QTd:b["a"],QPagination:f["a"]})},a3cd:function(e,t){}}]);