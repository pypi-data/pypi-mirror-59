(function(e){function t(t){for(var n,o,i=t[0],c=t[1],u=t[2],p=0,m=[];p<i.length;p++)o=i[p],a[o]&&m.push(a[o][0]),a[o]=0;for(n in c)Object.prototype.hasOwnProperty.call(c,n)&&(e[n]=c[n]);l&&l(t);while(m.length)m.shift()();return s.push.apply(s,u||[]),r()}function r(){for(var e,t=0;t<s.length;t++){for(var r=s[t],n=!0,i=1;i<r.length;i++){var c=r[i];0!==a[c]&&(n=!1)}n&&(s.splice(t--,1),e=o(o.s=r[0]))}return e}var n={},a={app:0},s=[];function o(t){if(n[t])return n[t].exports;var r=n[t]={i:t,l:!1,exports:{}};return e[t].call(r.exports,r,r.exports,o),r.l=!0,r.exports}o.m=e,o.c=n,o.d=function(e,t,r){o.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},o.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},o.t=function(e,t){if(1&t&&(e=o(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(o.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)o.d(r,n,function(t){return e[t]}.bind(null,n));return r},o.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return o.d(t,"a",t),t},o.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},o.p="";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],c=i.push.bind(i);i.push=t,i=i.slice();for(var u=0;u<i.length;u++)t(i[u]);var l=c;s.push([0,"chunk-vendors"]),r()})({0:function(e,t,r){e.exports=r("cd49")},"0af9":function(e,t,r){},"0e67":function(e,t,r){},"22ec":function(e,t,r){},"3a87":function(e,t,r){},4084:function(e,t,r){},"4fde":function(e,t,r){"use strict";var n=r("4084"),a=r.n(n);a.a},"584d":function(e,t,r){},"5c48":function(e,t,r){},6524:function(e,t,r){"use strict";var n=r("3a87"),a=r.n(n);a.a},6715:function(e,t,r){},"70d0":function(e,t,r){"use strict";var n=r("0e67"),a=r.n(n);a.a},7191:function(e,t,r){"use strict";var n=r("6715"),a=r.n(n);a.a},"77dc":function(e,t,r){"use strict";var n=r("a6ee"),a=r.n(n);a.a},"7c55":function(e,t,r){"use strict";var n=r("5c48"),a=r.n(n);a.a},"7dd9":function(e,t,r){"use strict";var n=r("22ec"),a=r.n(n);a.a},8233:function(e,t,r){},"86ca":function(e,t,r){"use strict";var n=r("91de"),a=r.n(n);a.a},"91de":function(e,t,r){},"965b":function(e,t,r){"use strict";var n=r("0af9"),a=r.n(n);a.a},a6ee:function(e,t,r){},be47:function(e,t,r){"use strict";var n=r("584d"),a=r.n(n);a.a},cd49:function(e,t,r){"use strict";r.r(t);r("cadf"),r("551c"),r("f751"),r("097d");var n=r("2b0e"),a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"app"}},[r("router-view"),r("MessagePopup")],1)},s=[],o=(r("96cf"),r("3b8d")),i=r("bc3a"),c=r.n(i),u=function(){var e=this,t=e.$createElement,r=e._self._c||t;return e.visible?r("div",{attrs:{id:"message_popup"}},[r("p",{staticClass:"message"},[e._v(e._s(e.message))]),r("p",{staticClass:"close"},[r("a",{attrs:{href:"#"},on:{click:function(t){t.preventDefault(),e.visible=!1}}},[e._v("Close")])])]):e._e()},l=[],p=n["a"].extend({data:function(){return{visible:!1,timeLastAppeared:0}},computed:{message:function(){return this.apiResponseMessage?this.apiResponseMessage.contents:"-"},apiResponseMessage:function(){return this.$store.state.apiResponseMessage}},methods:{getTime:function(){return(new Date).getTime()}},watch:{visible:function(){this.timeLastAppeared=this.getTime()},apiResponseMessage:function(){var e=this;this.visible=!0;var t=this;setTimeout(function(){var r=e.getTime();r-t.timeLastAppeared>=3e3&&(t.visible=!1)},3e3)}}}),m=p,f=(r("6524"),r("2877")),h=Object(f["a"])(m,u,l,!1,null,null,null),d=h.exports,v={components:{MessagePopup:d},beforeCreate:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){var t,r;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return t=this,c.a.interceptors.response.use(function(e){return e},function(e){return 401==e.response.status&&(console.log("Login required"),t.$router.push({name:"login"})),Promise.reject(e)}),e.next=4,c.a.get("./api/user/");case 4:r=e.sent,this.$store.commit("updateUser",r.data);case 6:case"end":return e.stop()}},e,this)}));function t(){return e.apply(this,arguments)}return t}()},w=v,b=(r("7c55"),Object(f["a"])(w,a,s,!1,null,null,null)),g=b.exports,_=r("8c4f"),R=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("BaseView",[r("div",{staticClass:"welcome"},[r("h1",[e._v("Welcome to Piccolo Admin")]),r("p",[e._v("Select one of the tables in the sidebar to get started.")])])])},x=[],N=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("NavBar"),r("div",{staticClass:"wrapper"},[r("SidebarNav"),e._t("default")],2)],1)},y=[],k=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"nav"}},[r("router-link",{attrs:{to:"/"}},[r("h1",[r("font-awesome-icon",{attrs:{icon:"tools"}}),e._v("Piccolo Admin\n        ")],1)]),r("p",[r("a",{staticStyle:{"padding-right":"1rem"},attrs:{href:"#"}},[r("font-awesome-icon",{attrs:{icon:"user"}}),e._v(e._s(e.username)+"\n        ")],1),r("a",{attrs:{href:"#"},on:{click:function(t){return t.preventDefault(),e.logout(t)}}},[e._v("\n            Log out\n            "),r("font-awesome-icon",{attrs:{icon:"sign-out-alt"}})],1)])],1)},$=[],O=n["a"].extend({computed:{tableName:function(){return this.$store.state.currentTableName},username:function(){var e=this.$store.state.user;return e?e.username:"Unknown"}},methods:{logout:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:if(!window.confirm("Are you sure you want to logout?")){e.next=12;break}return console.log("Logging out"),e.prev=2,e.next=5,c.a.post("./api/logout/");case 5:this.$router.push({name:"login"}),e.next=12;break;case 8:e.prev=8,e.t0=e["catch"](2),console.log("Logout failed"),console.log(e.t0);case 12:case"end":return e.stop()}},e,this,[[2,8]])}));function t(){return e.apply(this,arguments)}return t}()}}),j=O,C=(r("7191"),Object(f["a"])(j,k,$,!1,null,null,null)),S=C.exports,T=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"sidebar"},[r("p",[r("router-link",{attrs:{to:"/"}},[r("font-awesome-icon",{attrs:{icon:"home"}}),e._v("Home\n        ")],1)],1),r("p",[r("font-awesome-icon",{attrs:{icon:"table"}}),e._v("Tables\n    ")],1),r("TableNav")],1)},D=[],F=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("ul",e._l(e.tableNames,function(t){return r("li",{key:t},[r("a",{class:{active:e.isActive(t)},attrs:{href:"#"},on:{click:function(r){return r.preventDefault(),e.showListing(t)}}},[e._v(e._s(t))])])}),0)},P=[],A=n["a"].extend({computed:{tableNames:function(){return this.$store.state.tableNames},currentTableName:function(){return this.$store.state.currentTableName}},methods:{showListing:function(e){this.$store.commit("updateCurrentTablename",e),this.$router.push({name:"rowListing",params:{tableName:e}})},isActive:function(e){return this.currentTableName===e}},mounted:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.$store.dispatch("fetchTableNames");case 2:case"end":return e.stop()}},e,this)}));function t(){return e.apply(this,arguments)}return t}()}),E=A,L=(r("86ca"),Object(f["a"])(E,F,P,!1,null,"282eba58",null)),M=L.exports,I={components:{TableNav:M}},B=I,U=(r("7dd9"),Object(f["a"])(B,T,D,!1,null,null,null)),V=U.exports,K=n["a"].extend({components:{NavBar:S,SidebarNav:V}}),q=K,H=(r("e869"),Object(f["a"])(q,N,y,!1,null,null,null)),J=H.exports,W={components:{BaseView:J},mounted:function(){this.$store.commit("updateCurrentTablename","")}},X=W,z=(r("df73"),Object(f["a"])(X,R,x,!1,null,"564d2c13",null)),G=z.exports,Q=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("BaseView",[void 0!=e.schema?[r("div",{staticClass:"left_column"},[r("div",{staticClass:"title_bar"},[r("h1",[e._v(e._s(e.tableName))]),r("ul",[r("li",[r("a",{attrs:{href:"#"},on:{click:function(t){t.preventDefault(),e.showAddRow=!0}}},[r("font-awesome-icon",{attrs:{icon:"plus"}}),e._v("Add Row\n                        ")],1)]),r("li",[r("a",{attrs:{href:"#"},on:{click:function(t){t.preventDefault(),e.showFilter=!e.showFilter}}},[r("font-awesome-icon",{attrs:{icon:"filter"}}),e._v("\n                            "+e._s(e.showFilter?"Hide":"Show")+" Filters\n                        ")],1)])])]),0==e.rows.length?r("p",[e._v("No results found")]):r("table",[r("tr",[e._l(e.cellNames,function(t){return r("th",{key:t},[e._v(e._s(e.schema.properties[t]?e.schema.properties[t].title:t))])}),r("th",[e._v("Actions")])],2),e._l(e.rows,function(t){return r("tr",{key:t.id},[e._l(e.cellNames,function(n){return r("td",{key:n},["id"==n?r("span",{staticClass:"link"},[r("router-link",{attrs:{to:{name:"editRow",params:{tableName:e.tableName,rowID:t[n]}}}},[e._v(e._s(t[n]))])],1):e.isForeignKey(n)?r("span",{staticClass:"link"},[r("router-link",{attrs:{to:{name:"editRow",params:{tableName:e.getTableName(n),rowID:t[n]}}}},[e._v(e._s(t[n+"_readable"]))])],1):r("span",[e._v(e._s(t[n]))])])}),r("td",{staticClass:"snug"},[r("ul",[r("li",[r("router-link",{attrs:{to:{name:"editRow",params:{tableName:e.tableName,rowID:t.id}},title:"Edit Row"}},[r("font-awesome-icon",{attrs:{icon:"edit"}})],1)],1),r("li",[r("a",{staticClass:"delete",attrs:{href:"#",title:"Delete Row"},on:{click:function(r){return r.preventDefault(),e.deleteRow(t.id)}}},[r("font-awesome-icon",{attrs:{icon:"trash-alt"}})],1)])])])],2)})],2)]),e.showFilter?r("div",{staticClass:"right_column"},[r("RowFilter")],1):e._e(),e.showAddRow?r("AddRow",{attrs:{schema:e.schema,tableName:e.tableName},on:{addedRow:e.fetchRows,close:function(t){e.showAddRow=!1}}}):e._e()]:e._e()],2)},Y=[],Z=(r("ac6a"),r("5df3"),r("7f7f"),r("aef6"),function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("Modal",{on:{close:function(t){return e.$emit("close")}}},[r("h1",[e._v("Add")]),r("pre",[e._v(e._s(e.errors))]),e.defaults?r("form",{on:{submit:function(t){return t.preventDefault(),e.submitForm(t)}}},[r("RowForm",{attrs:{schema:e.schema,row:e.defaults}}),r("button",[e._v("Create")])],1):e._e()])}),ee=[],te=(r("ac4d"),r("8a81"),function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"overlay"}},[r("div",{staticClass:"modal"},[r("p",{staticClass:"close"},[r("a",{attrs:{href:"#"},on:{click:function(t){return t.preventDefault(),e.$emit("close")}}},[e._v("Close")])]),e._t("default")],2)])}),re=[],ne={},ae=ne,se=(r("77dc"),Object(f["a"])(ae,te,re,!1,null,"58ca6f0d",null)),oe=se.exports,ie=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",e._l(e.schema.properties,function(t){return r("div",{key:t.title},[t.foreign_key?[r("label",[e._v(e._s(t.title))]),r("KeySelect",{attrs:{fieldName:t.title.toLowerCase(),tableName:t.to,value:e.getValue(t.title)}})]:[r("InputField",{key:t.title,attrs:{format:t.format,title:t.title,type:t.type||t.anyOf[0].type,value:e.getValue(t.title)}})]],2)}),0)},ce=[],ue=(r("a481"),function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("select",{attrs:{name:e.fieldName}},[r("option",{attrs:{value:""}},[e._v("----")]),e._l(e.ids,function(t,n){return r("option",{key:n,domProps:{value:n,selected:e.value==n}},[e._v(e._s(t))])})],2)}),le=[],pe={props:["fieldName","tableName","value"],data:function(){return{ids:[]}},mounted:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){var t;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.$store.dispatch("fetchIds",this.tableName);case 2:t=e.sent,this.ids=t.data;case 4:case"end":return e.stop()}},e,this)}));function t(){return e.apply(this,arguments)}return t}()},me=pe,fe=Object(f["a"])(me,ue,le,!1,null,null,null),he=fe.exports,de=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("label",[e._v(e._s(e.title))]),"integer"==e.type?r("input",{attrs:{step:"1",type:"number",name:e.title.toLowerCase()},domProps:{value:e.value}}):e._e(),"string"==e.type?["date-time"==e.format?r("input",{staticClass:"datetime",attrs:{autocomplete:"off",type:"text",name:e.title.toLowerCase()},domProps:{value:e.value}}):r("input",{attrs:{type:"text",name:e.title.toLowerCase()},domProps:{value:e.value}})]:e._e(),r("div",{staticClass:"checkbox_wrapper"},["boolean"==e.type?r("input",{attrs:{type:"checkbox",name:e.title.toLowerCase()},domProps:{checked:e.value,value:e.value},on:{change:function(t){return e.valueChanged(t)}}}):e._e()])],2)},ve=[],we={props:{title:String,type:String,value:void 0,format:String},methods:{valueChanged:function(e){e.target.value=e.target.checked}},mounted:function(){flatpickr(".datetime",{enableTime:!0})}},be=we,ge=(r("70d0"),Object(f["a"])(be,de,ve,!1,null,"6da05f96",null)),_e=ge.exports,Re={props:{row:Object,schema:Object},components:{InputField:_e,KeySelect:he},methods:{getValue:function(e){var t=this.row?this.row[e.toLowerCase().replace(" ","_")]:void 0;return t}}},xe=Re,Ne=Object(f["a"])(xe,ie,ce,!1,null,null,null),ye=Ne.exports,ke={props:{tableName:String,schema:Object},components:{Modal:oe,RowForm:ye},data:function(){return{defaults:{},errors:""}},methods:{submitForm:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t){var r,n,a,s,o,i,c,u,l;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:for(console.log("I was pressed"),r=new FormData(t.target),n={},a=!0,s=!1,o=void 0,e.prev=6,i=r.entries()[Symbol.iterator]();!(a=(c=i.next()).done);a=!0)u=c.value,n[u[0]]=u[1];e.next=14;break;case 10:e.prev=10,e.t0=e["catch"](6),s=!0,o=e.t0;case 14:e.prev=14,e.prev=15,a||null==i.return||i.return();case 17:if(e.prev=17,!s){e.next=20;break}throw o;case 20:return e.finish(17);case 21:return e.finish(14);case 22:return e.prev=22,e.next=25,this.$store.dispatch("createRow",{tableName:this.tableName,data:n});case 25:e.sent,e.next=32;break;case 28:return e.prev=28,e.t1=e["catch"](22),this.errors=e.t1.response.data,e.abrupt("return");case 32:l={contents:"Successfully added row",type:"success"},this.$store.commit("updateApiResponseMessage",l),this.$emit("addedRow"),this.$emit("close");case 36:case"end":return e.stop()}},e,this,[[6,10,14,22],[15,,17,21],[22,28]])}));function t(t){return e.apply(this,arguments)}return t}()},mounted:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){var t;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.$store.dispatch("getNew",this.tableName);case 2:t=e.sent,this.defaults=t.data;case 4:case"end":return e.stop()}},e,this)}));function t(){return e.apply(this,arguments)}return t}()},$e=ke,Oe=Object(f["a"])($e,Z,ee,!1,null,"6f1e1063",null),je=Oe.exports,Ce=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("h1",[e._v("Filter")]),r("form",{ref:"form",on:{submit:function(t){return t.preventDefault(),e.submitForm(t)}}},[r("RowForm",{attrs:{schema:e.schema}}),r("button",[e._v("Apply")])],1),r("button",{on:{click:function(t){return t.preventDefault(),e.clearFilters(t)}}},[e._v("Clear filters")])])},Se=[],Te=n["a"].extend({components:{RowForm:ye},computed:{schema:function(){return this.$store.state.schema},tableName:function(){return this.$store.state.currentTableName}},methods:{submitForm:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t){var r,n,a,s,o,i,c,u;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:for(r=new FormData(t.target),n={},a=!0,s=!1,o=void 0,e.prev=5,i=r.entries()[Symbol.iterator]();!(a=(c=i.next()).done);a=!0)u=c.value,u[1]&&(n[u[0].replace(" ","_")]=u[1]);e.next=13;break;case 9:e.prev=9,e.t0=e["catch"](5),s=!0,o=e.t0;case 13:e.prev=13,e.prev=14,a||null==i.return||i.return();case 16:if(e.prev=16,!s){e.next=19;break}throw o;case 19:return e.finish(16);case 20:return e.finish(13);case 21:return e.next=23,this.$store.dispatch("fetchRows",{tableName:this.tableName,params:n});case 23:case"end":return e.stop()}},e,this,[[5,9,13,21],[14,,16,20]])}));function t(t){return e.apply(this,arguments)}return t}(),clearFilters:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){var t;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return console.log("Clearing ..."),t=this.$refs.form,t.reset(),e.next=5,this.$store.dispatch("fetchRows",{tableName:this.tableName,params:{}});case 5:case"end":return e.stop()}},e,this)}));function t(){return e.apply(this,arguments)}return t}()}}),De=Te,Fe=Object(f["a"])(De,Ce,Se,!1,null,"39af712e",null),Pe=Fe.exports,Ae=n["a"].extend({props:["tableName"],data:function(){return{showAddRow:!1,showFilter:!1}},components:{AddRow:je,BaseView:J,RowFilter:Pe,TableNav:M},computed:{cellNames:function(){var e=[];for(var t in this.rows[0])t.endsWith("_readable")||e.push(t);return e},rows:function(){return this.$store.state.rows},schema:function(){return this.$store.state.schema}},methods:{isForeignKey:function(e){var t=this.schema.properties[e];return void 0!=t&&t.foreign_key},getTableName:function(e){return this.schema.properties[e].to},deleteRow:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t){return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:if(!confirm("Are you sure you want to delete row ".concat(t,"?"))){e.next=6;break}return console.log("Deleting!"),e.next=4,this.$store.dispatch("deleteRow",{tableName:this.tableName,rowID:t});case 4:return e.next=6,this.fetchRows();case 6:case"end":return e.stop()}},e,this)}));function t(t){return e.apply(this,arguments)}return t}(),fetchRows:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.$store.dispatch("fetchRows",{tableName:this.tableName,params:{}});case 2:case"end":return e.stop()}},e,this)}));function t(){return e.apply(this,arguments)}return t}(),fetchSchema:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.$store.dispatch("fetchSchema",this.tableName);case 2:case"end":return e.stop()}},e,this)}));function t(){return e.apply(this,arguments)}return t}()},watch:{"$route.params.tableName":function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t){return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return this.$store.commit("updateCurrentTablename",this.tableName),this.$store.commit("updateRows",[]),e.next=4,Promise.all([this.fetchRows(),this.fetchSchema()]);case 4:case"end":return e.stop()}},e,this)}));function t(t){return e.apply(this,arguments)}return t}()},mounted:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return this.$store.commit("updateCurrentTablename",this.tableName),e.next=3,Promise.all([this.fetchRows(),this.fetchSchema()]);case 3:case"end":return e.stop()}},e,this)}));function t(){return e.apply(this,arguments)}return t}()}),Ee=Ae,Le=(r("965b"),Object(f["a"])(Ee,Q,Y,!1,null,null,null)),Me=Le.exports,Ie=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("NavBar"),e.schema?r("div",{staticClass:"edit_wrapper"},[r("p",[r("a",{attrs:{href:"#"},on:{click:function(t){return t.preventDefault(),e.$router.go(-1)}}},[e._v("Back")])]),r("h1",[e._v("Edit")]),r("form",{on:{submit:function(t){return t.preventDefault(),e.submitForm(t)}}},[r("RowForm",{attrs:{schema:e.schema,row:e.selectedRow}}),r("button",[e._v("Save")])],1)]):e._e()],1)},Be=[],Ue=n["a"].extend({props:["tableName","rowID"],components:{RowForm:ye,NavBar:S},computed:{schema:function(){return this.$store.state.schema},selectedRow:function(){return this.$store.state.selectedRow}},methods:{submitForm:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t){var r,n,a,s,o,i,c,u,l;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:for(console.log("Submitting..."),r=new FormData(t.target),n={},a=!0,s=!1,o=void 0,e.prev=6,i=r.entries()[Symbol.iterator]();!(a=(c=i.next()).done);a=!0)u=c.value,n[u[0].replace(" ","_")]=u[1];e.next=14;break;case 10:e.prev=10,e.t0=e["catch"](6),s=!0,o=e.t0;case 14:e.prev=14,e.prev=15,a||null==i.return||i.return();case 17:if(e.prev=17,!s){e.next=20;break}throw o;case 20:return e.finish(17);case 21:return e.finish(14);case 22:l={tableName:this.tableName,rowID:this.rowID,data:n},this.$store.dispatch("updateRow",l);case 24:case"end":return e.stop()}},e,this,[[6,10,14,22],[15,,17,21]])}));function t(t){return e.apply(this,arguments)}return t}()},mounted:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return this.$store.commit("updateCurrentTablename",this.tableName),e.next=3,Promise.all([this.$store.dispatch("fetchSingleRow",{tableName:this.tableName,rowID:this.rowID}),this.$store.dispatch("fetchSchema",this.tableName)]);case 3:case"end":return e.stop()}},e,this)}));function t(){return e.apply(this,arguments)}return t}()}),Ve=Ue,Ke=(r("be47"),Object(f["a"])(Ve,Ie,Be,!1,null,null,null)),qe=Ke.exports,He=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"login"}},[r("h1",[e._v("Login")]),r("form",{on:{submit:function(t){return t.preventDefault(),e.login(t)}}},[r("label",[e._v("Username")]),r("input",{directives:[{name:"model",rawName:"v-model",value:e.username,expression:"username"}],attrs:{type:"text"},domProps:{value:e.username},on:{input:function(t){t.target.composing||(e.username=t.target.value)}}}),r("label",[e._v("Password")]),r("input",{directives:[{name:"model",rawName:"v-model",value:e.password,expression:"password"}],attrs:{type:"password"},domProps:{value:e.password},on:{input:function(t){t.target.composing||(e.password=t.target.value)}}}),r("button",[e._v("Login")])])])},Je=[],We={data:function(){return{username:"",password:""}},methods:{login:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(){var t;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return console.log("Logging in"),e.prev=1,e.next=4,c.a.post("./api/login/",{username:this.username,password:this.password});case 4:e.sent,e.next=13;break;case 7:return e.prev=7,e.t0=e["catch"](1),console.log("Request failed"),console.log(e.t0.response),this.$store.commit("updateApiResponseMessage",{contents:"Problem logging in",type:"error"}),e.abrupt("return");case 13:return e.next=15,c.a.get("./api/user/");case 15:t=e.sent,this.$store.commit("updateUser",t.data),this.$router.push({name:"home"});case 18:case"end":return e.stop()}},e,this,[[1,7]])}));function t(){return e.apply(this,arguments)}return t}()}},Xe=We,ze=(r("4fde"),Object(f["a"])(Xe,He,Je,!1,null,null,null)),Ge=ze.exports;n["a"].use(_["a"]);var Qe=new _["a"]({mode:"hash",base:"",routes:[{path:"/",name:"home",component:G},{path:"/login/",name:"login",component:Ge},{path:"/:tableName/",name:"rowListing",component:Me,props:!0},{path:"/:tableName/:rowID/",name:"editRow",component:qe,props:!0}]}),Ye=r("2f62");n["a"].use(Ye["a"]);var Ze="./api/",et=new Ye["a"].Store({state:{tableNames:[],currentTableName:void 0,rows:[],schema:void 0,selectedRow:void 0,apiResponseMessage:null,user:void 0},mutations:{updateTableNames:function(e,t){e.tableNames=t},updateCurrentTablename:function(e,t){e.currentTableName=t},updateRows:function(e,t){e.rows=t},updateSelectedRow:function(e,t){e.selectedRow=t},updateSchema:function(e,t){e.schema=t},updateApiResponseMessage:function(e,t){e.apiResponseMessage=t},updateUser:function(e,t){e.user=t}},actions:{fetchTableNames:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t){var r;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.a.get("".concat(Ze,"tables/"));case 2:r=e.sent,this.commit("updateTableNames",r.data);case 4:case"end":return e.stop()}},e,this)}));function t(t){return e.apply(this,arguments)}return t}(),fetchRows:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t,r){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,c.a.get("".concat(Ze,"tables/").concat(r.tableName,"/?readable=true"),{params:r.params});case 3:return n=e.sent,t.commit("updateRows",n.data.rows),e.abrupt("return",n);case 8:e.prev=8,e.t0=e["catch"](0),console.log(e.t0.response),t.commit("updateApiResponseMessage",{contents:"Problem fetching ".concat(r.tableName," rows."),type:"error"});case 12:case"end":return e.stop()}},e,null,[[0,8]])}));function t(t,r){return e.apply(this,arguments)}return t}(),fetchIds:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t,r){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.a.get("".concat(Ze,"tables/").concat(r,"/ids/"));case 2:return n=e.sent,e.abrupt("return",n);case 4:case"end":return e.stop()}},e)}));function t(t,r){return e.apply(this,arguments)}return t}(),getNew:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t,r){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.a.get("".concat(Ze,"tables/").concat(r,"/new/"));case 2:return n=e.sent,e.abrupt("return",n);case 4:case"end":return e.stop()}},e)}));function t(t,r){return e.apply(this,arguments)}return t}(),fetchSingleRow:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t,r){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.a.get("".concat(Ze,"tables/").concat(r.tableName,"/").concat(r.rowID,"/"));case 2:return n=e.sent,t.commit("updateSelectedRow",n.data),e.abrupt("return",n);case 5:case"end":return e.stop()}},e)}));function t(t,r){return e.apply(this,arguments)}return t}(),fetchSchema:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t,r){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.a.get("".concat(Ze,"tables/").concat(r,"/schema/"));case 2:return n=e.sent,t.commit("updateSchema",n.data),e.abrupt("return",n);case 5:case"end":return e.stop()}},e)}));function t(t,r){return e.apply(this,arguments)}return t}(),createRow:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t,r){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.a.post("".concat(Ze,"tables/").concat(r.tableName,"/"),r.data);case 2:return n=e.sent,e.abrupt("return",n);case 4:case"end":return e.stop()}},e)}));function t(t,r){return e.apply(this,arguments)}return t}(),deleteRow:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t,r){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.a.delete("".concat(Ze,"tables/").concat(r.tableName,"/").concat(r.rowID,"/"));case 2:return n=e.sent,e.abrupt("return",n);case 4:case"end":return e.stop()}},e)}));function t(t,r){return e.apply(this,arguments)}return t}(),updateRow:function(){var e=Object(o["a"])(regeneratorRuntime.mark(function e(t,r){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.a.put("".concat(Ze,"tables/").concat(r.tableName,"/").concat(r.rowID,"/"),r.data);case 2:return n=e.sent,t.commit("updateApiResponseMessage",{contents:"Successfully saved row",type:"success"}),e.abrupt("return",n);case 5:case"end":return e.stop()}},e)}));function t(t,r){return e.apply(this,arguments)}return t}()}}),tt=r("ad3d"),rt=r("ecee"),nt=r("c074"),at=r("a78e"),st=r.n(at);rt["c"].add(nt["e"],nt["c"],nt["b"],nt["i"],nt["j"],nt["d"],nt["g"],nt["h"],nt["f"],nt["a"]),n["a"].component("font-awesome-icon",tt["a"]),c.a.interceptors.request.use(function(e){if(-1!=["POST","PUT","DELETE"].indexOf(e.method.toUpperCase())){var t=st.a.get("csrftoken");e.headers["X-CSRFToken"]=t}return e}),n["a"].config.productionTip=!1,new n["a"]({router:Qe,store:et,render:function(e){return e(g)}}).$mount("#app")},d3a5:function(e,t,r){},df73:function(e,t,r){"use strict";var n=r("8233"),a=r.n(n);a.a},e869:function(e,t,r){"use strict";var n=r("d3a5"),a=r.n(n);a.a}});
//# sourceMappingURL=app.41faf446.js.map