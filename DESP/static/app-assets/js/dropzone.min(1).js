!function(e,i,l){"use strict";Dropzone.options.dpzSingleFile={paramName:"file",maxFiles:1,init:function(){this.on("maxfilesexceeded",function(e){this.removeAllFiles(),this.addFile(e)})}},Dropzone.options.dpzMultipleFiles={paramName:"file",maxFilesize:.5,clickable:!0},new Dropzone(i.body,{url:"#",previewsContainer:"#dpz-btn-select-files",clickable:"#select-files"}),Dropzone.options.dpzFileLimits={paramName:"file",maxFilesize:.5,maxFiles:5,maxThumbnailFilesize:1},Dropzone.options.dpAcceptFiles={paramName:"file",maxFilesize:1,acceptedFiles:"image/*"},Dropzone.options.dpzRemoveThumb={paramName:"file",maxFilesize:1,addRemoveLinks:!0,dictRemoveFile:" Trash"},Dropzone.options.dpzRemoveAllThumb={paramName:"file",maxFilesize:1,init:function(){var e=this;l("#clear-dropzone").on("click",function(){e.removeAllFiles()})}}}(window,document,jQuery);