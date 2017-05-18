/*
    LIVE - updates state from websockets

    (c) 2016-2017 Ciro Scognamiglio <c.scognamiglio@cslash.net>

 */

import axios from 'axios';
import SockJS from 'sockjs-client';

class Live {

    constructor() {

        axios.get("/api/v1/usertoken").then((ret) => {
            // Process the dump
            console.log(ret);
            this.socket(ret.data);
        });
        //     .then((jqXHR, textStatus, errorThrown) => {
        //     console.log(textStatus);
        //     console.log(errorThrown);
        //     console.log("user is not logged in");
        // });

        /*

            callback: function
         */
        this.watchers = [];
    }

    socket(token) {
        this.url = '//' + window.location.host;
        this.ws = new SockJS(this.url + '/api/v1/live');

        this.ws.onmessage = function(e) {
            console.log("message");
            let data = JSON.parse(e.data);
            console.log(data);

            if (data.hasOwnProperty('result')) {
                // this is a result for a previous command
                this.result(data);
            } else {
                // this is a stream
                this.stream(data);
            }

        }.bind(this);

        this.ws.onopen = function() {
            console.log('opening ws...');
            this.authenticate(token);
            console.log("authenticated ws");
        }.bind(this);

        this.ws.onerror = function(error) {
            console.log('WebSocket error ' + error)
            console.dir(error)
        };

        this.ws.onclose = function(error){
            // websocket is closed.
            console.log("Connection is closed...");
            console.log(error);
        };

    }

    authenticate(token) {
        this.ws.send(JSON.stringify(
            {
                command: 'authenticate',
                token: token
            }
        ));
    }

    command(command, object) {
        this.ws.send(JSON.stringify(
            {
                command: command,
                object: object
            }
        ));
    }

    watch(object, filter=null) {
        this.command('watch', object);
        if(filter){
            this.command('filter', filter);
        }
    }

    unwatch(object) {
        this.command('unwatch', object);
    }

    count(object) {
        this.command('count', object);
    }

    filter(params) {
        this.command('filter', params);
    }
    /*
        Register a callback that will receive messages
        as they arrive from the websocket
        Will send a request for watching changes
     */
    register(watchObject, filter=null, callback) {
        console.log("register " + watchObject);
        this.watchers.push({
            object: watchObject,
            filter: filter,
            callback: callback
        });
    }

    /*
        Init the watchers, this will send watch requests over the ws
     */
    init() {
        this.watchers.map(function(w) {
            this.watch(w.object, w.filter);
        }.bind(this));
    }

    /*
        handles result messages
     */
    result(result) {
        switch(result.command) {
            case 'authenticate':
                /* once authenticated init the watchers */
                this.init();
                break;
            case 'watch':
                if (result.result.code == 1) {
                    console.log(result.result.message);
                } else {
                    console.log(result.result.message);
                }
                break;
            case 'unwatch':
                break;
            case 'count':
                break;
        }
    }

    /*
        handles a message stream coming in
     */
    stream(stream) {
        switch(stream.command) {
            case 'watch':
                let w = this.watchers.find((watcher) => watcher.object == stream.object);
                if (w) {
                    w.callback(stream.data);
                } else {
                    console.log('not watching: ' + JSON.stringify(stream))
                }
                break;
            case 'count':
                break;
            default:
                console.log('ignoring: ' + JSON.stringify(stream));

        }
    }

}

let live = new Live();

export default live;
