(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[69],{"778f":function(t,e,a){"use strict";var n=a("ce4f"),i=a.n(n);e["default"]=i.a},ce4f:function(t,e){},ea4d:function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t._self._c;return e("div",[e("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[e("q-table",{staticClass:"my-sticky-header-table shadow-24",attrs:{data:t.table_list,"row-key":"id",separator:t.separator,loading:t.loading,filter:t.filter,columns:t.columns,"hide-bottom":"",pagination:t.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:t.height},flat:"",bordered:"",selection:"multiple",selected:t.selected},on:{"update:pagination":function(e){t.pagination=e},"update:selected":function(e){t.selected=e}},scopedSlots:t._u([{key:"top",fn:function(){return[e("q-btn-group",{attrs:{push:""}},[e("q-btn",{attrs:{label:t.$t("refresh"),icon:"refresh"},on:{click:function(e){return t.reFresh()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n             "+t._s(t.$t("refreshtip"))+"\n           ")])],1),e("q-btn",{attrs:{label:"分配拣货员",icon:"how_to_vote"},on:{click:function(e){return t.openStaff()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n               把拣货单分配给拣货员\n             ")])],1)],1),e("q-space"),e("q-input",{attrs:{outlined:"",rounded:"",dense:"",debounce:"300",color:"primary",placeholder:t.$t("search")},on:{blur:function(e){return t.getSearchList()},keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.getSearchList()}},scopedSlots:t._u([{key:"append",fn:function(){return[e("q-icon",{attrs:{name:"search"},on:{click:function(e){return t.getSearchList()}}})]},proxy:!0}]),model:{value:t.filter,callback:function(e){t.filter=e},expression:"filter"}})]},proxy:!0}])})],1),[e("div",{staticClass:"q-pa-lg flex flex-center"},[e("q-pagination",{directives:[{name:"show",rawName:"v-show",value:0!==t.page_count,expression:"page_count!==0"}],attrs:{color:"purple",max:Math.ceil(t.page_count/30),"max-pages":30,"boundary-numbers":"","direction-links":""},on:{click:function(e){return t.getList()}},model:{value:t.current,callback:function(e){t.current=e},expression:"current"}}),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:0===t.page_count,expression:"page_count===0"}],attrs:{flat:"",push:"",color:"dark",label:t.$t("no_data")}})],1)],e("q-dialog",{model:{value:t.allocte_form,callback:function(e){t.allocte_form=e},expression:"allocte_form"}},[e("q-card",{staticClass:"shadow-24"},[e("q-bar",{staticClass:"bg-light-blue-10 text-white rounded-borders",staticStyle:{height:"50px"}},[e("div",[t._v("分配拣货单")]),e("q-space"),e("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{dense:"",flat:"",icon:"close"}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4"}},[t._v(t._s(t.$t("index.close"))+"\n        ")])],1)],1),e("q-card-section",{staticClass:"scroll",staticStyle:{"max-height":"325px",width:"400px"}},[e("q-select",{staticStyle:{"margin-bottom":"5px"},attrs:{filled:"","use-input":"","fill-input":"","hide-selected":"","input-debounce":"0",dense:"",outlined:"",square:"",options:t.staff_list,label:"拣货员",rules:[t=>t&&t.length>0||"请选择拣货员"]},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.allocateSubmit()}},model:{value:t.filter_data.staff_name,callback:function(e){t.$set(t.filter_data,"staff_name",e)},expression:"filter_data.staff_name"}})],1),e("div",{staticStyle:{float:"right",padding:"15px 15px 15px 0"}},[e("q-btn",{staticStyle:{"margin-right":"25px"},attrs:{color:"white","text-color":"black"},on:{click:function(e){return t.cancelSubmit()}}},[t._v(t._s(t.$t("cancel"))+"\n      ")]),e("q-btn",{attrs:{color:"primary"},on:{click:function(e){return t.allocateSubmit()}}},[t._v(t._s(t.$t("submit"))+"\n      ")])],1)],1)],1)],2)},i=[],l=a("3004"),o={name:"Pagednmorepick",data(){return{current:1,page_count:0,openid:"",login_name:"",authin:"0",pathname:"dn/pickingsumfilter/",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],bin_size_list:[],bin_property_list:[],warehouse_list:[],columns:[{name:"txnid",required:!0,label:"TxnId",align:"left",field:"txnid"},{name:"creater",label:this.$t("creater"),field:"creater",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"center"}],filter:"",pagination:{page:1,rowsPerPage:"30"},bin_list:[],staff_list:[],allocte_form:!1,filter_data:{txnid:"",staff_name:"",dn_code:"",bar_code:"",picking_list:[]},selected:[]}},methods:{getList(){var t=this;t.$q.localStorage.has("auth")&&(Object(l["e"])("dn/pickinglistfilter/?txnid=TEST-2024053113",{}).then((t=>{console.log(t)})),Object(l["e"])(t.pathname+"?page="+this.current+"&picking_status=0&order_line=2",{}).then((e=>{t.page_count=e.count,t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next,t.bin_list=e.bin_list,t.staff_list=e.staff_list})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})})))},getSearchList(){var t=this;t.$q.localStorage.has("auth")&&Object(l["e"])(t.pathname+"?txnid__icontains="+t.filter+"&page="+this.current,{}).then((e=>{t.page_count=e.count,t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListPrevious(){var t=this;t.$q.localStorage.has("auth")&&Object(l["e"])(t.pathname_previous,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListNext(){var t=this;t.$q.localStorage.has("auth")&&Object(l["e"])(t.pathname_next,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},reFresh(){var t=this;t.getList()},openStaff(){var t=this;t.$q.localStorage.has("auth")?t.allocte_form=!0:t.$q.notify({message:t.$t("no_auth"),icon:"close",color:"negative"})},allocateStaff(t){var e=this;e.$q.localStorage.has("auth")?(e.filter_data.txnid=t.txnid,e.filter_data.dn_code=t.dn_code,e.filter_data.bar_code=t.bar_code,e.resSubmit()):e.$q.notify({message:e.$t("no_auth"),icon:"close",color:"negative"})},allocateSubmit(){var t=this;t.$q.localStorage.has("auth")&&(""===t.filter_data.staff_name?t.$q.notify({message:"请选择拣货员",icon:"close",color:"negative"}):this.selected.length>=1&&(t.selected.forEach(((e,a)=>{t.allocateStaff(e)})),t.getList(),t.$q.notify({message:"分配成功",icon:"check",color:"green"})))},cancelSubmit(){var t=this;t.allocte_form=!1,t.filter_data.txnid="",t.filter_data.dn_code="",t.filter_data.bar_code="",t.filter_data.picking_list=[]},resSubmit(){var t=this;t.$q.localStorage.has("auth")&&Object(l["i"])(l["b"]+"dn/morepicking/?page="+this.current+"&picking_status=0&order_line=2&txnid="+t.filter_data.txnid,t.filter_data).then((e=>{Object(l["e"])("dn/pickinglistfilter/?txnid="+t.filter_data.txnid).then((e=>{t.filter_data.picking_list=e.results,Object(l["i"])("http://127.0.0.1:8008/print_picking/"+this.$q.localStorage.getItem("printer")+"/"+t.filter_data.txnid+"/",t.filter_data).then((e=>{t.cancelSubmit(),this.$q.notify({message:t.filter_data.txnid+"的拣货单打印成功"})}))}))})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getSelectedString(){return 0===this.selected.length?"":`${this.selected.length} record${this.selected.length>1?"s":""} selected of ${this.data.length}`}},created(){var t=this;t.$q.localStorage.has("openid")?t.openid=t.$q.localStorage.getItem("openid"):(t.openid="",t.$q.localStorage.set("openid","")),t.$q.localStorage.has("login_name")?t.login_name=t.$q.localStorage.getItem("login_name"):(t.login_name="",t.$q.localStorage.set("login_name","")),t.$q.localStorage.has("auth")?(t.authin="1",t.getList()):t.authin="0"},mounted(){var t=this;t.$q.platform.is.electron?t.height=String(t.$q.screen.height-290)+"px":t.height=t.$q.screen.height-290+"px"},updated(){},destroyed(){}},s=o,r=a("42e1"),c=a("778f"),d=a("eaac"),u=a("e7a9"),p=a("9c40"),h=a("05c0"),f=a("2c91"),g=a("27f9"),_=a("0016"),m=a("3b16"),b=a("24e8"),x=a("f09f"),v=a("d847"),q=a("a370"),S=a("ddd8"),$=a("7f67"),k=a("eebe"),y=a.n(k),w=Object(r["a"])(s,n,i,!1,null,null,null);"function"===typeof c["default"]&&Object(c["default"])(w);e["default"]=w.exports;y()(w,"components",{QTable:d["a"],QBtnGroup:u["a"],QBtn:p["a"],QTooltip:h["a"],QSpace:f["a"],QInput:g["a"],QIcon:_["a"],QPagination:m["a"],QDialog:b["a"],QCard:x["a"],QBar:v["a"],QCardSection:q["a"],QSelect:S["a"]}),y()(w,"directives",{ClosePopup:$["a"]})}}]);