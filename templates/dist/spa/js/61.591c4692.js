(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[61],{"286c":function(t,e){},"90d5":function(t,e,a){"use strict";var i=a("286c"),r=a.n(i);e["default"]=r.a},"986ad":function(t,e,a){"use strict";a.r(e);var i=function(){var t=this,e=t._self._c;return e("div",[e("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[e("q-table",{staticClass:"my-sticky-header-column-table shadow-24",attrs:{data:t.table_list,"row-key":"id",separator:t.separator,loading:t.loading,filter:t.filter,columns:t.columns,"hide-bottom":"",pagination:t.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:t.height},flat:"",bordered:""},on:{"update:pagination":function(e){t.pagination=e}},scopedSlots:t._u([{key:"top",fn:function(){return[e("q-btn-group",{attrs:{push:""}},[e("q-btn",{attrs:{label:t.$t("refresh"),icon:"refresh"},on:{click:function(e){return t.reFresh()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n                 "+t._s(t.$t("refreshtip"))+"\n               ")])],1),e("q-btn",{attrs:{label:"批量确认订单",icon:"recommend"},on:{click:function(e){return t.confirmOrders()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("批量确认订单\n              ")])],1)],1),e("q-space"),e("div",{staticClass:"row no-wrap"},[e("q-input",{staticClass:"q-field--dense q-field__native",staticStyle:{"padding-right":"20px",width:"200px"},attrs:{outlined:"",label:"TxnId"},model:{value:t.filterData.txnid,callback:function(e){t.$set(t.filterData,"txnid",e)},expression:"filterData.txnid"}}),e("q-select",{staticClass:"q-field__native q-field--dense",staticStyle:{"padding-right":"20px",width:"400px"},attrs:{outlined:"",options:t.order_type_list,label:"发货方式"},model:{value:t.filterData.order_type,callback:function(e){t.$set(t.filterData,"order_type",e)},expression:"filterData.order_type"}}),e("q-select",{staticClass:"q-field__native q-field--dense",staticStyle:{"padding-right":"20px",width:"200px"},attrs:{outlined:"",options:t.order_line_list,label:"订单行"},model:{value:t.filterData.order_line,callback:function(e){t.$set(t.filterData,"order_line",e)},expression:"filterData.order_line"}}),e("q-select",{staticClass:"q-field__native q-field--dense",staticStyle:{"padding-right":"20px",width:"200px"},attrs:{outlined:"",options:t.carrier_list,label:"承运人"},model:{value:t.filterData.carrier,callback:function(e){t.$set(t.filterData,"carrier",e)},expression:"filterData.carrier"}}),e("q-input",{staticClass:"q-field--dense q-field__native",staticStyle:{"padding-right":"20px",width:"200px"},attrs:{outlined:"",label:"SKU"},model:{value:t.filterData.sku,callback:function(e){t.$set(t.filterData,"sku",e)},expression:"filterData.sku"}})],1),e("div",[e("q-btn",{staticStyle:{height:"40px","margin-right":"10px"},attrs:{unelevated:"",color:"primary",label:"查询"},on:{click:function(e){return t.sortData()}}}),e("q-btn",{staticStyle:{height:"40px","margin-right":"10px"},attrs:{unelevated:"",color:"red",label:"重置"},on:{click:function(e){return t.filterDataClear()}}})],1)]},proxy:!0},{key:"body",fn:function(a){return[e("q-tr",{attrs:{props:a}},[e("q-td",{key:"txnid",attrs:{props:a}},[t._v("\n                 "+t._s(a.row.txnid)+"\n               ")]),e("q-td",{key:"order_type",attrs:{props:a}},[t._v("\n                 "+t._s(a.row.order_type)+"\n               ")]),e("q-td",{key:"trackingnumber",attrs:{props:a}},[t._v("\n                 "+t._s(a.row.trackingnumber)+"\n               ")]),e("q-td",{key:"carrier",attrs:{props:a}},[t._v("\n                 "+t._s(a.row.carrier)+"\n               ")]),e("q-td",{key:"goods_code",attrs:{props:a}},[t._v("\n                 "+t._s(a.row.goods_code)+"\n               ")]),e("q-td",{key:"goods_desc",attrs:{props:a}},[t._v("\n                 "+t._s(a.row.goods_desc)+"\n               ")]),e("q-td",{key:"goods_qty",attrs:{props:a}},[t._v("\n                 "+t._s(a.row.goods_qty)+"\n               ")]),e("q-td",{key:"goods_weight",attrs:{props:a}},[t._v("\n                 "+t._s(a.row.goods_weight)+"\n               ")]),e("q-td",{key:"goods_volume",attrs:{props:a}},[t._v("\n               "+t._s(a.row.goods_volume)+"\n             ")]),e("q-td",{key:"customer",attrs:{props:a}},[t._v("\n               "+t._s(a.row.customer)+"\n             ")]),e("q-td",{key:"creater",attrs:{props:a}},[t._v("\n               "+t._s(a.row.creater)+"\n             ")]),e("q-td",{key:"create_time",attrs:{props:a}},[t._v("\n               "+t._s(a.row.create_time)+"\n             ")]),e("q-td",{key:"update_time",attrs:{props:a}},[t._v("\n               "+t._s(a.row.update_time)+"\n             ")])],1)]}}])})],1),[e("div",{staticClass:"q-pa-lg flex flex-center"},[e("q-select",{staticClass:"q-field__native q-field--dense",staticStyle:{width:"100px"},attrs:{outlined:"",options:t.max_page,label:"每页数量"},model:{value:t.max_page_data,callback:function(e){t.max_page_data=e},expression:"max_page_data"}}),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:0===t.page_count,expression:"page_count===0"}],attrs:{flat:"",push:"",color:"dark",label:t.$t("no_data")}}),e("q-pagination",{directives:[{name:"show",rawName:"v-show",value:0!==t.page_count,expression:"page_count!==0"}],attrs:{color:"black",max:Math.ceil(t.page_count/t.max_page_data),"max-pages":5,"boundary-numbers":"","direction-links":""},on:{click:function(e){return t.getList()}},model:{value:t.current,callback:function(e){t.current=e},expression:"current"}}),e("div",{staticStyle:{"margin-left":"20px"}},[t._v(" Total:  "+t._s(t.page_count)+" ")])],1)]],2)},r=[],s=a("3004"),n={name:"Pagednneworder",data(){return{current:1,page_count:0,openid:"",login_name:"",authin:"0",pathname:"dn/detail/?dn_status=1",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",max_page_data:30,max_page:[30,100,500,1e3],table_list:[],bin_size_list:[],bin_property_list:[],warehouse_list:[],columns:[{name:"txnid",required:!0,label:"TxnId",align:"left",field:"txnid"},{name:"order_type",required:!0,label:"Method",align:"left",field:"order_type"},{name:"trackingnumber",required:!0,label:"面单",align:"left",field:"trackingnumber"},{name:"carrier",required:!0,label:"承运人",align:"left",field:"carrier"},{name:"goods_code",label:this.$t("goods.view_goodslist.goods_code"),field:"goods_code",align:"center"},{name:"goods_desc",label:this.$t("goods.view_goodslist.goods_desc"),field:"goods_desc",align:"center"},{name:"goods_qty",label:this.$t("outbound.view_dn.goods_qty"),field:"goods_qty",align:"center"},{name:"goods_weight",label:this.$t("outbound.view_dn.total_weight"),field:"goods_weight",align:"center"},{name:"goods_volume",label:this.$t("outbound.view_dn.total_volume"),field:"empty_label",align:"center"},{name:"customer",label:this.$t("baseinfo.view_customer.customer_name"),field:"customer",align:"center"},{name:"creater",label:this.$t("creater"),field:"creater",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"center"}],filter:"",filterData:{txnid:"",order_type:"",order_line:"",carrier:"",sku:""},pagination:{page:1,rowsPerPage:"1000"},order_type_list:[],order_line_list:["单件","多件"],carrier_list:[],txnid_list_data:[],order_type_data:"",order_line:"",carrier_data:"",sku_list_data:[]}},methods:{filterDataClear(){this.filterData={txnid:[],order_type:"",order_line:"",carrier:"",sku:[]},this.txnid_list_data=[],this.order_type_data="",this.order_line="",this.carrier_data="",this.sku_list_data=[],this.getList()},sortData(){var t=this;this.filterData.txnid.length>0?t.txnid_list_data=this.filterData.txnid.split("\n"):t.txnid_list_data=[],this.filterData.sku.length>0?t.sku_list_data=this.filterData.sku.split("\n"):t.sku_list_data=[],this.order_type_data=this.filterData.order_type,"单件"===this.filterData.order_line?this.order_line=1:this.order_line=2,this.carrier_data=this.filterData.carrier,t.getList()},getList(){var t=this;t.$q.localStorage.has("auth")&&("单件"===this.order_line||1===this.order_line?this.order_line=1:2===this.order_line?this.order_line=2:this.order_line="",Object(s["e"])(t.pathname+"&max_page="+t.max_page_data+"&page="+this.current+"&txnid__in="+this.txnid_list_data+"&order_type="+this.order_type_data+"&carrier="+this.carrier_data+"&order_line="+this.order_line+"&goods_code__in="+this.sku_list_data,{}).then((e=>{t.page_count=e.count,t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next,t.warehouse_list=e.warehouse_list,t.order_type_list=e.order_type_list,t.carrier_list=e.carrier_list})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})})))},confirmOrders(){var t=this;"单件"===this.order_line||1===this.order_line?this.order_line=1:this.order_line=2,Object(s["i"])("dn/confirmorders/?dn_status=1&page="+this.current+"&txnid__in="+this.txnid_list_data+"&order_type="+this.order_type_data+"&carrier="+this.carrier_data+"&order_line="+this.order_line+"&goods_code__in="+this.sku_list_data,{}).then((t=>{this.$q.notify({message:"确认订单完成",color:"green",icon:"check"}),this.getList()})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListPrevious(){var t=this;t.$q.localStorage.has("auth")&&Object(s["e"])(t.pathname_previous,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListNext(){var t=this;t.$q.localStorage.has("auth")&&Object(s["e"])(t.pathname_next,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},reFresh(){var t=this;t.getList()}},created(){var t=this;t.$q.localStorage.has("openid")?t.openid=t.$q.localStorage.getItem("openid"):(t.openid="",t.$q.localStorage.set("openid","")),t.$q.localStorage.has("login_name")?t.login_name=t.$q.localStorage.getItem("login_name"):(t.login_name="",t.$q.localStorage.set("login_name","")),t.$q.localStorage.has("auth")?(t.authin="1",t.filterDataClear()):t.authin="0"},watch:{max_page_data(t){var e=this;e.getList()}},mounted(){var t=this;t.$q.platform.is.electron?t.height=String(t.$q.screen.height-290)+"px":t.height=t.$q.screen.height-290+"px"},updated(){},destroyed(){}},o=n,l=a("42e1"),d=a("90d5"),_=a("eaac"),c=a("e7a9"),p=a("9c40"),h=a("05c0"),u=a("2c91"),g=a("27f9"),f=a("8572"),m=a("ddd8"),b=a("bd08"),v=a("db86"),x=a("3b16"),q=a("eebe"),y=a.n(q),w=Object(l["a"])(o,i,r,!1,null,null,null);"function"===typeof d["default"]&&Object(d["default"])(w);e["default"]=w.exports;y()(w,"components",{QTable:_["a"],QBtnGroup:c["a"],QBtn:p["a"],QTooltip:h["a"],QSpace:u["a"],QInput:g["a"],QField:f["a"],QSelect:m["a"],QTr:b["a"],QTd:v["a"],QPagination:x["a"]})}}]);