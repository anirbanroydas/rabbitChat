$(document).ready(function() {
    console.log('inside documet.read ()');
    var person = '';
    console.log(' person : ' + person);

    function myFunction() {
        console.log('inside myFunction()');
        person = prompt("What's your nickname?", "nick");
        if (person === null) {
            console.log('person == null');
            console.log('invoke myFunction() recursively again');
            myFunction();
            console.log('reutrning from myFunction()');
        } else if (person === '') {
            console.log('person==empty');
            console.log('invoke myFunction() recursively again');
            myFunction();
            console.log('returning from myFunction');
        } else if (person !== null) {
            console.log('person != null');
            $('.welcome .welcomeLine').append($('<h2>').text('Welcome, '));
            $('.welcome .welcomeLine').append($('<h3>').text(person + '.'));
            $('.welcome').append($('<code>'));
            console.log('text transformations done');
            console.log('returning from myFunction');
        }
    }
    $(window).bind("load", function() {
        console.log('inside window.bind load funtion ');
        console.log('invokeing myFunction first time');
        myFunction();
        console.log('returning from window.bind load myFunction');
    });

    var conn = null;
    var disconn = 0;
    var errorconn = 0;
    var origin_clientid = null;
    var typing = false;
    var lastTypingTime;
    var TYPING_TIMER_LENGTH = 2000; // in ms
    var $messages = $('.messages'); // Messages area
    var msgcount = 0;
    var personcount = 0;
    var colorcount = 0;
    var colorset = ['#4876FF', '#CD00CD', '#32CD32', '#FFC125',
        '#DC143C', '#8a2be2', '#00ff7f', '#00ced1',
        '#FF34B3', '#8B8989', '#00CD66', '#EE1289',
        '#1E90FF', '#FFD700', '#C67171', '#33A1C9',
        '#CD8500', '#2E8B57', '#68228B', '#00C5CD'
    ];
    var personcolor = {};
    console.log(' conn : ' + conn);
    console.log('origin_clientid :', origin_clientid);
    console.log('msgcount : %d, personcount : %d, colorcount : %d', msgcount, personcount, colorcount);
    console.log('personcolor : ', personcolor);
    console.log('colorset : ', colorset);

    $('#connect').click(function() {
        console.log('clicked #connect');
        if (conn === null) {
            console.log('conn==null');
            console.log('invoking connect()');
            connect();
            console.log('invoked connect() successful');
        } else {
            console.log('conn!= null');

            console.log('Now ready to disconnect connection');
            console.log('invoking disconnect()');
            disconnect();
            console.log('invoked disconnect() successful');
        }
        return false;
    });

    function update_ui() {
        var msg = '';
        console.log('inside update_ui');
        if (conn === null || conn.readyState != SockJS.OPEN) {
            console.log('conn==null or conn.readyState !=SockJS.Open');
            $('#status').text('Offline').removeClass('active').addClass('inactive');
            $('#connect').text('Connect');
            console.log('text transformations done');
        } else {
            console.log('conn != Null');
            $('#status').text('Online - ' + conn.protocol).removeClass('inactive').addClass('active');
            $('#connect').text('Disconnect');
            console.log('text transformations done');
        }
    }

    function disconnect() {
        console.log('inside disconnect()');
        if (conn !== null) {
            console.log('conn!=null');
            $('.welcome code').text('Diconnecting...');
            console.log('text transformations done');
            disconn = 1;
            conn.close();
        }
        console.log('returning from disconnect()');
    }

    function connect() {
        console.log('inside connect()');
        console.log('invoking disconnect()');
        disconnect();
        console.log('disconnect() invoked successful');
        var transports = $('#protocols input:checked').map(function() {
            return $(this).attr('id');
        }).get();
        console.log('creating new sockjs connection ');
        conn = new SockJS('http://' + window.location.host + '/chat', transports);
        console.log(' conn created successful - conn : ' + conn);
        $('.welcome code').text('Connecting...');
        console.log('welcome append code connecting...');
        console.log('returning from connect()');
        conn.onopen = function() {
            console.log('inside conn.onopen() ');
            $('.welcome code').text('Connected');
            console.log('text transformations done ');
            console.log('invoke update_ui()');
            update_ui();
            console.log('update_ui() invoked successul');
            console.log('returng from conn.onopen');
        };
        conn.onmessage = function(e) {
            console.log('inside conn.onmessage()');
            console.log('msg received before parsing : ' + e.data);
            console.log('typeof e.data : ' + typeof e.data);
            var m = JSON.parse(e.data);
            console.log('msg after parsing : ' + m);
            var msg_type = m['msg_type'];
            console.log('msg_type : ' + msg_type);
            if (msg_type === 'rabbitmqOK') {
                console.log('first msf received after rabbitmq client is created ');
                console.log(' Now ready to send message to reabbitMQ via websocket.');
                console.log('Sending first broadcast mesg');
                console.log('invoking sednmsg()');
                sendmsg('public.*', person, 'start', person + ' joined', 'public');
                console.log('sendmsg() invoked successfully');
                console.log('first broadcast mesg sent successfully');
            } else if (msg_type === 'public') {
                console.log('invoking print(m)');
                print(m);
                console.log('print(m) invoke successfully');
            } else if (msg_type === 'private') {
                console.log('invoking handlePrivateMsg(m)');
                handlePrivateMsg(m);
                console.log('handlePrivateMsg(m) invoked successfully');
            }
            console.log('returning from conn.onmessage');
        };

        conn.onclose = function() {
            console.log('inside conn.onclose()');

            if (errorconn !== 1) {

                if (disconn === 0) {
                    console.log('initating serverUnavailable()');
                    serverUnavailable();
                    console.log('closeConn() invoked successfully');


                } else {
                    console.log('initating closeConn()');
                    disconn = 0;
                    closeConn();
                    console.log('closeConn() invoked successfully');
                }

            } else if (errorconn === 1) {

                console.log('inside errorconn===1');
                console.log('invoking serverError()');
                serverError();
                errorconn =0;
                console.log('serverError() invoked successful');

            }

            $('.welcome code').text('');
            console.log('text transformations done ');
            conn = null;
            console.log(' conn=null -> conn : ' + conn);
            console.log('invoke update_ui()');
            update_ui();
            console.log('update_ui() invoked successul');

            console.log('returning from conn.onclose()');
        };

        conn.onerror = function() {

            console.log('inside conn.onerror()');
            errorconn = 1;
            console.log('error value : errorconn : ', errorconn);
            console.log('returning from conn.onerror');
        };
    }

    function print(p) {
        console.log('inside print()');

        msgcount = msgcount + 1;
        console.log('msgcount : ' + msgcount);

        var msg_type = p['msg_type'];
        chatbox = $('.' + msg_type + ' .chatbox');
        console.log('chatbox : ' + chatbox);


        console.log('p  : ' + p);
        var n = p['name'];
        var s = p['stage'];
        var clientid = p['clientid'];
        var m = '';
        var m1 = '';
        var m2 = '';
        console.log('received message : name : %s, stage : %s, clientid : %s', n, s, clientid);

        if (s === 'start') {
            console.log('insdie stage = start');
            console.log('invoking setUsernameColor(clientid)');
            setUsernameColor(clientid);
            console.log('setUsernameColor set successfully');
            if (n === person) {
                console.log('inside name == person');
                origin_clientid = clientid;
                m1 = "You joined";
            } else {
                console.log('inside name != person');
                m1 = n + ' joned';
            }
            console.log('invoking log(p)...');
            log(m1);
            console.log('log(p) invoked successfully');
            console.log('invokig updateParticipants()...');
            updateParticipants(p['participants']);
            console.log('updateParticipants() invoked successfully');
            
            
        } else if (s === 'msg') {
            console.log('inside stage == msg');
            if (personcolor[clientid] === undefined) {
                console.log('personcount[clientid] === undefined');
                console.log('invoking setUsernameColor(clientid)');
                setUsernameColor(clientid);
                console.log('setUsernameColor set successfully');
            }
            console.log('invoking addmsg(p)...');
            addmsg(p);
            console.log('addmsg(p) invoked successfully');

        } else if (s === 'stop') {
            console.log('inside stage == stop');
            if (n === person) {
                console.log('inside name == person');
                origin_clientid = clientid;
                m1 = "You left";
            } else {
                console.log('inside name != person');
                m1 = n + ' left';
            }
            console.log('invoking log(p)...');
            log(m1);
            console.log('log(p) invoked successfully');
            console.log('invokig updateParticipants()...');
            updateParticipants(p['participants']);
            console.log('updateParticipants() invoked successfully');
            
        } else if (s === 'error') {

            console.log('inside stage == error');
            console.log('invoking log(p)...');
            log(p['msg']);
            console.log('log(p) invoked successfully');
            console.log('invokig updateParticipants()...');
            updateParticipants(p['participants']);
            console.log('updateParticipants() invoked successfully');
            


        } else if (s === 'unavailable') {
            console.log('inside stage == unavailable');
            console.log('invoking log(p)...');
            log(p['msg']);
            console.log('log(p) invoked successfully');
            console.log('invokig updateParticipants()...');
            updateParticipants(p['participants']);
            console.log('updateParticipants() invoked successfully');

        } else if (s === 'start_typing') {

            console.log('inside stage == start_typing');

            if (personcolor[clientid] === undefined) {
                console.log('personcount[clientid] === undefined');
                console.log('invoking setUsernameColor(clientid)');
                setUsernameColor(clientid);
                console.log('setUsernameColor set successfully');
            }

            if (n !== person){
                console.log('inside n !== person thus initiating typing printing');
                console.log('invoking addChatTyping()');
                addChatTyping(p);
                console.log('addChatTyping invoked successfully');
            }
            else {
                console.log('inside n====person thus not printing anything');
            }

        } else if (s === 'stop_typing') {
            console.log('inside stage == stop_typing');

            if (personcolor[clientid] === undefined) {
                console.log('personcount[clientid] === undefined');
                console.log('invoking setUsernameColor(clientid)');
                setUsernameColor(clientid);
                console.log('setUsernameColor set successfully');
            }

            if (n !== person){
                console.log('inside n !== person thus initiating typing printing');
                console.log('invoking removeChatTyping()');
                removeChatTyping(p);
                console.log('removeChatTyping invoked successfully');
            }
            else {
                console.log('inside n====person thus not printing anything');
            }
        }


        chatbox.scrollTop(chatbox.scrollTop() + 10000);
        $('.public .groupchatTB #groupcount').text(p['participants']);
        console.log('returnin from print()');
    }




    function log(msg) {

        console.log('inside log(msg)');

        var $el = $('<li>').addClass('log').text(msg);
        var options = {};
        console.log('invoking echomsg(el,options)');
        echomsg($el, options);
        console.log('echomsg() invoked successfully');
        console.log('returnig from log(msg)');

    }



    function updateParticipants(participants) {

        console.log('inside updateParticipants');
        var msg = '';
        if (participants === 0) {
            console.log('inside participants ===0');
            msg += "nobody is online";
        } else if (participants === 1) {
            console.log('inside participants ===1');
            msg += "there is 1 person online";
        } else {
            console.log('inside participants > 1');
            msg += "there are " + participants + "people online";
        }

        console.log('updated participants msg : ', msg);
        console.log('invoking log(msg)');
        log(msg);
        console.log('log(msg) invoiked successfully');
        console.log('returing from updateParticipants()');
    }




    // Adds a message element to the messages and scrolls to the bottom
    // elem - The element to add as a message
    // options.fade - If the element should fade-in (default = true)
    // options.prepend - If the element should prepend
    //   all other messages (default = false)
    function echomsg(elem, options) {

        console.log('inside echomsg(elem,options)');
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
        console.log('printing of msgin done');
        console.log('returing from echomsg');
    }





    // Adds the visual chat message to the message list
    function addmsg(data, options) {
        // Don't fade the message in if there is an 'X was typing'
        console.log('inside addmsg(data,options)' );
        console.log('invoking var $typingMessages = getTypingMessages(data)');
        var $typingMessages = getTypingMessages(data);
        console.log('getTypingMessages invoked successfully');
        console.log(' valur of $typingMessages : ',$typingMessages);
        options = options || {};
        if ($typingMessages.length !== 0) {
            options.fade = false;
            $typingMessages.remove();
        }

        var tm = new Date().toString("hh:mm tt");
        var typingClass = data.typing ? 'typing' : '';
        var timeTypingClass = data.typing ? 'timeTyping' : '';

        var $timeinfoDiv = $('<p class="timeinfo2" />').addClass(timeTypingClass).text(tm).css('color','#C2C2C2');

        var $usernameDiv = $('<p class="username"/>').text(data['name']).css('color', personcolor[data['clientid']]);
        var $messageBodyDiv = $('<span class="messageBody">').text(data['msg']);
        
        var $messageDiv = $usernameDiv.append($messageBodyDiv);

        var $messageDivFinal = $('<li class="message"/>').attr('clientid', data['clientid']).addClass(typingClass).append($timeinfoDiv, $messageDiv);

        console.log('invoking echomsg()');
        echomsg($messageDivFinal, options);
        console.log('echomsg invoked successfully');
        console.log('returinig from addmsg()');
    }




    // Decide color of user
    function setUsernameColor(clientid) {

        console.log('inside setUsernameColor()');
        colorcount = colorcount + 1;
        personcolor[clientid] = colorset[colorcount % 20 - 1];
        console.log('color set successfully');
        console.log('returning from setUsernameColor');

    }




    // Adds the visual chat typing message
    function addChatTyping(data) {
        console.log('inside addChatTyping()');
        data['typing'] = true;
        data['msg'] = 'is typing...';
        console.log(' data modified : ',data);
        console.log('invoking addmsg()');
        addmsg(data);
        console.log('addmsg invoked successfully');
        console.log('returing from addChatTyping()');
    }

    // Removes the visual chat typing message
    function removeChatTyping(data) {
        console.log('inside removeChatTyping()');
        console.log('invoking getTypingMessages().fadeOUt(function())');
        getTypingMessages(data).fadeOut(function() {
            $(this).remove();
        });
        console.log('getTypingMessages invoked successfully');
        console.log('returnign from removeChatTyping()');
    }


    // Gets the 'X is typing' messages of a user
    function getTypingMessages(data) {
        console.log('inside getTypingMessages()');
        return $('.typing').filter(function(index) {
            console.log('inside $(.typing.message).filter(function()) with INDEX : ',index);
            var res = $(this).attr('clientid') === data['clientid'];
            console.log(" res = $(this).attr('clientid') === data['clientid'] : ", res);
            console.log('returnign from filter with index : ',index) ;
            return res;

        });
    }




    function closeConn() {
        console.log('inside closeConn() ');
        console.log(' creating connection close msg objects.');
        var m = {
            'name': person,
            'stage': 'stop',
            'msg': person + ' left',
            'msg_type': 'public',
            'clientid': origin_clientid,
            'participants': 0

        };
        console.log(' msg to be sent: ' + m);
        console.log('print(m) initiated..');
        print(m);
        console.log('print(m) invoked successul');
        console.log('returning from closeConn()');
    }

    function serverUnavailable() {
        console.log('inside serverUnavailable() ');
        console.log(' creating serverUnavailable msg objects.');
        var m = {
            'name': person,
            'stage': 'unavailable',
            'msg': 'Oops! server unavailable',
            'msg_type': 'public',
            'clientid': origin_clientid,
            'participants': 0

        };
        console.log(' msg to be sent: ' + m);
        console.log('print(m) initiated..');
        print(m);
        console.log('print(m) invoked successul');
        console.log('returning from closeConn()');
    }


    function serverError() {
        console.log('inside serverError() ');
        console.log(' creating serverError msg objects.');
        var m = {
            'name': person,
            'stage': 'error',
            'msg': 'Aw! Snap. Server no do',
            'msg_type': 'public',
            'clientid': origin_clientid,
            'participants': 0

        };
        console.log(' msg to be sent: ' + m);
        console.log('print(m) initiated..');
        print(m);
        console.log('print(m) invoked successul');
        console.log('returning from closeConn()');
    }




    $('#publicsendbtn').click(function() {
        console.log('inside publicsendbtn clict()');
        console.log('invoking formsubmit()');
        formsubmit('public');
        console.log('formsubmit invoked successfully');
        return false;
    });

    $('#privatesendbtn').click(function() {
        console.log('inside privatesendbtn click()');
        console.log('invoking formsubmit()');
        formsubmit('private');
        console.log('formsubmit invoked successfully');
        return false;
    });

    $('.publicsend').submit(function() {
        console.log('inside .publicsend form.submit');
        console.log('invoking formsubmit()');
        formsubmit('public');
        console.log('formsubmit invoked successfully');
        return false;

    });

    $('.privatesend').submit(function() {
        console.log('inside .privatesend form.submit');
        console.log('invoking formsubmit()');
        formsubmit('private');
        console.log('formsubmit invoked successfully');
        return false;

    });


    function formsubmit(typ) {

        console.log('inside formsubmit()');
        console.log('sending stop typing event to server');
        console.log('invoking sednmsg()');
        sendmsg(typ + '.*', person, 'stop_typing', '', typ);
        console.log('sendmsg() invoked successfully');
        console.log('stop typing event sent to server successfully');
        typing = false;
        var v = $('#' + typ + 'text').val();
        console.log(' message value : ', v);
        console.log('sending actual msg to server');
        console.log('invoking sednmsg()');
        sendmsg(typ + '.*', person, 'msg', v, typ);
        console.log('sendmsg() invoked successfully');
        console.log('actual msg sent to server successfully');
        $('#' + typ + 'text').val('');
        console.log('returning from formsubmit()');
        return false;
    }


    $('.box .inpbox').on('keypress', function() {

        console.log('inside on.keypress event');
        var typ = $(this).attr('data');
        console.log('calling updateTyping()');
        updateTyping(typ);
        console.log('updateTyping() invoked successfully');
        console.log('returing from on.keypress event');


    });

    function updateTyping(typ) {
        if (conn !== null) {
            if (typing === false) {
                typing = true;
                console.log('invoking sednmsg()');
                sendmsg(typ + '.*', person, 'start_typing', '', typ);
                console.log('sendmsg() invoked successfully');
            }

            lastTypingTime = (new Date()).getTime();

            setTimeout(function() {
                    var typingTimer = (new Date()).getTime();
                    var timeDiff = typingTimer - lastTypingTime;
                    if (timeDiff >= TYPING_TIMER_LENGTH && typing) {
                        console.log('invoking sednmsg()');
                        sendmsg(typ + '.*', person, 'stop_typing', '', typ);
                        console.log('sendmsg() invoked successfully');
                        typing = false;
                    }
                },
                TYPING_TIMER_LENGTH
            );
        }
    }



    function sendmsg(routing_key, name, stage, msg, msg_type) {

        console.log('inside sendmsg()');

        var newmsg = {

            'routing_key': routing_key,
            'msg': {
                'name': name,
                'stage': stage,
                'msg': msg,
                'msg_type': msg_type
            }

        };

        console.log('newmsg createtd : ', newmsg);
        var res = JSON.stringify(newmsg);
        console.log('newmsg -> res after jsonifying : ', newmsg);
        console.log('sending the msg -> invoking conn.send()');
        conn.send(res);
        console.log('conn.send invoked successfully');

        console.log('returning from sendmsg()');
    }





    function handlePrivateMsg(m) {
        // Todo -> verifying who has sent the message and notifying the user with print(m,'private')
    }
});
