(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[61],{"40cd":function(t,e,a){"use strict";var n=a("e20a"),i=a.n(n);e["default"]=i.a},ae50:function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t._self._c;return e("div",[e("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[e("q-table",{staticClass:"my-sticky-header-table shadow-24",attrs:{data:t.table_list,"row-key":"id",separator:t.separator,loading:t.loading,filter:t.filter,columns:t.columns,"hide-bottom":"",pagination:t.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:t.height},flat:"",bordered:""},on:{"update:pagination":function(e){t.pagination=e}},scopedSlots:t._u([{key:"top",fn:function(){return[e("q-btn-group",{attrs:{push:""}},[e("q-btn",{attrs:{label:t.$t("refresh"),icon:"refresh"},on:{click:function(e){return t.reFresh()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n             "+t._s(t.$t("refreshtip"))+"\n           ")])],1),e("q-btn",{attrs:{label:"分配拣货员",icon:"how_to_vote"},on:{click:function(e){return t.allocateStaff()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n             把拣货单分配给拣货员\n           ")])],1)],1),e("q-space"),e("q-input",{attrs:{outlined:"",rounded:"",dense:"",debounce:"300",color:"primary",placeholder:t.$t("search")},on:{blur:function(e){return t.getSearchList()},keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.getSearchList()}},scopedSlots:t._u([{key:"append",fn:function(){return[e("q-icon",{attrs:{name:"search"},on:{click:function(e){return t.getSearchList()}}})]},proxy:!0}]),model:{value:t.filter,callback:function(e){t.filter=e},expression:"filter"}})]},proxy:!0},{key:"body",fn:function(a){return[e("q-tr",{attrs:{props:a}},[e("q-td",{key:"txnid",attrs:{props:a}},[t._v("\n             "+t._s(a.row.txnid)+"\n           ")]),e("q-td",{key:"bin_name",attrs:{props:a}},[t._v("\n             "+t._s(a.row.bin_name)+"\n           ")]),e("q-td",{key:"goods_code",attrs:{props:a}},[t._v("\n             "+t._s(a.row.goods_code)+"\n           ")]),e("q-td",{key:"pick_qty",attrs:{props:a}},[t._v("\n             "+t._s(a.row.pick_qty)+"\n           ")]),e("q-td",{key:"picked_qty",attrs:{props:a}},[t._v("\n           "+t._s(a.row.picked_qty)+"\n         ")]),e("q-td",{key:"creater",attrs:{props:a}},[t._v("\n           "+t._s(a.row.creater)+"\n         ")]),e("q-td",{key:"create_time",attrs:{props:a}},[t._v("\n           "+t._s(a.row.create_time)+"\n         ")]),e("q-td",{key:"update_time",attrs:{props:a}},[t._v("\n           "+t._s(a.row.update_time)+"\n         ")])],1)]}}])})],1),[e("div",{staticClass:"q-pa-lg flex flex-center"},[e("q-pagination",{directives:[{name:"show",rawName:"v-show",value:0!==t.page_count,expression:"page_count!==0"}],attrs:{color:"purple",max:Math.ceil(t.page_count/30),"max-pages":30,"boundary-numbers":"","direction-links":""},on:{click:function(e){return t.getList()}},model:{value:t.current,callback:function(e){t.current=e},expression:"current"}}),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:0===t.page_count,expression:"page_count===0"}],attrs:{flat:"",push:"",color:"dark",label:t.$t("no_data")}})],1)],e("q-dialog",{model:{value:t.allocte_form,callback:function(e){t.allocte_form=e},expression:"allocte_form"}},[e("q-card",{staticClass:"shadow-24"},[e("q-bar",{staticClass:"bg-light-blue-10 text-white rounded-borders",staticStyle:{height:"50px"}},[e("div",[t._v("分配拣货单")]),e("q-space"),e("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{dense:"",flat:"",icon:"close"}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4"}},[t._v(t._s(t.$t("index.close"))+"\n        ")])],1)],1),e("q-card-section",{staticClass:"scroll",staticStyle:{"max-height":"325px",width:"400px"}},[e("q-select",{staticStyle:{"margin-bottom":"5px"},attrs:{filled:"","use-input":"","fill-input":"","hide-selected":"","input-debounce":"0",dense:"",outlined:"",square:"",options:t.bin_list,label:"巷道名称",rules:[t=>t&&t.length>0||"请选择巷道"]},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.allocateSubmit()}},model:{value:t.filter_data.bin_data,callback:function(e){t.$set(t.filter_data,"bin_data",e)},expression:"filter_data.bin_data"}}),e("q-select",{staticStyle:{"margin-bottom":"5px"},attrs:{filled:"","use-input":"","fill-input":"","hide-selected":"","input-debounce":"0",dense:"",outlined:"",square:"",options:t.staff_list,label:"拣货员",rules:[t=>t&&t.length>0||"请选择拣货员"]},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.allocateSubmit()}},model:{value:t.filter_data.staff_name,callback:function(e){t.$set(t.filter_data,"staff_name",e)},expression:"filter_data.staff_name"}})],1),e("div",{staticStyle:{float:"right",padding:"15px 15px 15px 0"}},[e("q-btn",{staticStyle:{"margin-right":"25px"},attrs:{color:"white","text-color":"black"},on:{click:function(e){return t.cancelSubmit()}}},[t._v(t._s(t.$t("cancel"))+"\n      ")]),e("q-btn",{attrs:{color:"primary"},on:{click:function(e){return t.allocateSubmit()}}},[t._v(t._s(t.$t("submit"))+"\n      ")])],1)],1)],1)],2)},i=[],o=a("3004"),s={name:"Pagednonepick",data(){return{current:1,page_count:0,openid:"",login_name:"",authin:"0",pathname:"dn/pickinglistfilter/",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],bin_size_list:[],bin_property_list:[],warehouse_list:[],columns:[{name:"txnid",required:!0,label:"TxnId",align:"left",field:"txnid"},{name:"bin_name",label:this.$t("warehouse.view_binset.bin_name"),field:"bin_name",align:"center"},{name:"goods_code",label:this.$t("goods.view_goodslist.goods_code"),field:"goods_code",align:"center"},{name:"pick_qty",label:this.$t("stock.view_stocklist.pick_stock"),field:"pick_qty",align:"center"},{name:"picked_qty",label:this.$t("stock.view_stocklist.picked_stock"),field:"picked_qty",align:"center"},{name:"creater",label:this.$t("creater"),field:"creater",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"center"}],filter:"",pagination:{page:1,rowsPerPage:"30"},bin_list:[],staff_list:[],allocte_form:!1,filter_data:{bin_data:"",staff_name:""}}},methods:{getList(){var t=this;t.$q.localStorage.has("auth")&&Object(o["e"])(t.pathname+"?page="+this.current+"&picking_status=0&order_line=1",{}).then((e=>{t.page_count=e.count,t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next,t.bin_list=e.bin_list,t.staff_list=e.staff_list})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getSearchList(){var t=this;t.$q.localStorage.has("auth")&&Object(o["e"])(t.pathname+"?txnid__icontains="+t.filter+"&page="+this.current,{}).then((e=>{t.page_count=e.count,t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListPrevious(){var t=this;t.$q.localStorage.has("auth")&&Object(o["e"])(t.pathname_previous,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListNext(){var t=this;t.$q.localStorage.has("auth")&&Object(o["e"])(t.pathname_next,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},reFresh(){var t=this;t.getList()},allocateStaff(){var t=this;t.$q.localStorage.has("auth")?t.allocte_form=!0:t.$q.notify({message:t.$t("no_auth"),icon:"close",color:"negative"})},allocateSubmit(){var t=this;t.$q.localStorage.has("auth")&&(""===t.filter_data.bin_data?t.$q.notify({message:"请选择巷道名称",icon:"close",color:"negative"}):""===t.filter_data.staff_name?t.$q.notify({message:"请选择拣货员",icon:"close",color:"negative"}):t.resSubmit())},cancelSubmit(){var t=this;t.allocte_form=!1,t.filter_data.bin_data="",t.filter_data.staff_name=""},resSubmit(){var t=this;t.$q.localStorage.has("auth")&&Object(o["i"])(o["b"]+"dn/onepicking/?page="+this.current+"&picking_status=0&order_line=1&bin_name__startswith="+t.filter_data.bin_data,t.filter_data).then((e=>{t.cancelSubmit(),t.getList(),t.$q.notify({message:"分配成功",icon:"check",color:"green"})})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))}},created(){var t=this;t.$q.localStorage.has("openid")?t.openid=t.$q.localStorage.getItem("openid"):(t.openid="",t.$q.localStorage.set("openid","")),t.$q.localStorage.has("login_name")?t.login_name=t.$q.localStorage.getItem("login_name"):(t.login_name="",t.$q.localStorage.set("login_name","")),t.$q.localStorage.has("auth")?(t.authin="1",t.getList()):t.authin="0"},mounted(){var t=this;t.$q.platform.is.electron?t.height=String(t.$q.screen.height-290)+"px":t.height=t.$q.screen.height-290+"px"},updated(){},destroyed(){}},l=s,r=a("42e1"),c=a("40cd"),d=a("eaac"),p=a("e7a9"),u=a("9c40"),_=a("05c0"),f=a("2c91"),h=a("27f9"),g=a("0016"),m=a("bd08"),b=a("db86"),v=a("3b16"),k=a("24e8"),q=a("f09f"),y=a("d847"),x=a("a370"),$=a("ddd8"),S=a("7f67"),w=a("eebe"),Q=a.n(w),C=Object(r["a"])(l,n,i,!1,null,null,null);"function"===typeof c["default"]&&Object(c["default"])(C);e["default"]=C.exports;Q()(C,"components",{QTable:d["a"],QBtnGroup:p["a"],QBtn:u["a"],QTooltip:_["a"],QSpace:f["a"],QInput:h["a"],QIcon:g["a"],QTr:m["a"],QTd:b["a"],QPagination:v["a"],QDialog:k["a"],QCard:q["a"],QBar:y["a"],QCardSection:x["a"],QSelect:$["a"]}),Q()(C,"directives",{ClosePopup:S["a"]})},e20a:function(t,e){}}]);