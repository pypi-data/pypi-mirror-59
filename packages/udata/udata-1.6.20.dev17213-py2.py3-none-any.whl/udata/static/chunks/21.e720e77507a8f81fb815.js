webpackJsonp([21],{296:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o=2;t.default={name:"pagination-widget",props:{p:Object},computed:{start:function(){return this.p?this.p.page<=o?1:this.p.page-o:-1},end:function(){return this.p?this.p.page+o>this.p.pages?this.p.pages:this.p.page+o:-1},range:function(){var e=this;return isNaN(this.start)||isNaN(this.end)||this.start>=this.end?[]:Array.apply(0,Array(this.end+1-this.start)).map(function(t,o){return o+e.start})}}}},297:function(e,t){e.exports=' <ul class="pagination pagination-sm no-margin" v-show="p && p.pages > 1"> <li :class="{ \'disabled\': !p || p.page == 1 }"> <a :title="_(\'First page\')" class=pointer @click=p.go_to_page(1)> &laquo; </a> </li> <li :class="{ \'disabled\': !p || p.page == 1 }"> <a :title="_(\'Previous page\')" class=pointer @click=p.previousPage()> &lsaquo; </a> </li> <li v-for="current in range" :class="{ \'active\': current == p.page }"> <a @click=p.go_to_page(current) class=pointer>{{ current }}</a> </li> <li :class="{ \'disabled\': !p || p.page == p.pages }"> <a :title="_(\'Next page\')" class=pointer @click=p.nextPage()> &rsaquo; </a> </li> <li :class="{ \'disabled\': !p || p.page == p.pages }"> <a :title="_(\'Last page\')" class=pointer @click=p.go_to_page(p.pages)> &raquo; </a> </li> </ul> '},298:function(e,t,o){var s,i;s=o(296),i=o(297),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},400:function(e,t,o){var s,i;o(404),s=o(401),i=o(403),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},401:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"box",props:{title:String,icon:null,boxclass:{type:String,default:""},bodyclass:{type:String,default:""},footerclass:{type:String,default:""},loading:Boolean,footer:null}}},402:function(e,t,o){t=e.exports=o(8)(),t.push([e.id,".box .box-tools>*{float:right}.box .box-tools .text-muted{color:#777!important}.box .box-tools .box-search{width:180px;display:inline-block}.box .box-tools .box-search input:focus{box-shadow:none;border-color:transparent!important}.box .box-tools .box-search .btn,.box .box-tools .box-search input[type=text]{box-shadow:none;background-color:#fbfbfb;border:1px solid #fbfbfb}.box .box-tools .box-search .btn:focus,.box .box-tools .box-search input[type=text]:focus{background-color:#fff;color:#666}.box .box-tools .box-search .btn:focus+.input-group-btn .btn,.box .box-tools .box-search input[type=text]:focus+.input-group-btn .btn{background-color:#fff;border-left-color:#fff;color:#666}.box .box-tools .box-search>*{border-top:1px solid #eee;border-bottom:1px solid #eee}.box .box-tools .box-search>:first-child{border-left:1px solid #eee}.box .box-tools .box-search>:last-child{border-right:1px solid #eee}.box .box-tools .btn-box-tool{font-size:14px;padding:6px 8px}.box .box-tools .btn-group{vertical-align:inherit}.box form{margin:10px}","",{version:3,sources:["/./js/components/containers/box.vue"],names:[],mappings:"AAAA,kBAAkB,WAAW,CAAC,4BAA4B,oBAAqB,CAAC,4BAA4B,YAAY,oBAAoB,CAAC,wCAAwC,gBAAgB,kCAAmC,CAAC,8EAAgF,gBAAgB,yBAAyB,wBAAwB,CAAC,0FAA4F,sBAAsB,UAAU,CAAC,sIAAwI,sBAAsB,uBAAuB,UAAU,CAAC,8BAA8B,0BAA0B,4BAA4B,CAAC,yCAA0C,0BAA0B,CAAC,wCAAyC,2BAA2B,CAAC,8BAA8B,eAAe,eAAe,CAAC,2BAA2B,sBAAsB,CAAC,UAAU,WAAW,CAAC",file:"box.vue",sourcesContent:['.box .box-tools>*{float:right}.box .box-tools .text-muted{color:#777 !important}.box .box-tools .box-search{width:180px;display:inline-block}.box .box-tools .box-search input:focus{box-shadow:none;border-color:transparent !important}.box .box-tools .box-search input[type="text"],.box .box-tools .box-search .btn{box-shadow:none;background-color:#fbfbfb;border:1px solid #fbfbfb}.box .box-tools .box-search input[type="text"]:focus,.box .box-tools .box-search .btn:focus{background-color:#fff;color:#666}.box .box-tools .box-search input[type="text"]:focus+.input-group-btn .btn,.box .box-tools .box-search .btn:focus+.input-group-btn .btn{background-color:#fff;border-left-color:#fff;color:#666}.box .box-tools .box-search>*{border-top:1px solid #eee;border-bottom:1px solid #eee}.box .box-tools .box-search>*:first-child{border-left:1px solid #eee}.box .box-tools .box-search>*:last-child{border-right:1px solid #eee}.box .box-tools .btn-box-tool{font-size:14px;padding:6px 8px}.box .box-tools .btn-group{vertical-align:inherit}.box form{margin:10px}'],sourceRoot:"webpack://"}])},403:function(e,t){e.exports=' <div class="box {{ boxclass }}"> <header class=box-header v-show="title || icon"> <i v-show=icon class="fa fa-{{icon}}"></i> <h3 class=box-title>{{title}}</h3> <div class=box-tools> <slot name=tools></slot> </div> </header> <div class="box-body {{bodyclass}}"> <slot></slot> </div> <div class=overlay v-show=loading> <span class="fa fa-refresh fa-spin"></span> </div> <div class="box-footer clearfix {{footerclass}}" v-show=footer> <slot name=footer></slot> </div> </div> '},404:function(e,t,o){var s=o(402);"string"==typeof s&&(s=[[e.id,s,""]]);o(9)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},418:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"small-box",props:{value:null,label:String,icon:String,color:{type:String,default:"aqua"},target:null},computed:{bgcolor:function(){return"bg-"+this.color},faicon:function(){return"fa-"+this.icon}},methods:{click:function(){this.target&&("#"===this.target[0]?this.$scrollTo(this.target):this.$go?this.$go(this.target):window.location=this.target),this.$dispatch("small-box:click",this)}}}},419:function(e,t,o){t=e.exports=o(8)(),t.push([e.id,".small-box{overflow:hidden}","",{version:3,sources:["/./js/components/containers/small-box.vue"],names:[],mappings:"AAAA,WAAW,eAAe,CAAC",file:"small-box.vue",sourcesContent:[".small-box{overflow:hidden}"],sourceRoot:"webpack://"}])},420:function(e,t){e.exports=' <div> <a class="small-box pointer" :class="[ bgcolor ]" @click=click> <div class=inner> <h3>{{value | numbers}}</h3> <p>{{label}}</p> </div> <div class=icon> <i class=fa :class="[ faicon ]"></i> </div> <div v-if=target class=small-box-footer> <span v-i18n="More infos"></span> <i class="fa fa-arrow-circle-right"></i> </div> </a> </div> '},421:function(e,t,o){var s,i;o(422),s=o(418),i=o(420),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},422:function(e,t,o){var s=o(419);"string"==typeof s&&(s=[[e.id,s,""]]);o(9)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1145:function(e,t,o){var s,i;s=o(1659),i=o(1760),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1256:function(e,t,o){var s,i;o(1384),s=o(1324),i=o(1363),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1287:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(625),i=_interopRequireDefault(s);t.default={name:"layout",props:{title:String,subtitle:String,page:String,actions:{type:Array,default:function(){return[]}},badges:Array},components:{NotificationZone:i.default},computed:{main_action:function(){if(this.actions.length)return this.actions[0]},menu_actions:function(){if(this.actions&&this.actions.length>1)return this.actions.slice(1)}}}},1288:function(e,t,o){t=e.exports=o(8)(),t.push([e.id,".content-header h1 a{color:#000}.content-header h1 a .fa{font-size:.4em}","",{version:3,sources:["/./js/components/layout.vue"],names:[],mappings:"AAAA,qBAAqB,UAAW,CAAC,yBAAyB,cAAc,CAAC",file:"layout.vue",sourcesContent:[".content-header h1 a{color:black}.content-header h1 a .fa{font-size:.4em}"],sourceRoot:"webpack://"}])},1289:function(e,t){e.exports=' <div class=content-wrapper> <router-view></router-view> <section class=content-header> <div v-if=main_action class="btn-group btn-group-sm btn-actions pull-right clearfix"> <div v-if=menu_actions class="btn-group btn-group-sm" role=group> <button type=button class="btn btn-info" @click=main_action.method> <span v-if=main_action.icon class="fa fa-fw fa-{{main_action.icon}}"></span> {{main_action.label}} </button> <button type=button class="btn btn-info dropdown-toggle" data-toggle=dropdown> <span class=caret></span> <span class=sr-only>Toggle Dropdown</span> </button> <ul class="dropdown-menu dropdown-menu-right" role=menu> <li v-for="action in menu_actions" :role="action.divider ? \'separator\' : false" :class="{ \'divider\': action.divider }"> <a class=pointer v-if=!action.divider @click=action.method> <span v-if=action.icon class="fa fa-fw fa-{{action.icon}}"></span> {{action.label}} </a> </li> </ul> </div> <button v-if=!menu_actions type=button class="btn btn-info btn-sm" @click=main_action.method> <span v-if=main_action.icon class="fa fa-fw fa-{{main_action.icon}}"></span> {{main_action.label}} </button> </div> <h1> <a v-if=page :href=page :title="_(\'See on the site\')"> {{ title }} <span class="fa fa-external-link"></span> </a> <span v-if=!page>{{title}}</span> <small v-if=subtitle>{{subtitle}}</small> <small v-if=badges> <span v-for="badge in badges" class="label label-{{badge.class}}">{{badge.label}}</span> </small> </h1> </section> <notification-zone></notification-zone> <section class=content> <slot></slot> </section> </div> '},1290:function(e,t,o){var s,i;o(1291),s=o(1287),i=o(1289),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1291:function(e,t,o){var s=o(1288);"string"==typeof s&&(s=[[e.id,s,""]]);o(9)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1305:function(e,t,o){function webpackContext(e){return o(webpackContextResolve(e))}function webpackContextResolve(e){return s[e]||function(){throw new Error("Cannot find module '"+e+"'.")}()}var s={"./avatar.vue":1365,"./date.vue":1366,"./datetime.vue":1367,"./deletable-text.vue":1368,"./label.vue":1369,"./metric.vue":1370,"./playpause.vue":1371,"./progress-bars.vue":1372,"./since.vue":1373,"./text.vue":1374,"./thumbnail.vue":1375,"./timeago.vue":1376,"./visibility.vue":1377};webpackContext.keys=function(){return Object.keys(s)},webpackContext.resolve=webpackContextResolve,e.exports=webpackContext,webpackContext.id=1305},1308:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(31),i=(_interopRequireDefault(s),o(283)),a=_interopRequireDefault(i);t.default={name:"datatable-cell",default:"",props:{field:Object,item:Object},computed:{value:function(){if(!this.field||!this.item)return this.$options.default;if(this.field.key)if(a.default.isFunction(this.field.key))t=this.field.key(this.item);else for(var e=this.field.key.split("."),t=this.item,o=0;o<e.length;o++){var s=e[o];if(!t||!t.hasOwnProperty(s)){t=null;break}t=t[s]}else t=this.item;return t||this.$options.default}}}},1309:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={attached:function(){this.$el.closest("td").classList.add("avatar-cell")}}},1310:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-date"}},1311:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-datetime"}},1312:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-deletable-text"}},1313:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-label",filters:{format:function(e){return this.field.hasOwnProperty("label_func")?this.field.label_func(e):e},color:function(e){return this.field.hasOwnProperty("label_type")?this.field.label_type(e):"default"}},computed:{labels:function(){return this.value instanceof Array?this.value:[this.value]}}}},1314:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-metric",default:0}},1315:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-playpause",default:!1}},1316:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-progress-bars",computed:{progress_class:function(){return this.value<2?"danger":this.value<5?"warning":this.value<9?"primary":"success"}}}},1317:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-since"}},1318:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-text"}},1319:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(73),i=_interopRequireDefault(s);t.default={attached:function(){this.$el.closest("td").classList.add("thumbnail-cell")},computed:{src:function(){return this.value?this.value:this.field.placeholder?i.default.getFor(this.field.placeholder):i.default.generic}}}},1320:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-timeago"}},1321:function(e,t,o){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=o(52),i={deleted:{label:(0,s._)("Deleted"),type:"danger"},private:{label:(0,s._)("Private"),type:"warning"},public:{label:(0,s._)("Public"),type:"info"}};t.default={name:"datatable-cell-visibility",computed:{type:function(){if(this.item)return this.item.deleted?i.deleted.type:this.item.private?i.private.type:i.public.type},text:function(){if(this.item)return this.item.deleted?i.deleted.label:this.item.private?i.private.label:i.public.label}}}},1322:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(295),i=_interopRequireDefault(s),a=o(31),n=_interopRequireDefault(a),l=o(1364),r=_interopRequireDefault(l);t.default={name:"datatable-row",props:{item:Object,fields:Array,selected:{type:Boolean,default:!1}},created:function(){var e=!0,t=!1,o=void 0;try{for(var s,a=(0,i.default)(this.fields);!(e=(s=a.next()).done);e=!0){var n=s.value;this.load_cell(n.type||"text")}}catch(l){t=!0,o=l}finally{try{!e&&a.return&&a.return()}finally{if(t)throw o}}},methods:{item_click:function(e){this.$dispatch("datatable:item:click",e)},load_cell:function(e){if(!this.$options.components.hasOwnProperty(e)){var t=o(1305)("./"+e+".vue");t.hasOwnProperty("mixins")||(t.mixins=[]),r.default in t.mixins||t.mixins.push(r.default),this.$options.components[e]=n.default.extend(t)}}}}},1323:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(1378),i=_interopRequireDefault(s);t.default={name:"datatable",components:{Row:i.default},props:{p:Object,fields:Array,track:{type:null,default:"id"}},data:function(){return{selected:null}},computed:{remote:function(){return this.p&&this.p.serverside},trackBy:function(){return this.track||""}},events:{"datatable:item:click":function(e){return this.selected=e,!0}},methods:{header_click:function(e){e.sort&&this.p.sort(this.sort_for(e))},sort_for:function(e){return this.remote?e.sort:e.key},classes_for:function(e){var t={pointer:Boolean(e.sort)},o=e.align||"left";return t["text-"+o]=!0,t},sort_classes_for:function(e){var t={};return this.p.sorted!=this.sort_for(e)?t["fa-sort"]=!0:this.p.reversed?this.p.reversed&&(t["fa-sort-desc"]=!0):t["fa-sort-asc"]=!0,t}},filters:{thwidth:function(e){switch(e){case void 0:return"";case 0:return 0;default:return e+5}}}}},1324:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(400),i=_interopRequireDefault(s),a=o(1379),n=_interopRequireDefault(a),l=o(298),r=_interopRequireDefault(l);t.default={name:"datatable-widget",components:{Box:i.default,Datatable:n.default,PaginationWidget:r.default},data:function(){return{search_query:null,selected:null}},computed:{has_footer_children:function(){return this.$els.footer_container&&this.$els.footer_container.children.length},show_footer:function(){return this.p&&this.p.pages>1||this.has_footer_children},boxclasses:function(){return["datatable-widget",this.tint?"box-"+this.tint:"box-solid",this.boxclass].join(" ")}},props:{p:Object,title:String,icon:String,fields:Array,boxclass:String,tint:String,empty:String,loading:{type:Boolean,default:void 0},track:{type:null,default:"id"},downloads:{type:Array,default:function(){return[]}}},methods:{search:function(){this.p.search(this.search_query)}},watch:{search_query:function(e){this.p.search(e)}}}},1340:function(e,t,o){t=e.exports=o(8)(),t.push([e.id,".datatable td.ellipsis{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:0}","",{version:3,sources:["/./js/components/datatable/cell.vue"],names:[],mappings:"AAAA,uBAAuB,mBAAmB,gBAAgB,uBAAuB,WAAW,CAAC",file:"cell.vue",sourcesContent:[".datatable td.ellipsis{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:0}"],sourceRoot:"webpack://"}])},1341:function(e,t,o){t=e.exports=o(8)(),t.push([e.id,".datatable td.avatar-cell{padding:3px}","",{version:3,sources:["/./js/components/datatable/cells/avatar.vue"],names:[],mappings:"AAAA,0BAA0B,WAAW,CAAC",file:"avatar.vue",sourcesContent:[".datatable td.avatar-cell{padding:3px}"],sourceRoot:"webpack://"}])},1342:function(e,t,o){t=e.exports=o(8)(),t.push([e.id,".datatable td.thumbnail-cell{padding:3px}","",{version:3,sources:["/./js/components/datatable/cells/thumbnail.vue"],names:[],mappings:"AAAA,6BAA6B,WAAW,CAAC",file:"thumbnail.vue",sourcesContent:[".datatable td.thumbnail-cell{padding:3px}"],sourceRoot:"webpack://"}])},1343:function(e,t,o){t=e.exports=o(8)(),t.push([e.id,".datatable th{white-space:nowrap}","",{version:3,sources:["/./js/components/datatable/table.vue"],names:[],mappings:"AAAA,cAAc,kBAAkB,CAAC",file:"table.vue",sourcesContent:[".datatable th{white-space:nowrap}"],sourceRoot:"webpack://"}])},1344:function(e,t,o){t=e.exports=o(8)(),t.push([e.id,".datatable-widget .datatable-header>.row{width:100%}","",{version:3,sources:["/./js/components/datatable/widget.vue"],names:[],mappings:"AAAA,yCAAyC,UAAU,CAAC",file:"widget.vue",sourcesContent:[".datatable-widget .datatable-header>.row{width:100%}"],sourceRoot:"webpack://"}])},1345:function(e,t,o){t=e.exports=o(8)(),t.push([e.id,".label{margin:1px}","",{version:3,sources:["/./js/components/datatable/cells/label.vue"],names:[],mappings:"AACA,OACI,UAAY,CACf",file:"label.vue",sourcesContent:["\n.label {\n    margin: 1px;\n}\n"],sourceRoot:"webpack://"}])},1348:function(e,t){e.exports=' <img :src="value | avatar_url field.width" :width=field.width :height=field.width /> '},1349:function(e,t){e.exports=' <time :datetime="value | dt YYYY-MM-DD">{{value | dt L}}</time> '},1350:function(e,t){e.exports=" <time :datetime=value>{{value | dt L LT}}</time> "},1351:function(e,t){e.exports=" <del v-if=item.deleted :title=\"_('This item has been deleted')\" :datetime=item.deleted>{{value}}</del> <span v-else>{{value}}</span> "},1352:function(e,t){e.exports=' <span v-for="label in labels" class="label label-{{label | color}}"> {{label | format}} </span> '},1353:function(e,t){e.exports=" <span class=badge :class=\"{\n    'bg-green': value > 0,\n    'bg-red': value == 0\n    }\">{{value}}</span> "},1354:function(e,t){e.exports=" <i class=\"fa fa-fw fa-{{value ? 'play' : 'stop'}} text-{{value ? 'green' : 'red'}}\"></i> "},1355:function(e,t){e.exports=' <div class="progress progress-sm"> <span class="progress-bar progress-bar-{{ progress_class }}" :style="{width: value + 1 + \'0%\'}" :title="_(\'Score:\') + \' \' + value"> </span> </div> '},1356:function(e,t){e.exports=" <time :datetime=value>{{value | since}}</time> "},1357:function(e,t){e.exports="<span>{{value}}</span>"},1358:function(e,t){e.exports=" <img :src=src :width=field.width :height=field.width /> "},1359:function(e,t){e.exports=" <time :datetime=value class=timeago>{{value | timeago}}</time> "},1360:function(e,t){e.exports=' <span class="label label-{{type}}">{{text}}</span> '},1361:function(e,t){e.exports=" <tr class=pointer :class=\"{ 'active': selected }\" @click=item_click(item)> <td v-for=\"field in fields\" track-by=key :class=\"{\n            'text-center': field.align === 'center',\n            'text-left': field.align === 'left',\n            'text-right': field.align === 'right',\n            'ellipsis': field.ellipsis\n        }\"> <component :is=\"field.type || 'text'\" :item=item :field=field> </component> </td> </tr> "},1362:function(e,t){e.exports=' <table class="table table-hover datatable"> <thead> <tr> <th v-for="field in fields" :class=classes_for(field) @click=header_click(field) :width="field.width | thwidth"> {{field.label}} <span class="fa fa-fw" v-if=field.sort :class=sort_classes_for(field)></span> </th> </tr> </thead> <tbody> <tr v-for="item in p.data" :track-by=trackBy is=row :item=item :fields=fields :selected="item === selected"> </tr> </tbody> </table> '},1363:function(e,t){e.exports=' <div> <box :title=title :icon=icon :boxclass=boxclasses bodyclass="table-responsive no-padding" footerclass="text-center clearfix" :loading="loading !== undefined ? loading : p.loading" :footer=show_footer> <aside slot=tools> <div class=btn-group v-show=downloads.length> <button type=button class="btn btn-box-tool dropdown-toggle" data-toggle=dropdown aria-expanded=false> <span class="fa fa-download"></span> </button> <ul class=dropdown-menu role=menu> <li v-for="download in downloads"> <a :href=download.url>{{download.label}}</a> </li> </ul> </div> <div class=box-search v-if=p.has_search> <div class=input-group> <input type=text class="form-control input-sm pull-right" style="width: 150px" :placeholder="_(\'Search\')" v-model=search_query debounce=500 @keyup.enter=search> <div class=input-group-btn> <button class="btn btn-sm btn-flat" @click=search> <i class="fa fa-search"></i> </button> </div> </div> </div> </aside> <header class=datatable-header> <slot name=header></slot> </header> <datatable v-if=p.has_data :p=p :fields=fields :track=track> </datatable> <div class="text-center lead" v-if=!p.has_data> {{ empty || _(\'No data\')}} </div> <footer slot=footer> <div :class="{ \'pull-right\': p.pages > 1 }" v-el:footer_container> <slot name=footer></slot> </div> <pagination-widget :p=p></pagination-widget> </footer> </box> </div> '},1364:function(e,t,o){var s,i;o(1380),s=o(1308),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1365:function(e,t,o){var s,i;o(1381),s=o(1309),i=o(1348),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1366:function(e,t,o){var s,i;s=o(1310),i=o(1349),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1367:function(e,t,o){var s,i;s=o(1311),i=o(1350),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1368:function(e,t,o){var s,i;s=o(1312),i=o(1351),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1369:function(e,t,o){var s,i;o(1385),s=o(1313),i=o(1352),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1370:function(e,t,o){var s,i;s=o(1314),i=o(1353),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1371:function(e,t,o){var s,i;s=o(1315),i=o(1354),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1372:function(e,t,o){var s,i;s=o(1316),i=o(1355),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1373:function(e,t,o){var s,i;s=o(1317),i=o(1356),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1374:function(e,t,o){var s,i;s=o(1318),i=o(1357),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1375:function(e,t,o){var s,i;o(1382),s=o(1319),i=o(1358),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1376:function(e,t,o){var s,i;s=o(1320),i=o(1359),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1377:function(e,t,o){var s,i;s=o(1321),i=o(1360),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1378:function(e,t,o){var s,i;s=o(1322),i=o(1361),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1379:function(e,t,o){var s,i;o(1383),s=o(1323),i=o(1362),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1380:function(e,t,o){var s=o(1340);"string"==typeof s&&(s=[[e.id,s,""]]);o(9)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1381:function(e,t,o){var s=o(1341);"string"==typeof s&&(s=[[e.id,s,""]]);o(9)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1382:function(e,t,o){var s=o(1342);"string"==typeof s&&(s=[[e.id,s,""]]);o(9)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1383:function(e,t,o){var s=o(1343);"string"==typeof s&&(s=[[e.id,s,""]]);o(9)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1384:function(e,t,o){var s=o(1344);"string"==typeof s&&(s=[[e.id,s,""]]);o(9)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1385:function(e,t,o){var s=o(1345);"string"==typeof s&&(s=[[e.id,s,""]]);o(9)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1418:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(1256),i=_interopRequireDefault(s);t.default={name:"reuses-list",components:{Datatable:i.default},MASK:["id","title","created_at","last_modified","metrics","private","image_thumbnail"],data:function(){return{fields:[{key:"image_thumbnail",type:"thumbnail",width:30},{label:this._("Title"),key:"title",sort:"title",type:"deletable-text"},{label:this._("Creation"),key:"created_at",sort:"created",align:"left",type:"timeago",width:120},{label:this._("Modification"),key:"last_modified",sort:"last_modified",align:"left",type:"timeago",width:120},{label:this._("Datasets"),key:"metrics.datasets",sort:"datasets",align:"center",type:"metric",width:135},{label:this._("Followers"),key:"metrics.followers",sort:"followers",align:"center",type:"metric",width:95},{label:this._("Views"),key:"metrics.views",sort:"views",align:"center",type:"metric",width:95},{label:this._("Status"),align:"center",type:"visibility",width:95}]}},events:{"datatable:item:click":function(e){this.$go("/reuse/"+e.id+"/")}},props:{reuses:null,downloads:{type:Array,default:function(){return[]}},title:{type:String,default:function(){return this._("Reuses")}}}}},1424:function(e,t){e.exports=" <div> <datatable :title=title icon=recycle boxclass=reuses-widget :fields=fields :p=reuses :downloads=downloads :empty=\"_('No reuse')\"> </datatable> </div> "},1427:[1867,1418,1424],1433:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(1256),i=_interopRequireDefault(s);t.default={name:"discussions-list",components:{Datatable:i.default},MASK:["id","title","created","closed","class","subject"],data:function(){return{fields:[{label:this._("Title"),key:"title",type:"text",ellipsis:!0},{label:this._("Created on"),key:"created",type:"datetime",width:200},{label:this._("Closed on"),key:"closed",type:"datetime",width:200}]}},events:{"datatable:item:click":function(e){var t=e.subject.class.toLowerCase(),o=t+"-discussion";this.$go({name:o,params:{oid:e.subject.id,discussion_id:e.id}})}},props:{discussions:null,title:{type:String,default:function(){return this._("Discussions")}}}}},1435:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(1256),i=_interopRequireDefault(s);t.default={name:"issues-list",components:{Datatable:i.default},MASK:["id","class","title","created","closed","subject"],data:function(){return{fields:[{label:this._("Title"),key:"title",type:"text",ellipsis:!0},{label:this._("Created on"),key:"created",type:"datetime",width:200},{label:this._("Closed on"),key:"closed",type:"datetime",width:200}]}},events:{"datatable:item:click":function(e){var t=e.subject.class.toLowerCase(),o=t+"-issue";this.$go({name:o,params:{oid:e.subject.id,issue_id:e.id}})}},props:{issues:null,title:{type:String,default:function(){return this._("Issues")}}}}},1438:function(e,t){e.exports=" <div> <datatable :title=title icon=comment boxclass=discussions-widget :fields=fields :p=discussions :empty=\"_('No discussion')\"> </datatable> </div> "},1439:function(e,t){e.exports=" <div> <datatable :title=title icon=warning boxclass=issues-widget :fields=fields :p=issues :empty=\"_('No issues')\"> </datatable> </div> "},1441:[1867,1433,1438],1443:[1867,1435,1439],1585:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(6),i=_interopRequireDefault(s),a=o(7),n=_interopRequireDefault(a),l=o(26),r=_interopRequireDefault(l),u=o(12),c=_interopRequireDefault(u),p=o(11),d=_interopRequireDefault(p),f=o(5),b=(_interopRequireDefault(f),o(14)),x=function(e){function MyMetrics(){return(0,n.default)(this,MyMetrics),(0,c.default)(this,(MyMetrics.__proto__||(0,i.default)(MyMetrics)).apply(this,arguments))}return(0,d.default)(MyMetrics,e),(0,r.default)(MyMetrics,[{key:"fetch",value:function(e){return this.loading=!0,this.$api("me.my_metrics",{id:e},this.on_fetched),this}}]),MyMetrics}(b.Model);t.default=x},1659:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(10),i=(_interopRequireDefault(s),o(14)),a=o(1585),n=_interopRequireDefault(a),l=o(1290),r=_interopRequireDefault(l),u=o(421),c=_interopRequireDefault(u),p=o(1427),d=_interopRequireDefault(p),f=o(1443),b=_interopRequireDefault(f),x=o(1441),h=_interopRequireDefault(x);t.default={name:"Home",data:function(){return{metrics:new n.default,reuses:new i.PageList({
ns:"me",fetch:"my_org_reuses",mask:d.default.MASK.concat(["deleted"])}),issues:new i.PageList({ns:"me",fetch:"my_org_issues",mask:b.default.MASK}),discussions:new i.PageList({ns:"me",fetch:"my_org_discussions",mask:h.default.MASK})}},computed:{dataBoxes:function(){if(!this.metrics.id||!this.reuses)return[];var e=this.metrics.datasets_count||0,t=this.metrics.datasets_org_count||0,o=this.metrics.followers_count||0,s=this.metrics.followers_org_count||0,i=this.reuses.items.length||0,a=this.metrics.resources_availability>=80;return[{value:t+" ("+e+")",label:this._("Datasets (only yours)"),icon:"cubes",color:"aqua"},{value:(this.metrics.resources_availability||0)+" %",label:this._("Availability of your datasets"),icon:a?"thumbs-up":"thumbs-down",color:a?"green":"red"},{value:s+" ("+o+")",label:this._("Followers (only yours)"),icon:"heart",color:"purple"},{value:i,label:this._("Reuses"),icon:"recycle",color:"teal"}]}},components:{SmallBox:c.default,DiscussionList:h.default,IssueList:b.default,ReuseList:d.default,Layout:r.default},attached:function(){this.update(),this._handler=this.$root.me.$on("updated",this.update.bind(this))},detached:function(){this._handler.remove()},methods:{update:function(){this.$root.me.id&&(this.metrics.fetch(),this.reuses.fetch(),this.issues.fetch(),this.discussions.fetch())}}}},1760:function(e,t){e.exports=' <div> <layout :title="_(\'Dashboard\')"> <div class=row> <small-box class="col-lg-3 col-xs-6" v-for="b in dataBoxes" :value=b.value :label=b.label :color=b.color :icon=b.icon :target=b.target> </small-box> </div> <div class=row> <reuse-list class=col-xs-12 :reuses=reuses :title="_(\'Reuses about your data (including your organizations)\')"> </reuse-list> </div> <div class=row> <issue-list id=issues-widget class=col-xs-12 :issues=issues :title="_(\'Issues about your data (including your organizations)\')"> </issue-list> </div> <div class=row> <discussion-list id=discussions-widget class=col-xs-12 :discussions=discussions :title="_(\'Discussions about your data (including your organizations)\')"> </discussion-list> </div> </layout> </div> '},1867:function(e,t,o,s,i){var a,n;a=o(s),n=o(i),e.exports=a||{},e.exports.__esModule&&(e.exports=e.exports.default),n&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=n)}});
//# sourceMappingURL=21.e720e77507a8f81fb815.js.map