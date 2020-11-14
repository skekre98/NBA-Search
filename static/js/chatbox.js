//links
//http://eloquentjavascript.net/09_regexp.html
//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions


var messages = [], //array that hold the record of each string in chat
lastUserMessage = "", //keeps track of the most recent input string from the user
botMessage = "", //var keeps track of what the chatbot is going to say
botName = 'Chatbot', //name of the chatbot
talking = true; //when false the speach function doesn't work

window.alert = function(){};
        var defaultCSS = document.getElementById('bootstrap-css');
        function changeCSS(css){
            if(css) $('head > link').filter(':first').replaceWith('<link rel="stylesheet" href="'+ css +'" type="text/css" />'); 
            else $('head > link').filter(':first').replaceWith(defaultCSS); 
        }

// Function to handle bot response 
async function chatbotResponse() {
  talking = true;
  botMessage = "I'm confused"; //the default message

    const payload = new FormData();
    payload.append('msg', lastUserMessage);

    for(var value of payload.values()) {
      console.log(value);
    }

    const res = await fetch('/bot-msg', {
        method: 'post',
        body: payload
    });

    botMessage = await res.json();
}

// Auto-scroll and update based on https://stackoverflow.com/a/39729993

async function newmsg(){
    var data = $("#btn-input").val();

    $('chat_log').append('<div class="row msg_container base_sent"><div class="messages msg_sent"><p>'+data+'</p></div></div>');
    clearInput();
    lastUserMessage = String(data);
    botMessage = 'TEST';
    await chatbotResponse();
    $('chat_log').append('<div class="row msg_container base_receive"><div class="messages msg_receive"><p>'+botMessage+'</p></div></div>')

    messages.push(data);
    //Speech(botMessage) // Turned speech off, recommend adding a toggle switch so user can choose 
    $(".msg_container_base").stop().animate({ scrollTop: $(".msg_container_base")[0].scrollHeight}, 1000);
}


$("#submit").click(async function() {
    newmsg();
});

function clearInput() {
    $("#myForm :input").each(function() {
        $(this).val(''); //clears form
    });
}

$("#myForm").submit(function() {
    return false; // do-nothing code to prevent redirection
});

// Function to convert text to speech
//https://developers.google.com/web/updates/2014/01/Web-apps-that-talk-Introduction-to-the-Speech-Synthesis-API
function Speech(say) {
  if ('speechSynthesis' in window && talking) {
    var utterance = new SpeechSynthesisUtterance(say);
    speechSynthesis.speak(utterance);
  }
}

//runs the keypress() function when a key is pressed
document.onkeypress = keyPress;
//if the key pressed is 'enter' runs the function newEntry()
function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13 || key == 3) {
    //runs this function when enter is pressed
    newmsg();
  }
  if (key == 38) {
    console.log('hi')
      //document.getElementById("chatbox").value = lastUserMessage;
  }
}