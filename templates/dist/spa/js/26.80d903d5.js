(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[26],{1637:function(t,e){},"239b":function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t._self._c;return e("div",[e("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[e("q-table",{staticClass:"shadow-24",attrs:{data:t.table_list,"row-key":"id",separator:t.separator,loading:t.loading,columns:t.columns,"hide-bottom":"",pagination:t.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:t.height},flat:"",bordered:""},on:{"update:pagination":function(e){t.pagination=e}},scopedSlots:t._u([{key:"top",fn:function(){return[e("div",{staticClass:"flex items-center"},[e("div",{staticClass:"q-mr-md"},[t._v(t._s(t.$t("download_center.createTime")))]),e("q-input",{attrs:{readonly:"",outlined:"",dense:"",placeholder:t.interval},scopedSlots:t._u([{key:"append",fn:function(){return[e("q-icon",{staticClass:"cursor-pointer",attrs:{name:"event"}},[e("q-popup-proxy",{ref:"qDateProxy",attrs:{"transition-show":"scale","transition-hide":"scale"}},[e("q-date",{attrs:{range:""},model:{value:t.createDate1,callback:function(e){t.createDate1=e},expression:"createDate1"}})],1)],1)]},proxy:!0}]),model:{value:t.createDate2,callback:function(e){t.createDate2=e},expression:"createDate2"}}),e("q-btn-group",{staticClass:"q-ml-md",attrs:{push:""}},[e("q-btn",{attrs:{label:t.$t("download_center.reset"),icon:"img:statics/downloadcenter/reset.svg"},on:{click:function(e){return t.reset()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v(t._s(t.$t("download_center.reset")))])],1),e("q-btn",{attrs:{label:t.$t("downloadasnlist"),icon:"cloud_download"},on:{click:function(e){return t.downloadlistData()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v(t._s(t.$t("downloadasnlisttip")))])],1)],1)],1)]},proxy:!0},{key:"body",fn:function(a){return[e("q-tr",{attrs:{props:a}},[e("q-td",{key:"bin_name",attrs:{props:a}},[t._v(t._s(a.row.bin_name))]),e("q-td",{key:"goods_code",attrs:{props:a}},[t._v(t._s(a.row.goods_code))]),e("q-td",{key:"goods_desc",attrs:{props:a}},[t._v(t._s(a.row.goods_desc))]),e("q-td",{key:"goods_qty",attrs:{props:a}},[t._v(t._s(a.row.goods_qty))]),e("q-td",{key:"pick_qty",attrs:{props:a}},[t._v(t._s(a.row.pick_qty))]),e("q-td",{key:"picked_qty",attrs:{props:a}},[t._v(t._s(a.row.picked_qty))]),e("q-td",{key:"bin_size",attrs:{props:a}},[t._v(t._s(a.row.bin_size))]),e("q-td",{key:"bin_property",attrs:{props:a}},[t._v(t._s(a.row.bin_property))]),e("q-td",{key:"create_time",attrs:{props:a}},[t._v(t._s(a.row.create_time))]),e("q-td",{key:"update_time",attrs:{props:a}},[t._v(t._s(a.row.update_time))])],1)]}}])})],1),[e("div",{staticClass:"q-pa-lg flex flex-center"},[e("q-btn",{directives:[{name:"show",rawName:"v-show",value:t.pathname_previous,expression:"pathname_previous"}],attrs:{flat:"",push:"",color:"purple",label:t.$t("previous"),icon:"navigate_before"},on:{click:function(e){return t.getListPrevious()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v(t._s(t.$t("previous")))])],1),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:t.pathname_next,expression:"pathname_next"}],attrs:{flat:"",push:"",color:"purple",label:t.$t("next"),"icon-right":"navigate_next"},on:{click:function(e){return t.getListNext()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v(t._s(t.$t("next")))])],1),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:!t.pathname_previous&&!t.pathname_next,expression:"!pathname_previous && !pathname_next"}],attrs:{flat:"",push:"",color:"dark",label:t.$t("no_data")}})],1)]],2)},n=[],i=(a("5319"),a("3004")),o=a("bd4c"),r=a("a357"),l=(a("a639"),a("18d6")),c={name:"Pageasnlist",data(){return{login_name:"",authin:"0",pathname:"stock/",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],columns:[{name:"bin_name",required:!0,label:this.$t("warehouse.view_binset.bin_name"),align:"left",field:"bin_name"},{name:"goods_code",label:this.$t("stock.view_stocklist.goods_code"),field:"goods_code",align:"center"},{name:"goods_desc",label:this.$t("stock.view_stocklist.goods_desc"),field:"onhand_stock",align:"center"},{name:"goods_qty",label:this.$t("stock.view_stocklist.onhand_stock"),field:"goods_qty",align:"center"},{name:"pick_qty",label:this.$t("stock.view_stocklist.pick_stock"),field:"pick_qty",align:"center"},{name:"picked_qty",label:this.$t("stock.view_stocklist.picked_stock"),field:"picked_qty",align:"center"},{name:"bin_size",label:this.$t("warehouse.view_binset.bin_size"),field:"bin_size",align:"center"},{name:"bin_property",label:this.$t("warehouse.view_binset.bin_property"),field:"bin_property",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"right"}],pagination:{page:1,rowsPerPage:"30"},createDate1:"",createDate2:"",date_range:"",searchUrl:"",downloadhUrl:"stock/filebinlist/"}},computed:{interval(){return this.$t("download_center.start")+" - "+this.$t("download_center.end")}},watch:{createDate1(t){t&&(t.to?(this.createDate2=`${t.from} - ${t.to}`,this.date_range=`${t.from},${t.to} 23:59:59`,this.searchUrl=this.pathname+"bin/?create_time__range="+this.date_range,this.downloadhUrl=this.pathname+"filebinlist/?create_time__range="+this.date_range):(this.createDate2=`${t}`,this.dateArray=t.split("/"),this.searchUrl=this.pathname+"bin/?create_time__year="+this.dateArray[0]+"&create_time__month="+this.dateArray[1]+"&create_time__day="+this.dateArray[2],this.downloadhUrl=this.pathname+"filebinlist/?create_time__year="+this.dateArray[0]+"&create_time__month="+this.dateArray[1]+"&create_time__day="+this.dateArray[2]),this.date_range=this.date_range.replace(/\//g,"-"),this.getSearchList(),this.$refs.qDateProxy.hide())}},methods:{getList(){var t=this;Object(i["e"])(t.pathname+"bin/").then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getSearchList(){var t=this;Object(i["e"])(t.searchUrl).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListPrevious(){var t=this;Object(i["e"])(t.pathname_previous,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListNext(){var t=this;Object(i["e"])(t.pathname_next,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},downloadlistData(){var t=this;console.log(t.downloadhUrl),Object(i["f"])(t.downloadhUrl).then((e=>{var a=Date.now(),s=o["b"].formatDate(a,"YYYYMMDDHHmmssSSS");const n=Object(r["a"])(t.pathname+"list"+s+".csv","\ufeff"+e.data,"text/csv");!0!==n&&t.$q.notify({message:"Browser denied file download...",color:"negative",icon:"warning"})}))},reset(){this.getList(),this.downloadUrl="stock/filebinlist/",this.createDate2=""}},created(){var t=this;l["a"].has("openid")?t.openid=l["a"].getItem("openid"):(t.openid="",l["a"].set("openid","")),l["a"].has("login_name")?t.login_name=l["a"].getItem("login_name"):(t.login_name="",l["a"].set("login_name","")),l["a"].has("auth")?(t.authin="1",t.getList()):t.authin="0"},mounted(){var t=this;t.$q.platform.is.electron?t.height=String(t.$q.screen.height-290)+"px":t.height=t.$q.screen.height-290+"px"},updated(){},destroyed(){}},d=c,p=a("42e1"),_=a("5a27"),h=a("eaac"),m=a("27f9"),u=a("0016"),g=a("7cbe"),b=a("52ee"),v=a("e7a9"),f=a("9c40"),w=a("05c0"),y=a("bd08"),k=a("db86"),q=a("eebe"),x=a.n(q),$=Object(p["a"])(d,s,n,!1,null,null,null);"function"===typeof _["default"]&&Object(_["default"])($);e["default"]=$.exports;x()($,"components",{QTable:h["a"],QInput:m["a"],QIcon:u["a"],QPopupProxy:g["a"],QDate:b["a"],QBtnGroup:v["a"],QBtn:f["a"],QTooltip:w["a"],QTr:y["a"],QTd:k["a"]})},"5a27":function(t,e,a){"use strict";var s=a("1637"),n=a.n(s);e["default"]=n.a}}]);