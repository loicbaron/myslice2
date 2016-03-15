
feed = (function() {
    var socket = null;
    //var ellog = document.getElementById('log');
    var wsuri = "ws://" + window.location.hostname + ":8111/ws";
    var el = $('#log');

    return {
        connect: function ()
        {
            if ("WebSocket" in window) {
                socket = new WebSocket(wsuri);
            } else if ("MozWebSocket" in window) {
                socket = new MozWebSocket(wsuri);
            } else {
                console.log("Browser does not support WebSocket!");
            }
            if (socket) {
                socket.onopen = function () {
                    console.log("Connected to " + wsuri);
                    socket.send('hello');
                }

                socket.onclose = function (e) {
                    console.log("Connection closed (wasClean = " + e.wasClean + ", code = " + e.code + ", reason = '" + e.reason + "')");
                    socket = null;
                }

                socket.onmessage = function(e) {
                    var result = JSON.parse(e.data);
                    console.log(result);
                    if (result.id) {
                        el.prepend('<div>' +
                            '<b>Job:</b> ' + result.id +
                            ' <b>Status:</b> ' + result.jobstatus +
                            ' <b>Command:</b> ' + result.command +
                            ' <b>Message:</b> ' + result.message +
                            '</div>');
                        if (result.stdout) {
                            el.prepend('<div><b>Output:</b><pre>' + result.stdout + '</pre></div>')
                        }
                    } else {
                        el.append('<div>'+result.message+'</div>');
                    }
                }
            }
        },

        send: function (msg)
        {
            if (socket) {
                socket.send(msg);
                console.log("Sent: " + msg);
            } else {
                console.log("Not connected.");
            }
        },

        resources: function()
        {

        }

    }
});




