(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[60],{"4e97":function(t,e,a){"use strict";var n=a("a3cd"),i=a.n(n);e["default"]=i.a},"5e2a":function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t._self._c;return e("div",[e("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[e("q-table",{staticClass:"my-sticky-header-table shadow-24",attrs:{data:t.table_list,"row-key":"id",separator:t.separator,loading:t.loading,filter:t.filter,columns:t.columns,"hide-bottom":"",pagination:t.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:t.height},flat:"",bordered:""},on:{"update:pagination":function(e){t.pagination=e}},scopedSlots:t._u([{key:"top",fn:function(){return[e("q-btn-group",{attrs:{push:""}},[e("q-btn",{attrs:{label:t.$t("refresh"),icon:"refresh"},on:{click:function(e){return t.reFresh()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n             "+t._s(t.$t("refreshtip"))+"\n           ")])],1)],1)]},proxy:!0},{key:"body",fn:function(a){return[e("q-tr",{attrs:{props:a}},[e("q-td",{key:"txnid",attrs:{props:a}},[t._v("\n             "+t._s(a.row.txnid)+"\n           ")]),e("q-td",{key:"trackingnumber",attrs:{props:a}},[t._v("\n             "+t._s(a.row.trackingnumber)+"\n           ")]),e("q-td",{key:"create_time",attrs:{props:a}},[t._v("\n           "+t._s(a.row.create_time)+"\n         ")]),e("q-td",{key:"update_time",attrs:{props:a}},[t._v("\n           "+t._s(a.row.update_time)+"\n         ")])],1)]}}])})],1),[e("div",{staticClass:"q-pa-lg flex flex-center"},[e("q-pagination",{directives:[{name:"show",rawName:"v-show",value:0!==t.page_count,expression:"page_count!==0"}],attrs:{color:"purple",max:Math.ceil(t.page_count/5e3),"max-pages":5e3,"boundary-numbers":"","direction-links":""},on:{click:function(e){return t.getList()}},model:{value:t.current,callback:function(e){t.current=e},expression:"current"}}),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:0===t.page_count,expression:"page_count===0"}],attrs:{flat:"",push:"",color:"dark",label:t.$t("no_data")}})],1)]],2)},i=[],s=(a("d9e2"),a("3004")),o=a("bc3a"),r=a.n(o),l={name:"Pagednmorepick",data(){return{current:1,page_count:0,openid:"",login_name:"",authin:"0",pathname:"dn/pickingsumfilter/",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],bin_size_list:[],bin_property_list:[],warehouse_list:[],columns:[{name:"txnid",required:!0,label:"TxnId",align:"left",field:"txnid"},{name:"trackingnumber",label:"面单号",field:"trackingnumber",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"center"}],filter:"",pagination:{page:1,rowsPerPage:"5000"},scanData:[],resData:"",resMode:"",scan_detail:[],sendData:{},picking_status_list:[1,2]}},methods:{getList(t){var e=this;e.$q.localStorage.has("auth")&&Object(s["e"])(e.pathname+"?page="+this.current+"&order_line=2&dn_code="+t+"&max_page=10000&picking_status=1",{}).then((t=>{e.page_count=t.count,e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getListPrevious(){var t=this;t.$q.localStorage.has("auth")&&Object(s["e"])(t.pathname_previous,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListNext(){var t=this;t.$q.localStorage.has("auth")&&Object(s["e"])(t.pathname_next,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getScanData(t){r.a.get(s["b"]+"scanner/list/"+t+"/",{headers:{"Content-Type":'application/json, charset="utf-8"',token:"SCANGOODS",language:this.$q.localStorage.getItem("lang"),operator:this.$q.localStorage.getItem("login_id")}}).then((e=>{e.data.detail||(this.resData=e.data.code,this.resMode=e.data.mode,console.log(e),"DN"===this.resMode?this.getList(this.resData):"PSUM"===this.resMode?this.PickChange():"MD"===this.resMode?this.MDConfirm(this.resData):this.$q.notify({message:t+"编码不存在",icon:"close",color:"negative"}))})).catch((t=>{this.$q.notify({type:"negative",message:t.detail})}))},PickChange(){try{this.table_list.forEach(((t,e)=>{if(t.bar_code===this.resData&&1===t.picking_status){if(t.pick_qty>0)throw t.picking_status=2,this.table_list.unshift(t),this.table_list.splice(e+1,1),this.sendData=t,new Error("success");e+1===this.table_list.length&&this.$q.notify({type:"negative",icon:"close",message:"Can Not Pick More"})}}))}catch(t){console.log(t)}finally{console.log("error")}},submitSendData(t){this.scan_detail=[],this.scan_detail.push(t),this.submitRes(t)},submitRes(t){const e={creater:this.login_name,customer:t.customer,dn_code:t.dn_code,goodsData:this.scan_detail};Object(s["i"])("dn/morepicked/"+t.id+"/",e,{}).then((e=>{e.detail||(this.scan_detail=[],Object(s["i"])("http://127.0.0.1:8008/print/"+this.$q.localStorage.getItem("printer")+"/"+t.txnid+"/",{data:t.mian_dan}).then((t=>{this.$q.notify({message:"面单打印成功"})})),this.$q.notify({message:this.$t("拣货成功")})),this.InitData("")})).catch((t=>{this.$q.notify({message:this.$t("notice.network_error")})}))},MDConfirm(t){Object(s["e"])("dn/list/?trackingnumber="+t).then((t=>{t.results.length>0?4===t.results[0].dn_status?Object(s["i"])("dn/dispatch/"+t.results[0].id+"/",t.results[0]).then((t=>{this.getList(""),this.$q.notify({message:"发货成功",icon:"check",color:"green"})})):this.$q.notify({message:"订单已完成，或者还未到发货环节",icon:"close",color:"negative"}):this.$q.notify({message:"面单不存在",icon:"close",color:"negative"})}))},reFresh(){var t=this;t.getList("")},KeyDown(t){"Enter"===t.key||13===t.keyCode?(this.getScanData(this.scanData.join("")),this.scanData=[]):"Shift"===t.key||16===t.keyCode||"Tab"===t.key||9===t.keyCode||this.scanData.push(t.key)},InitData(){this.submitForm=!1}},watch:{sendData(t){var e=this;e.submitSendData(t)}},created(){var t=this;t.$q.localStorage.has("openid")?t.openid=t.$q.localStorage.getItem("openid"):(t.openid="",t.$q.localStorage.set("openid","")),t.$q.localStorage.has("login_name")?t.login_name=t.$q.localStorage.getItem("login_name"):(t.login_name="",t.$q.localStorage.set("login_name","")),t.$q.localStorage.has("auth")?(t.authin="1",t.getList("")):t.authin="0"},mounted(){var t=this;t.$q.platform.is.electron?t.height=String(t.$q.screen.height-290)+"px":t.height=t.$q.screen.height-290+"px",window.addEventListener("keydown",this.KeyDown,!0)},updated(){},destroyed(){}},c=l,h=a("42e1"),d=a("4e97"),g=a("eaac"),p=a("e7a9"),u=a("9c40"),m=a("05c0"),_=a("bd08"),b=a("db86"),f=a("3b16"),y=a("eebe"),k=a.n(y),v=Object(h["a"])(c,n,i,!1,null,null,null);"function"===typeof d["default"]&&Object(d["default"])(v);e["default"]=v.exports;k()(v,"components",{QTable:g["a"],QBtnGroup:p["a"],QBtn:u["a"],QTooltip:m["a"],QTr:_["a"],QTd:b["a"],QPagination:f["a"]})},a3cd:function(t,e){}}]);