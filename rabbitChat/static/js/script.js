$(document).ready(function() {
    

    // Global name of person
    var person = '';


    // Function to take the name of person until he selects a qualified name.
    // Calls repeatedly until name is selected.
    function myFunction() {
        person = prompt("What's your nickname?", "nick");
        if (person === null) {
            myFunction();
        } else if (person === '') {
            myFunction();
        } else if (person !== null) {
            $('.welcome .welcomeLine').append($('<h2>').text('Welcome, '));
            $('.welcome .welcomeLine').append($('<h3>').text(person + '.'));
            $('.welcome').append($('<code>'));
        }
    }


    // Call the myFunction just as the window loads
    $(window).bind("load", function() {
        myFunction();
    });


    // Default variables
    
    var conn = null;                    // global connection object
    var disconn = 0;                    // checks if connection was closed by server or user
    var errorconn = 0;                  // checks if connection is havving error
    var origin_clientid = null;         // clientid if the main user sent by server
    var typing = false;                 // If person is typing presently or not
    var lastTypingTime;                 // last time the typing event was called
    var TYPING_TIMER_LENGTH = 1000;     // in ms
    var $messages = $('.messages');     // Messages area
    var msgcount = 0;                   // currently of no use. can used in your own way.
    var colorcount = 0;                 // No of usernames ( keeps on adding even if user leaves chat)
    var personcolor = {};               // Color set array for different usernames picked from colorset
    // The color set for usernames
    var colorset = ['#4876FF', '#CD00CD', '#32CD32', '#FFC125',
                    '#DC143C', '#8a2be2', '#00ff7f', '#00ced1',
                    '#FF34B3', '#8B8989', '#00CD66', '#EE1289',
                    '#1E90FF', '#FFD700', '#C67171', '#33A1C9',
                    '#CD8500', '#2E8B57', '#68228B', '#00C5CD'];
    


    // Function to be called when a person clicks the Connect/Dicsonnect button
    // basically to start the connection to chat
    $('#connect').click(function() {
        if (conn === null) {
            connect();
        } else {
            disconnect();
        }
        return false;
    });


    // Funciton to update the UI from present status - online/offline, connect/disconnect
    function update_ui() {
        var msg = '';
        if (conn === null || conn.readyState != SockJS.OPEN) {
            $('#status').text('Offline').removeClass('active').addClass('inactive');
            $('#connect').text('Connect');
        } else {
            $('#status').text('Online - ' + conn.protocol).removeClass('inactive').addClass('active');
            $('#connect').text('Disconnect');
        }
    }


    // Funciton called when user disconnects using Disconnect button
    function disconnect() {
        if (conn !== null) {
            disconn = 1;
            conn.close();
        }
    }


    // function called when user clicks on connect button, initated by click event
    function connect() {

        // first call disconnect() to be clean any stale previous connections
        disconnect();

        // To add any other transport layers to be used if websocket is not possible
        var transports = $('#protocols input:checked').map(function() {
            return $(this).attr('id');
        }).get();

        // sockjs connection object created
        conn = new SockJS('http://' + window.location.host + '/chat', transports);

        $('.welcome code').text('Connecting...');

        // Sockjs onOpen event triggered when connection is opened and readystate is OPEN
        conn.onopen = function() {
            $('.welcome code').text('Connected');
            update_ui();
        };

        // sockjs onMessage event triggered whenever there is a message sent on the connection
        conn.onmessage = function(e) {
            var m = JSON.parse(e.data);
            var msg_type = m['msg_type'];
            if (msg_type === 'rabbitmqOK') {
                sendmsg('public.*', person, 'start', person + ' joined', 'public');
            } else if (msg_type === 'public') {
                print(m);
            } else if (msg_type === 'private') {
                handlePrivateMsg(m);
            }
        };

        // sockjs on Close event triggered whenever there is a close event either triggered by
        // server or by user itself via disconnect button -> disconnect()
        conn.onclose = function() {
            if (errorconn !== 1) {
                if (disconn === 0) {
                    serverUnavailable();
                } else {
                    disconn = 0;
                    closeConn();
                }
            } else if (errorconn === 1) {
                serverError();
                errorconn = 0;
            }
            $('.welcome code').text('');
            conn = null;
            update_ui();
        };

        // sockjs Error event triggered whenver there is an error connecting to the connection or
        // error info sent by server
        conn.onerror = function() {
            errorconn = 1;
        };
    }


    // Funciton to print the message received by connection,
    // this funciton doesn't print directly, rather it processes the messages and
    // calls other utility funcitons to print the final message
    function print(p) {
        msgcount = msgcount + 1;
        var msg_type = p['msg_type'];
        chatbox = $('.' + msg_type + ' .chatbox');
        var n = p['name'];
        var s = p['stage'];
        var clientid = p['clientid'];
        var m = '';
        var m1 = '';
        var m2 = '';

        // Process what is the Stage of the message -> start, stop, msg, error,
        // start_typing,stop_typing, sevrver is unavailable...
        if (s === 'start') {
            setUsernameColor(clientid);
            if (n === person) {
                origin_clientid = clientid;
                m1 = "You joined";
            } 
            else {
                m1 = n + ' joned';
            }
            log(m1);
            updateParticipants(p['participants']);
        } 
        else if (s === 'msg') {
            if (personcolor[clientid] === undefined) {
                setUsernameColor(clientid);
            }
            addmsg(p);
        }
        else if (s === 'stop') {
            if (n === person) {
                origin_clientid = clientid;
                m1 = "You left";
            } 
            else {
                m1 = n + ' left';
            }
            log(m1);
            updateParticipants(p['participants']);
        } 
        else if (s === 'error') {
            log(p['msg']);
            updateParticipants(p['participants']);
        } 
        else if (s === 'unavailable') {
            log(p['msg']);
            updateParticipants(p['participants']);
        } 
        else if (s === 'start_typing') {
            if (personcolor[clientid] === undefined) {
                setUsernameColor(clientid);
            }
            if (n !== person) {
                addChatTyping(p);
            }
        } 
        else if (s === 'stop_typing') {
            if (personcolor[clientid] === undefined) {
                setUsernameColor(clientid);
            }
            if (n !== person) {
                removeChatTyping(p);
            }
        }
        chatbox.scrollTop(chatbox.scrollTop() + 10000);
        $('.public .groupchatTB #groupcount').text(p['participants']);
    }


    // function logs the start, stop, unavailable message in the center of chat screen
    function log(msg) {
        var $el = $('<li>').addClass('log').text(msg);
        var options = {};
        echomsg($el, options);
    }

    
    // funciton updates the present number of participants after start,stop, unavaible events
    function updateParticipants(participants) {
        var msg = '';
        if (participants === 0) {
            msg += "nobody is online";
        } else if (participants === 1) {
            msg += "there is 1 person online";
        } else {
            msg += "there are " + participants + "people online";
        }
        log(msg);
    }



    // Adds a message element to the messages and scrolls to the bottom
    // elem - The element to add as a message
    // options.fade - If the element should fade-in (default = true)
    // options.prepend - If the element should prepend
    //   all other messages (default = false)
    function echomsg(elem, options) {
        var $el = $(elem);
        // Setup default options
        if (!options) {
            options = {};
        }
        if (typeof options.fade === 'undefined') {
            options.fade = true;
        }
        if (typeof options.prepend === 'undefined') {
            options.prepend = false;
        }
        // Apply options
        if (options.fade) {
            $el.hide().fadeIn(100);
        }
        if (options.prepend) {
            $messages.prepend($el);
        } else {
            $messages.append($el);
        }
        // $messages[0].scrollTop = $messages[0].scrollHeight;
    }


    // Adds the visual chat message to the message list
    function addmsg(data, options) {
        // Don't fade the message in if there is an 'X was typing'
        var $typingMessages = getTypingMessages(data);
        options = options || {};
        if ($typingMessages.length !== 0) {
            options.fade = false;
            $typingMessages.remove();
        }
        var tm = new Date().toString("hh:mm tt");
        var typingClass = data.typing ? 'typing' : '';
        var timeTypingClass = data.typing ? 'timeTyping' : '';
        var $timeinfoDiv = $('<p class="timeinfo2" />').addClass(timeTypingClass).text(tm).css('color', '#C2C2C2');
        var $usernameDiv = $('<p class="username"/>').text(data['name']).css('color', personcolor[data['clientid']]);
        var $messageBodyDiv = $('<span class="messageBody">').text(data['msg']);
        var $messageDiv = $usernameDiv.append($messageBodyDiv);
        var $messageDivFinal = $('<li class="message"/>').attr('clientid', data['clientid']).addClass(typingClass).append($timeinfoDiv, $messageDiv);
        echomsg($messageDivFinal, options);
    }


    // Decide color of user
    function setUsernameColor(clientid) {
        colorcount = colorcount + 1;
        personcolor[clientid] = colorset[colorcount % 20 - 1];
    }


    // Adds the visual chat typing message
    function addChatTyping(data) {
        data['typing'] = true;
        data['msg'] = 'is typing...';
        addmsg(data);
    }


    // Removes the visual chat typing message
    function removeChatTyping(data) {
        getTypingMessages(data).fadeOut(function() {
            $(this).remove();
        });
    }


    // Gets the 'X is typing' messages of a user
    function getTypingMessages(data) {
        return $('.typing').filter(function(index) {
            var res = $(this).attr('clientid') === data['clientid'];
            return res;
        });
    }


    // preares msg to be sent to print() when close connection initated by user
    function closeConn() {
        var m = {
            'name': person,
            'stage': 'stop',
            'msg': person + ' left',
            'msg_type': 'public',
            'clientid': origin_clientid,
            'participants': 0
        };
        print(m);
    }


    // preares msg to be sent to print() when close connection initated by server or server is unavailbel
    function serverUnavailable() {
        var m = {
            'name': person,
            'stage': 'unavailable',
            'msg': 'Oops! server unavailable',
            'msg_type': 'public',
            'clientid': origin_clientid,
            'participants': 0
        };
        print(m);
    }


    // preares msg to be sent to print() when close connection initated by some error in connection
    function serverError() {
        var m = {
            'name': person,
            'stage': 'error',
            'msg': 'Aw! Snap. Server no do',
            'msg_type': 'public',
            'clientid': origin_clientid,
            'participants': 0
        };
        print(m);
    }


    // triggered when msg is sent by send button
    $('#publicsendbtn').click(function() {
        formsubmit('public');
        return false;
    });


    // triggered when msg is sent by send button
    $('#privatesendbtn').click(function() {
        formsubmit('private');
        return false;
    });


    // triggered when msg is sent by hitting Enter
    $('.publicsend').submit(function() {
        formsubmit('public');
        return false;
    });


    // triggered when msg is sent by hitting Enter
    $('.privatesend').submit(function() {
        formsubmit('private');
        return false;
    });


    //  sends the message content to sendmsg -> which actually sends msg to the connection
    function formsubmit(typ) {
        sendmsg(typ + '.*', person, 'stop_typing', '', typ);
        typing = false;
        var v = $('#' + typ + 'text').val();
        sendmsg(typ + '.*', person, 'msg', v, typ);
        $('#' + typ + 'text').val('');
        return false;
    }


    // triggers whenever user is Typing...
    $('.box .inpbox').on('keypress', function() {
        var typ = $(this).attr('data');
        updateTyping(typ);
    });


    // called to update typing status whenever user is typing event is triggered
    function updateTyping(typ) {
        if (conn !== null) {
            if (typing === false) {
                typing = true;
                sendmsg(typ + '.*', person, 'start_typing', '', typ);
            }
            lastTypingTime = (new Date()).getTime();
            setTimeout(function() {
                var typingTimer = (new Date()).getTime();
                var timeDiff = typingTimer - lastTypingTime;
                if (timeDiff >= TYPING_TIMER_LENGTH && typing) {
                    sendmsg(typ + '.*', person, 'stop_typing', '', typ);
                    typing = false;
                }
            }, TYPING_TIMER_LENGTH);
        }
    }


    // sends the actual msg after JSONifying it to the connection via conn.send()
    function sendmsg(routing_key, name, stage, msg, msg_type) {
        var newmsg = {
            'routing_key': routing_key,
            'msg': {
                'name': name,
                'stage': stage,
                'msg': msg,
                'msg_type': msg_type
            }
        };
        var res = JSON.stringify(newmsg);
        conn.send(res);
    }


    // function handle private msgs
    function handlePrivateMsg(m) {
        // Todo -> verifying who has sent the message and notifying the user with print(m,'private')
    }

});