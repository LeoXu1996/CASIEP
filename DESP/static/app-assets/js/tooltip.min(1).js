!function(t,o,i){"use strict";i(function(){i('[data-toggle="tooltip"]').tooltip()}),i("#show-tooltip").tooltip({title:"Tooltip Show Event",trigger:"click",placement:"right"}).on("show.bs.tooltip",function(){alert("Show event fired.")}),i("#shown-tooltip").tooltip({title:"Tooltip Shown Event",trigger:"click",placement:"top"}).on("shown.bs.tooltip",function(){alert("Shown event fired.")}),i("#hide-tooltip").tooltip({title:"Tooltip Hide Event",trigger:"click",placement:"bottom"}).on("hide.bs.tooltip",function(){alert("Hide event fired.")}),i("#hidden-tooltip").tooltip({title:"Tooltip Hidden Event",trigger:"click",placement:"left"}).on("hidden.bs.tooltip",function(){alert("Hidden event fired.")}),i("#show-method").on("click",function(){i(this).tooltip("show")}),i("#hide-method").on("mouseenter",function(){i(this).tooltip("show")}),i("#hide-method").on("click",function(){i(this).tooltip("hide")}),i("#toggle-method").on("click",function(){i(this).tooltip("toggle")}),i("#dispose").on("click",function(){i("#dispose-method").tooltip("dispose")}),i(".manual").on("click",function(){i(this).tooltip("show")}),i(".manual").on("mouseout",function(){i(this).tooltip("hide")}),i(".template").on("click",function(){console.log('<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>')})}(window,document,jQuery);