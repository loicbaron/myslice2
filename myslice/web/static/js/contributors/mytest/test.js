/*
 Get the security token of current user
*/
$.ajax({ 
    url : "/api/v1/usertoken", 
    dataType: 'html',
    }).done(function(token){ 
        // Process the dump
        console.log(token); 
        launchWS(token);
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log(textStatus);
        console.log(errorThrown);
        console.log("user is not logged in");
    });

/*
 Manage WebSocket
*/
function launchWS(token){
  if ("WebSocket" in window){
      var wsUrl = 'ws://' + window.location.host 
      var ws = new WebSocket(wsUrl + '/api/v1/live/websocket')
      
      ws.onmessage = function(e) {
        console.log(e.data)
      }
      
      ws.onopen = function() {
        console.log('opening...');
        ws.send(JSON.stringify({'auth' : token}));
        ws.send(JSON.stringify({'watch': 'activity'}));
      }
      
      ws.onerror = function(error) {
        console.log('WEbSocket error ' + error)
        console.dir(error)
      }
  
      ws.onclose = function(error){ 
        // websocket is closed.
        console.log("Connection is closed..."); 
        console.log(error);
      }
  }else{
      // The browser doesn't support WebSocket
      alert("WebSocket NOT supported by your Browser!");
  }
}
