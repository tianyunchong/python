$(document).ready(function(){
	$("#analy").live("click", function(){
		//第一步，请求获取当前链接所有的url入库
		$.ajax({
			"url"     : "/index/urls/analy/init/",
			"data"    : "id="+id,
			"type"    : "GET",
			"dataType": "json",
			"async"   : false,
			"success" : function(msg) {
				if (msg.status && msg.message) {
				    $(".well.well-lg").html("");
				    $(".well.well-lg").append(msg.message+"<br>")
					return true;
				}
				$(".alert.alert-danger").html(msg.message).show();
			}
		});
	});
});