(function($) {

send = (url, value, method) => {
    console.log(value);
    var payload = { method: method,
                    mode: 'cors',
                    cache: 'default',
                    headers: {
                      'Accept': 'application/json',
                      'Content-Type': 'application/json'},
                    body: JSON.stringify(value)
                  };
    fetch(url, payload)
    .then(response => response.json()) // Result from the
    .then(data => {
      console.log(data) // Prints result from `response.json()`
    })
    .catch(error => console.error(error))
  }

sendData = (value) => {
    send('/send', {value : value}, 'POST');
  }

sendByUrl = (url, method) => {
    send(url, {value : 1}, method);
}


updateCron = (id, job) => {
    var cron = document.getElementById(id).value;
    var object = {job: job, cron: cron};
    send('/update-cron', object, 'PUT');
}

  sendDataById = (id) => {
    var value = document.getElementById(id).value;
    sendData(value);
  }
  
  sendDataByIdType = (id, type) => {
    var value = document.getElementById(id).value;
    sendValue = type.concat("=", value);
    sendData(sendValue);
  }
  
  
  sendTrsLighting = (id, type) => {
    var value = document.getElementById(id).value;
    if(!value.isNumber()) {
      alert("Value must be number!");
      return;
    }
    var object = {name: id, value: value};
    send('/update-setting', object, 'PUT');
    sendValue = type.concat("=", value);
    sendData(sendValue);
  }

showMessageBox = (message) => {
    var x = document.getElementById("snackbar");
    x.textContent = message;
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

}

showMessageBoxById = (id) => {
  var value = document.getElementById(id).value;
  showMessageBox(value);
}

var socket = io.connect()

socket.on('message', function(msg){
    console.log('msg = ' + msg);
  showMessageBox(msg);
})

  String.prototype.isNumber = function(){return /^\d+$/.test(this);}
})(jQuery);