(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[31],{4997:function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e._self._c;return t("div",[t("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[t("q-table",{staticClass:"my-sticky-header-column-table shadow-24",attrs:{data:e.table_list,"row-key":"id",separator:e.separator,loading:e.loading,filter:e.filter,columns:e.columns,"hide-bottom":"",pagination:e.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:e.height},flat:"",bordered:""},on:{"update:pagination":function(t){e.pagination=t}},scopedSlots:e._u([{key:"top",fn:function(){return[t("q-btn-group",{attrs:{push:""}},[t("q-btn",{attrs:{label:e.$t("new"),icon:"add"},on:{click:function(t){e.newForm=!0}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("newtip")))])],1),t("q-btn",{attrs:{label:e.$t("refresh"),icon:"refresh"},on:{click:function(t){return e.reFresh()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("refreshtip")))])],1),t("q-btn",{attrs:{label:e.$t("download"),icon:"cloud_download"},on:{click:function(t){return e.downloadData()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("downloadtip")))])],1)],1),t("q-space"),t("q-input",{attrs:{outlined:"",rounded:"",dense:"",debounce:"300",color:"primary",placeholder:e.$t("search")},on:{blur:function(t){return e.getSearchList()},keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.getSearchList()}},scopedSlots:e._u([{key:"append",fn:function(){return[t("q-icon",{attrs:{name:"search"},on:{click:function(t){return e.getSearchList()}}})]},proxy:!0}]),model:{value:e.filter,callback:function(t){e.filter=t},expression:"filter"}})]},proxy:!0},{key:"body",fn:function(a){return[t("q-tr",{attrs:{props:a}},[a.row.id===e.editid?[t("q-td",{key:"driver_name",attrs:{props:a}},[t("q-input",{attrs:{dense:"",outlined:"",square:"",label:e.$t("driver.view_driver.driver_name"),autofocus:""},model:{value:e.editFormData.driver_name,callback:function(t){e.$set(e.editFormData,"driver_name",t)},expression:"editFormData.driver_name"}})],1)]:a.row.id!==e.editid?[t("q-td",{key:"driver_name",attrs:{props:a}},[e._v(e._s(a.row.driver_name))])]:e._e(),a.row.id===e.editid?[t("q-td",{key:"license_plate",attrs:{props:a}},[t("q-input",{attrs:{dense:"",outlined:"",square:"",label:e.$t("driver.view_driver.license_plate")},model:{value:e.editFormData.license_plate,callback:function(t){e.$set(e.editFormData,"license_plate",t)},expression:"editFormData.license_plate"}})],1)]:a.row.id!==e.editid?[t("q-td",{key:"license_plate",attrs:{props:a}},[e._v(e._s(a.row.license_plate))])]:e._e(),a.row.id===e.editid?[t("q-td",{key:"contact",attrs:{props:a}},[t("q-input",{attrs:{dense:"",outlined:"",square:"",label:e.$t("driver.view_driver.contact")},model:{value:e.editFormData.contact,callback:function(t){e.$set(e.editFormData,"contact",t)},expression:"editFormData.contact"}})],1)]:a.row.id!==e.editid?[t("q-td",{key:"contact",attrs:{props:a}},[e._v(e._s(a.row.contact))])]:e._e(),t("q-td",{key:"creater",attrs:{props:a}},[e._v(e._s(a.row.creater))]),t("q-td",{key:"create_time",attrs:{props:a}},[e._v(e._s(a.row.create_time))]),t("q-td",{key:"update_time",attrs:{props:a}},[e._v(e._s(a.row.update_time))]),e.editMode?e.editMode?[a.row.id===e.editid?[t("q-td",{key:"action",staticStyle:{width:"100px"},attrs:{props:a}},[t("q-btn",{attrs:{round:"",flat:"",push:"",color:"secondary",icon:"check"},on:{click:function(t){return e.editDataSubmit()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("confirmedit")))])],1),t("q-btn",{attrs:{round:"",flat:"",push:"",color:"red",icon:"close"},on:{click:function(t){return e.editDataCancel()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("canceledit")))])],1)],1)]:a.row.id!==e.editid?void 0:e._e()]:e._e():[t("q-td",{key:"action",staticStyle:{width:"100px"},attrs:{props:a}},[t("q-btn",{attrs:{round:"",flat:"",push:"",color:"purple",icon:"edit"},on:{click:function(t){return e.editData(a.row)}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("edit")))])],1),t("q-btn",{attrs:{round:"",flat:"",push:"",color:"dark",icon:"delete"},on:{click:function(t){return e.deleteData(a.row.id)}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("delete")))])],1)],1)]],2)]}}])})],1),[t("div",{staticClass:"q-pa-lg flex flex-center"},[t("q-btn",{directives:[{name:"show",rawName:"v-show",value:e.pathname_previous,expression:"pathname_previous"}],attrs:{flat:"",push:"",color:"purple",label:e.$t("previous"),icon:"navigate_before"},on:{click:function(t){return e.getListPrevious()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("previous")))])],1),t("q-btn",{directives:[{name:"show",rawName:"v-show",value:e.pathname_next,expression:"pathname_next"}],attrs:{flat:"",push:"",color:"purple",label:e.$t("next"),"icon-right":"navigate_next"},on:{click:function(t){return e.getListNext()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("next")))])],1),t("q-btn",{directives:[{name:"show",rawName:"v-show",value:!e.pathname_previous&&!e.pathname_next,expression:"!pathname_previous && !pathname_next"}],attrs:{flat:"",push:"",color:"dark",label:e.$t("no_data")}})],1)],t("q-dialog",{model:{value:e.newForm,callback:function(t){e.newForm=t},expression:"newForm"}},[t("q-card",{staticClass:"shadow-24"},[t("q-bar",{staticClass:"bg-light-blue-10 text-white rounded-borders",staticStyle:{height:"50px"}},[t("div",[e._v(e._s(e.$t("newtip")))]),t("q-space"),t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{dense:"",flat:"",icon:"close"}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4"}},[e._v(e._s(e.$t("index.close")))])],1)],1),t("q-card-section",{staticClass:"scroll",staticStyle:{"max-height":"325px",width:"400px"}},[t("q-input",{attrs:{dense:"",outlined:"",square:"",label:e.$t("driver.view_driver.driver_name"),autofocus:"",rules:[t=>t&&t.length>0||e.error1]},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.newDataSubmit()}},model:{value:e.newFormData.driver_name,callback:function(t){e.$set(e.newFormData,"driver_name",t)},expression:"newFormData.driver_name"}}),t("q-input",{attrs:{dense:"",outlined:"",square:"",label:e.$t("driver.view_driver.license_plate"),rules:[t=>t&&t.length>0||e.error2]},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.newDataSubmit()}},model:{value:e.newFormData.license_plate,callback:function(t){e.$set(e.newFormData,"license_plate",t)},expression:"newFormData.license_plate"}}),t("q-input",{attrs:{dense:"",outlined:"",square:"",label:e.$t("driver.view_driver.contact"),rules:[t=>t&&t>0||e.error3]},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.newDataSubmit()}},model:{value:e.newFormData.contact,callback:function(t){e.$set(e.newFormData,"contact",t)},expression:"newFormData.contact"}})],1),t("div",{staticStyle:{float:"right",padding:"15px 15px 15px 0"}},[t("q-btn",{staticStyle:{"margin-right":"25px"},attrs:{color:"white","text-color":"black"},on:{click:function(t){return e.newDataCancel()}}},[e._v(e._s(e.$t("cancel")))]),t("q-btn",{attrs:{color:"primary"},on:{click:function(t){return e.newDataSubmit()}}},[e._v(e._s(e.$t("submit")))])],1)],1)],1),t("q-dialog",{model:{value:e.deleteForm,callback:function(t){e.deleteForm=t},expression:"deleteForm"}},[t("q-card",{staticClass:"shadow-24"},[t("q-bar",{staticClass:"bg-light-blue-10 text-white rounded-borders",staticStyle:{height:"50px"}},[t("div",[e._v(e._s(e.$t("delete")))]),t("q-space"),t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{dense:"",flat:"",icon:"close"}},[t("q-tooltip",[e._v(e._s(e.$t("index.close")))])],1)],1),t("q-card-section",{staticClass:"scroll",staticStyle:{"max-height":"325px",width:"400px"}},[e._v(e._s(e.$t("deletetip")))]),t("div",{staticStyle:{float:"right",padding:"15px 15px 15px 0"}},[t("q-btn",{staticStyle:{"margin-right":"25px"},attrs:{color:"white","text-color":"black"},on:{click:function(t){return e.deleteDataCancel()}}},[e._v(e._s(e.$t("cancel")))]),t("q-btn",{attrs:{color:"primary"},on:{click:function(t){return e.deleteDataSubmit()}}},[e._v(e._s(e.$t("submit")))])],1)],1)],1)],2)},r=[],i=a("3004"),o=a("bd4c"),s=a("a357"),l=a("18d6"),c={name:"Pagedriverlist",data(){return{openid:"",login_name:"",authin:"0",pathname:"driver/",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],columns:[{name:"driver_name",required:!0,label:this.$t("driver.view_driver.driver_name"),align:"left",field:"driver_name"},{name:"license_plate",label:this.$t("driver.view_driver.license_plate"),field:"license_plate",align:"center"},{name:"contact",label:this.$t("driver.view_driver.contact"),field:"contact",align:"center"},{name:"creater",label:this.$t("creater"),field:"creater",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"center"},{name:"action",label:this.$t("action"),align:"right"}],filter:"",pagination:{page:1,rowsPerPage:"30"},newForm:!1,newFormData:{driver_name:"",license_plate:"",contact:"",creater:""},editid:0,editFormData:{},editMode:!1,deleteForm:!1,deleteid:0,error1:this.$t("driver.error1"),error2:this.$t("driver.error2"),error3:this.$t("driver.error3")}},methods:{getList(){var e=this;e.$q.localStorage.has("auth")&&Object(i["e"])(e.pathname,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getSearchList(){var e=this;e.$q.localStorage.has("auth")&&Object(i["e"])(e.pathname+"?driver_name__icontains="+e.filter,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getListPrevious(){var e=this;e.$q.localStorage.has("auth")&&Object(i["e"])(e.pathname_previous,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},getListNext(){var e=this;e.$q.localStorage.has("auth")&&Object(i["e"])(e.pathname_next,{}).then((t=>{e.table_list=t.results,e.pathname_previous=t.previous,e.pathname_next=t.next})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},reFresh(){var e=this;e.getList()},newDataSubmit(){var e=this;0!==e.newFormData.driver_name.length?(e.newFormData.creater=e.login_name,Object(i["i"])(e.pathname,e.newFormData).then((t=>{e.getList(),e.newDataCancel(),t.detail||e.$q.notify({message:"Success Create",icon:"check",color:"green"})})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))):e.$q.notify({message:"",icon:"close",color:"negative"})},newDataCancel(){var e=this;e.newForm=!1,e.newFormData={driver_name:"",license_plate:"",contact:"",creater:""}},editData(e){var t=this;t.editMode=!0,t.editid=e.id,t.editFormData={driver_name:e.driver_name,license_plate:e.license_plate,contact:e.contact,creater:t.login_name}},editDataSubmit(){var e=this;Object(i["j"])(e.pathname+e.editid+"/",e.editFormData).then((t=>{e.editDataCancel(),e.getList(),e.$q.notify({message:"Success Edit Data",icon:"check",color:"green"})})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},editDataCancel(){var e=this;e.editMode=!1,e.editid=0,e.editFormData={driver_name:"",license_plate:"",contact:"",creater:""}},deleteData(e){var t=this;t.deleteForm=!0,t.deleteid=e},deleteDataSubmit(){var e=this;Object(i["d"])(e.pathname+e.deleteid+"/").then((t=>{e.deleteDataCancel(),e.getList(),e.$q.notify({message:"Success Edit Data",icon:"check",color:"green"})})).catch((t=>{e.$q.notify({message:t.detail,icon:"close",color:"negative"})}))},deleteDataCancel(){var e=this;e.deleteForm=!1,e.deleteid=0},downloadData(){var e=this;l["a"].has("auth")?Object(i["f"])(e.pathname+"file/?lang="+l["a"].getItem("lang")).then((t=>{var a=Date.now(),n=o["b"].formatDate(a,"YYYYMMDDHHmmssSSS");const r=Object(s["a"])(e.pathname+n+".csv","\ufeff"+t.data,"text/csv");!0!==r&&e.$q.notify({message:"Browser denied file download...",color:"negative",icon:"warning"})})):e.$q.notify({message:e.$t("notice.loginerror"),color:"negative",icon:"warning"})}},created(){var e=this;e.$q.localStorage.has("openid")?e.openid=e.$q.localStorage.getItem("openid"):(e.openid="",e.$q.localStorage.set("openid","")),e.$q.localStorage.has("login_name")?e.login_name=e.$q.localStorage.getItem("login_name"):(e.login_name="",e.$q.localStorage.set("login_name","")),e.$q.localStorage.has("auth")?(e.authin="1",e.getList()):e.authin="0"},mounted(){var e=this;e.$q.platform.is.electron?e.height=String(e.$q.screen.height-290)+"px":e.height=e.$q.screen.height-290+"px"},updated(){},destroyed(){}},d=c,p=a("42e1"),u=a("737f"),m=a("eaac"),h=a("e7a9"),v=a("9c40"),_=a("05c0"),f=a("2c91"),b=a("27f9"),g=a("0016"),w=a("bd08"),q=a("db86"),x=a("24e8"),y=a("f09f"),k=a("d847"),$=a("a370"),D=a("7f67"),S=a("eebe"),F=a.n(S),C=Object(p["a"])(d,n,r,!1,null,null,null);"function"===typeof u["default"]&&Object(u["default"])(C);t["default"]=C.exports;F()(C,"components",{QTable:m["a"],QBtnGroup:h["a"],QBtn:v["a"],QTooltip:_["a"],QSpace:f["a"],QInput:b["a"],QIcon:g["a"],QTr:w["a"],QTd:q["a"],QDialog:x["a"],QCard:y["a"],QBar:k["a"],QCardSection:$["a"]}),F()(C,"directives",{ClosePopup:D["a"]})},"610a":function(e,t){},"737f":function(e,t,a){"use strict";var n=a("610a"),r=a.n(n);t["default"]=r.a}}]);