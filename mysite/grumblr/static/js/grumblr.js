
var req;

function sendRequest(){
	if (window.XMLHttpRequest){
		req= new XMLHttpRequest();
	}else{
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	req.onreadystatechange = handleResponse;
	req.open("GET","/grumblr/get_mygrumbl", true)
	req.send();
}

function handleResponse(){
	if(req.readyState != 4 || req.status !=200){
		return;
	}
	var list = document.getElementById("allMyGrumbl");
	var allItems = JSON.parse(req.responseText);
	while(list.hasChildNodes()){

	}

}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function sendComment(grumblrid,p,personid,first_name){
	var t = $("#comment_content").val();

	var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
	var obj={page: p, text:t, csrfmiddlewaretoken:csrftoken,id:grumblrid};
	var target = $(this)
	$.ajax({
		type:"POST",
		url:"/grumblr/add_comment/".concat(grumblrid),
		data:obj,
		success:function(first_name,t){
			$("#all_comments").append(("<div class='row'>") +first_name + ": "+ t + "</div>");
			// $("#all_comments").append("<div class='row'>"+first_name+": "+t+"</p>"));
		},

	})
};



window.setInterval(sendRequest,1000);