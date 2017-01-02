/*
    LIVE - updates state from websockets

    (c) 2016 Ciro Scognamiglio <c.scognamiglio@cslash.net>

 */

import axios from 'axios';

class live {

    constructor() {
        if (!"WebSocket" in window) {
            console.log("WebSocket NOT supported by your Browser!");
        }

        axios.get("/api/v1/usertoken").then((ret) => {
            // Process the dump
            console.log(ret);
            this.socket(ret.data);
        })
        //     .then((jqXHR, textStatus, errorThrown) => {
        //     console.log(textStatus);
        //     console.log(errorThrown);
        //     console.log("user is not logged in");
        // });
    }

    socket(token) {
        this.url = 'ws://' + window.location.host;
        this.ws = new WebSocket(this.url + '/api/v1/live/websocket');

          this.ws.onmessage = function(e) {
            console.log(e.data)
          }

          this.ws.onopen = function() {
            console.log('opening...');
            this.send(JSON.stringify({'auth' : token}));
            this.send(JSON.stringify({'watch': 'projects'}));
            //ws.send(JSON.stringify({'watch': 'sessions'}));
            //ws.send(JSON.stringify({'watch': 'messages'}));
          }

          this.ws.onerror = function(error) {
            console.log('WEbSocket error ' + error)
            console.dir(error)
          }

          this.ws.onclose = function(error){
            // websocket is closed.
            console.log("Connection is closed...");
            console.log(error);
          }

    }

}

export { live };