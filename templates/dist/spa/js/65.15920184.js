(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[65],{"24a4":function(t,e){},"9d6c":function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t._self._c;return e("div",[e("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[e("q-table",{staticClass:"my-sticky-header-column-table shadow-24",attrs:{id:"table",data:t.table_list,"row-key":"id",separator:t.separator,loading:t.loading,columns:t.columns,"hide-bottom":"",pagination:t.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:t.height},flat:"",bordered:""},on:{"update:pagination":function(e){t.pagination=e}},scopedSlots:t._u([{key:"top",fn:function(){return[e("q-btn-group",{attrs:{push:""}},[e("q-btn",{attrs:{label:t.$t("refresh"),icon:"refresh"},on:{click:function(e){return t.reFresh()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v(t._s(t.$t("refreshtip")))])],1)],1)]},proxy:!0},{key:"body",fn:function(a){return[e("q-tr",{attrs:{props:a}},[e("q-td",{key:"staff_name",attrs:{props:a}},[t._v(t._s(a.row.staff_name))]),e("q-td",{key:"update_time",attrs:{props:a}},[t._v(t._s(a.row.update_time))]),[e("q-td",{key:"action",staticStyle:{width:"50px"},attrs:{props:a}},[e("q-btn",{attrs:{round:"",flat:"",push:"",color:"black",icon:"download"},on:{click:function(e){return t.downloadPickingList(a.row)}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n                    下载这个仓管员的拣货单\n                  ")])],1)],1)]],2)]}}])})],1),[e("div",{staticClass:"q-pa-lg flex flex-center"},[e("q-btn",{directives:[{name:"show",rawName:"v-show",value:t.pathname_previous,expression:"pathname_previous"}],attrs:{flat:"",push:"",color:"purple",label:t.$t("previous"),icon:"navigate_before"},on:{click:function(e){return t.getListPrevious()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v(t._s(t.$t("previous")))])],1),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:t.pathname_next,expression:"pathname_next"}],attrs:{flat:"",push:"",color:"purple",label:t.$t("next"),"icon-right":"navigate_next"},on:{click:function(e){return t.getListNext()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v(t._s(t.$t("next")))])],1),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:!t.pathname_previous&&!t.pathname_next,expression:"!pathname_previous && !pathname_next"}],attrs:{flat:"",push:"",color:"dark",label:t.$t("no_data")}})],1)]],2)},n=[],o=(a("5319"),a("3004")),i=a("bd4c"),f=a("a357"),r=a("18d6"),p={name:"Pagestafflist",data(){return{openid:"",login_name:"",authin:"0",pathname:"staff/?picking_task=1",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],staff_type_list:[],columns:[{name:"staff_name",required:!0,label:this.$t("staff.view_staff.staff_name"),align:"left",field:"staff_name"},{name:"update_time",label:this.$t("createtime"),field:"update_time",align:"center"},{name:"action",label:this.$t("action"),align:"right"}],pagination:{page:1,rowsPerPage:"30"}}},methods:{getList(){var t=this;Object(o["e"])(t.pathname,{}).then((e=>{t.table_list=e.results,"zh-hans"===r["a"].getItem("lang")&&t.table_list.forEach(((t,e)=>{"Admin"===t.staff_type?t.staff_type="管理员":"Customer"===t.staff_type?t.staff_type="客户":"Supplier"===t.staff_type?t.staff_type="供应商":"Manager"===t.staff_type?t.staff_type="经理":"Supervisor"===t.staff_type?t.staff_type="主管":"Inbound"===t.staff_type?t.staff_type="收货组":"Outbound"===t.staff_type?t.staff_type="发货组":"StockControl"===t.staff_type&&(t.staff_type="库存管理")})),t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getSearchList(){var t=this;t.filter=t.filter.replace(/\s+/g,""),Object(o["e"])(t.pathname+"?staff_name__icontains="+t.filter,{}).then((e=>{t.table_list=e.results,"zh-hans"===r["a"].getItem("lang")&&t.table_list.forEach(((t,e)=>{"Admin"===t.staff_type?t.staff_type="管理员":"Customer"===t.staff_type?t.staff_type="客户":"Supplier"===t.staff_type?t.staff_type="供应商":"Manager"===t.staff_type?t.staff_type="经理":"Supervisor"===t.staff_type?t.staff_type="主管":"Inbound"===t.staff_type?t.staff_type="收货组":"Outbound"===t.staff_type?t.staff_type="发货组":"StockControl"===t.staff_type&&(t.staff_type="库存管理")})),t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListPrevious(){var t=this;Object(o["e"])(t.pathname_previous,{}).then((e=>{t.table_list=e.results,"zh-hans"===r["a"].getItem("lang")&&t.table_list.forEach(((t,e)=>{"Admin"===t.staff_type?t.staff_type="管理员":"Customer"===t.staff_type?t.staff_type="客户":"Supplier"===t.staff_type?t.staff_type="供应商":"Manager"===t.staff_type?t.staff_type="经理":"Supervisor"===t.staff_type?t.staff_type="主管":"Inbound"===t.staff_type?t.staff_type="收货组":"Outbound"===t.staff_type?t.staff_type="发货组":"StockControl"===t.staff_type&&(t.staff_type="库存管理")})),t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListNext(){var t=this;Object(o["e"])(t.pathname_next,{}).then((e=>{t.table_list=e.results,"zh-hans"===r["a"].getItem("lang")&&t.table_list.forEach(((t,e)=>{"Admin"===t.staff_type?t.staff_type="管理员":"Customer"===t.staff_type?t.staff_type="客户":"Supplier"===t.staff_type?t.staff_type="供应商":"Manager"===t.staff_type?t.staff_type="经理":"Supervisor"===t.staff_type?t.staff_type="主管":"Inbound"===t.staff_type?t.staff_type="收货组":"Outbound"===t.staff_type?t.staff_type="发货组":"StockControl"===t.staff_type&&(t.staff_type="库存管理")})),t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},reFresh(){var t=this;t.getList()},downloadPickingList(t){var e=this;r["a"].has("auth")?Object(o["f"])(o["b"]+"dn/picklistdownload/?lang="+r["a"].getItem("lang")+"&picker="+t.staff_name+"&picking_status=1&order_line=1",{}).then((t=>{var e=Date.now(),a=i["b"].formatDate(e,"YYYYMMDDHHmmssSSS");const s=Object(f["a"])("pickinglist"+a+".csv","\ufeff"+t.data,"text/csv");!0!==s&&this.$q.notify({message:"Browser denied file download...",color:"negative",icon:"warning"})})):e.$q.notify({message:e.$t("notice.loginerror"),color:"negative",icon:"warning"})}},created(){var t=this;r["a"].has("openid")?t.openid=r["a"].getItem("openid"):(t.openid="",r["a"].set("openid","")),r["a"].has("login_name")?t.login_name=r["a"].getItem("login_name"):(t.login_name="",r["a"].set("login_name","")),r["a"].has("auth")?(t.authin="1",t.getList()):t.authin="0"},mounted(){var t=this;t.$q.platform.is.electron?t.height=String(t.$q.screen.height-290)+"px":t.height=t.$q.screen.height-290+"px","zh-hans"===r["a"].getItem("lang")?t.staff_type_list=["经理","主管","收货组","发货组","库存控制","客户","供应商"]:t.staff_type_list=["Manager","Supervisor","Inbount","Outbound","StockControl","Customer","Supplier"]},updated(){},destroyed(){}},l=p,_=a("42e1"),c=a("be9e"),u=a("eaac"),h=a("e7a9"),d=a("9c40"),m=a("05c0"),y=a("bd08"),g=a("db86"),b=a("eebe"),v=a.n(b),x=Object(_["a"])(l,s,n,!1,null,null,null);"function"===typeof c["default"]&&Object(c["default"])(x);e["default"]=x.exports;v()(x,"components",{QTable:u["a"],QBtnGroup:h["a"],QBtn:d["a"],QTooltip:m["a"],QTr:y["a"],QTd:g["a"]})},be9e:function(t,e,a){"use strict";var s=a("24a4"),n=a.n(s);e["default"]=n.a}}]);