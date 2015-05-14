(function(){
    console.log('app triger');


    var MainApp = function(){
	
	//function to call fetchDataFromWorldcat

	this.fetchDataFromWorldcat = function(){
	   
	    console.log('Calling fetchDataFromWorldcat');
	    var documentId = $('#documentId').val();
	    var url = 'http://localhost:8000/fetchDataFromWorldcat/' ;


	    if(documentId !== ''){
		url = url + '?documentId='+ documentId;
	    }

	    var parent = this;


	    $.ajax({
		url: url,
		type: "GET",
		success : function(response){
		    console.log(response);
		    var response = JSON.parse(response);
		    
		    if(response.message != undefined){

			console.log('Auth done already, calling save', response.document);
			functions.saveLocal('document',JSON.stringify(response.document));
			parent.saveMendeleyDocument();
		    }else{
			console.log(response.document, response.login_url);
			
			functions.saveLocal('document',JSON.stringify(response.document));
			
			console.log(functions.getLocal('document'));
			var auth_window = window.open(response.login_url,'newwindow','height=400,width=600' );
			
			var checkForWindow = window.setInterval(function(){
			    console.log('checking for window close: ', auth_window.closed);
			    if(auth_window.closed){
				clearInterval(checkForWindow);
				parent.saveMendeleyDocument();
			    }else{}
			},1000);
		    }

		},
		faliure : function(response){
		    console.log(response);
		}
	    });

	};

	
	this.saveMendeleyDocument = function(){
	    

	    var document = JSON.parse(functions.getLocal('document'));
	    
	    console.log('calling mendeley save on :', document);	    
	    var url = 'http://localhost:8000/createMendeleyDoc/';
	   /* var url = 'http://localhost:8000/createMendeleyDoc'+'?title='+document.title+'&type='+document.type+'&year='+document.year+'&pages='+document.pages+'&accessed='+document.accessed+'&authors='+document.authors+'&abstract='+document.abstract+'&tags='+document.tags+'&keywords='+document.keywords+'&city='+document.city+'&publisher='+document.publisher+'&url='+document.link;
*/
	   

	    $.ajax({
		url: url,
		type: "POST",
		data : {document : JSON.stringify(document)} ,
		success : function(response){
		    console.log(response);
		    var responseJson = JSON.parse(response);
		    window.response = response;
		    if(responseJson.success){
			var documentId = responseJson.success.documentId;
			var title = responseJson.success.title;
			var html = "Document saved<br> Title: " + title + "<br>DocumentId: " + documentId;
			$('#response-message').html(html);
		    }else{
			$('#response-message').html(responseJson.error);
		    }
		    
		    
		},
		failure : function(response){
		    
		}
	    });
	};

	var functions = {
	    getCookie: function (c_name) {
		var i, x, y, ARRcookies = document.cookie.split(";");

		for (i = 0; i < ARRcookies.length; i++) {
                    x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
                    y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
                    x = x.replace(/^\s+|\s+$/g, "");
                    if (x == c_name) {
			return unescape(y);
                    }
		}

		return null;
        },

        setCookie: function (key, value, c_extra) {
            if (!c_extra) c_extra = "Expires=Fri, 15-Jan-2099 21:47:38 GMT; Path=/";
            document.cookie = key + '=' + value + '; ' + c_extra;
        },

	saveLocal: function(key,value){
	    localStorage.setItem(key, value);
	},

	getLocal: function(key){
	    return localStorage.getItem(key);
	}

	};

	this.functions = functions;
	var attachEvents = function(){

	    console.log('Attaching the events');

	    $('#share-button').click(function(){
		appo.fetchDataFromWorldcat();
	    });
	};


	this.storeInCookie = function(){
	    
	};


	this.initApp = function(){
	    attachEvents();
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
		}
	    var csrftoken = getCookie('csrftoken');
	    
	    //alert(csrftoken);
	    //make AJAX call post settings
	    function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	    }
	    
	    $.ajaxSetup({
		crossDomain: false, // obviates need for sameOrigin test
		beforeSend: function(xhr, settings) {
		    if (!csrfSafeMethod(settings.type)) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		    }
		}
	    });
	};

    };


    
    //object to access the MainApp

    
    appo  = new MainApp();
    
    appo.initApp();


})();
