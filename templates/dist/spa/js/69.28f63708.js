(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[69],{"778f":function(e,t,a){"use strict";var n=a("ce4f"),i=a.n(n);t["default"]=i.a},ce4f:function(e,t){},ea4d:function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e._self._c;return t("div",[t("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[t("q-table",{staticClass:"my-sticky-header-table shadow-24",attrs:{data:e.table_list,"row-key":"name",separator:e.separator,loading:e.loading,filter:e.filter,columns:e.columns,"hide-bottom":"",pagination:e.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:e.height},flat:"",bordered:"","selected-rows-label":e.getSelectedString,selection:"multiple",selected:e.selected},on:{"update:pagination":function(t){e.pagination=t},"update:selected":function(t){e.selected=t}},scopedSlots:e._u([{key:"top",fn:function(){return[t("q-btn-group",{attrs:{push:""}},[t("q-btn",{attrs:{label:e.$t("refresh"),icon:"refresh"},on:{click:function(t){return e.reFresh()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v("\n             "+e._s(e.$t("refreshtip"))+"\n           ")])],1),t("q-btn",{attrs:{label:"分配拣货员",icon:"how_to_vote"},on:{click:function(t){return e.openStaff()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v("\n               把拣货单分配给拣货员\n             ")])],1)],1),t("q-space"),t("q-input",{attrs:{outlined:"",rounded:"",dense:"",debounce:"300",color:"primary",placeholder:e.$t("search")},on:{blur:function(t){return e.getSearchList()},keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.getSearchList()}},scopedSlots:e._u([{key:"append",fn:function(){return[t("q-icon",{attrs:{name:"search"},on:{click:function(t){return e.getSearchList()}}})]},proxy:!0}]),model:{value:e.filter,callback:function(t){e.filter=t},expression:"filter"}})]},proxy:!0}])})],1),[t("div",{staticClass:"q-pa-lg flex flex-center"},[t("q-pagination",{directives:[{name:"show",rawName:"v-show",value:0!==e.page_count,expression:"page_count!==0"}],attrs:{color:"purple",max:Math.ceil(e.page_count/30),"max-pages":30,"boundary-numbers":"","direction-links":""},on:{click:function(t){return e.getList()}},model:{value:e.current,callback:function(t){e.current=t},expression:"current"}}),t("q-btn",{directives:[{name:"show",rawName:"v-show",value:0===e.page_count,expression:"page_count===0"}],attrs:{flat:"",push:"",color:"dark",label:e.$t("no_data")}})],1)],t("q-dialog",{model:{value:e.allocte_form,callback:function(t){e.allocte_form=t},expression:"allocte_form"}},[t("q-card",{staticClass:"shadow-24"},[t("q-bar",{staticClass:"bg-light-blue-10 text-white rounded-borders",staticStyle:{height:"50px"}},[t("div",[e._v("分配拣货单")]),t("q-space"),t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{dense:"",flat:"",icon:"close"}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4"}},[e._v(e._s(e.$t("index.close"))+"\n        ")])],1)],1),t("q-card-section",{staticClass:"scroll",staticStyle:{"max-height":"325px",width:"400px"}},[t("q-select",{staticStyle:{"margin-bottom":"5px"},attrs:{filled:"","use-input":"","fill-input":"","hide-selected":"","input-debounce":"0",dense:"",outlined:"",square:"",options:e.staff_list,label:"拣货员",rules:[e=>e&&e.length>0||"请选择拣货员"]},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.allocateSubmit()}},model:{value:e.filter_data.staff_name,callback:function(t){e.$set(e.filter_data,"staff_name",t)},expression:"filter_data.staff_name"}})],1),t("div",{staticStyle:{float:"right",padding:"15px 15px 15px 0"}},[t("q-btn",{staticStyle:{"margin-right":"25px"},attrs:{color:"white","text-color":"black"},on:{click:function(t){return e.cancelSubmit()}}},[e._v(e._s(e.$t("cancel"))+"\n      ")]),t("q-btn",{attrs:{color:"primary"},on:{click:function(t){return e.allocateSubmit()}}},[e._v(e._s(e.$t("submit"))+"\n      ")])],1)],1)],1)],2)},i=[],l=a("3004"),o={name:"Pagednmorepick",data(){return{current:1,page_count:0,openid:"",login_name:"",authin:"0",pathname:"dn/pickingsumfilter/",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],bin_size_list:[],bin_property_list:[],warehouse_list:[],columns:[{name:"txnid",required:!0,label:"TxnId",align:"left",field:"txnid"},{name:"creater",label:this.$t("creater"),field:"creater",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"center"}],filter:"",pagination:{page:1,rowsPerPage:"30"},bin_list:[],staff_list:[],allocte_form:!1,filter_data:{txnid:"",staff_name:"",dn_code:"",bar_code:"",picking_list:[]},selected:[]}},methods:{getList(){var e=this;e.$q.localStorage.has("auth")&&(Object(l["e"])("dn/pickinglistfilter/?txnid=TEST-2024053113",{}).then((e=>{console.log(e)})),Object(l["e"])(e.pathname+"?page="+this.current+"&picking_status=0&order_line=2",{}).then((t=>{e.page_count=t.count,e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next,e.bin_list=t.bin_list,e.staff_list=t.staff_list})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})})))},getSearchList(){var e=this;e.$q.localStorage.has("auth")&&Object(l["e"])(e.pathname+"?txnid__icontains="+e.filter+"&page="+this.current,{}).then((t=>{e.page_count=t.count,e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getListPrevious(){var e=this;e.$q.localStorage.has("auth")&&Object(l["e"])(e.pathname_previous,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getListNext(){var e=this;e.$q.localStorage.has("auth")&&Object(l["e"])(e.pathname_next,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},reFresh(){var e=this;e.getList()},openStaff(){var e=this;e.$q.localStorage.has("auth")?e.allocte_form=!0:e.$q.notify({message:e.$t("no_auth"),icon:"close",color:"negative"})},allocateStaff(e){var t=this;t.$q.localStorage.has("auth")?(t.filter_data.txnid=e.txnid,t.filter_data.dn_code=e.dn_code,t.filter_data.bar_code=e.bar_code,t.resSubmit()):t.$q.notify({message:t.$t("no_auth"),icon:"close",color:"negative"})},allocateSubmit(){var e=this;e.$q.localStorage.has("auth")&&(""===e.filter_data.staff_name?e.$q.notify({message:"请选择拣货员",icon:"close",color:"negative"}):this.selected.length>=1&&e.selected.forEach(((t,a)=>{e.allocateStaff(t)})))},cancelSubmit(){var e=this;e.allocte_form=!1,e.filter_data.txnid="",e.filter_data.dn_code="",e.filter_data.bar_code="",e.filter_data.picking_list=[]},resSubmit(){var e=this;e.$q.localStorage.has("auth")&&Object(l["i"])(l["b"]+"dn/morepicking/?page="+this.current+"&picking_status=0&order_line=2&txnid="+e.filter_data.txnid,e.filter_data).then((t=>{Object(l["e"])("dn/pickinglistfilter/?txnid="+e.filter_data.txnid).then((t=>{e.filter_data.picking_list=t.results,Object(l["i"])("http://127.0.0.1:8008/print_picking/"+this.$q.localStorage.getItem("printer")+"/"+e.filter_data.txnid+"/",e.filter_data).then((t=>{e.cancelSubmit(),e.getList(),e.$q.notify({message:"分配成功",icon:"check",color:"green"}),this.$q.notify({message:"拣货单打印成功"})}))}))})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getSelectedString(){return 0===this.selected.length?"":`${this.selected.length} record${this.selected.length>1?"s":""} selected of ${this.data.length}`}},created(){var e=this;e.$q.localStorage.has("openid")?e.openid=e.$q.localStorage.getItem("openid"):(e.openid="",e.$q.localStorage.set("openid","")),e.$q.localStorage.has("login_name")?e.login_name=e.$q.localStorage.getItem("login_name"):(e.login_name="",e.$q.localStorage.set("login_name","")),e.$q.localStorage.has("auth")?(e.authin="1",e.getList()):e.authin="0"},mounted(){var e=this;e.$q.platform.is.electron?e.height=String(e.$q.screen.height-290)+"px":e.height=e.$q.screen.height-290+"px"},updated(){},destroyed(){}},s=o,r=a("42e1"),c=a("778f"),d=a("eaac"),u=a("e7a9"),p=a("9c40"),h=a("05c0"),f=a("2c91"),g=a("27f9"),_=a("0016"),m=a("3b16"),b=a("24e8"),v=a("f09f"),x=a("d847"),q=a("a370"),S=a("ddd8"),$=a("7f67"),k=a("eebe"),y=a.n(k),w=Object(r["a"])(s,n,i,!1,null,null,null);"function"===typeof c["default"]&&Object(c["default"])(w);t["default"]=w.exports;y()(w,"components",{QTable:d["a"],QBtnGroup:u["a"],QBtn:p["a"],QTooltip:h["a"],QSpace:f["a"],QInput:g["a"],QIcon:_["a"],QPagination:m["a"],QDialog:b["a"],QCard:v["a"],QBar:x["a"],QCardSection:q["a"],QSelect:S["a"]}),y()(w,"directives",{ClosePopup:$["a"]})}}]);