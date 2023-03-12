var userOpenedAlert = false;

function setInnerText(element, value) {
  if (element.innerText) {
    element.innerText = value;
  } else {
    element.textContent = value;
  }
}

window.addEventListener("message", function(event) {

  if (!window.location.origin) {
    window.location.origin = window.location.protocol + "//" 
        + window.location.hostname 
        + (window.location.port ? ':' + window.location.port: '');
  }

  if (event.origin == window.location.origin && event.data == "success") {
    userOpenedAlert = true;
    levelSolved();
    return;
  }

  updateURLBar('1', event.data);
}, false);

function updateURLBar(frameNum, value) {
  var urlbar = document.getElementById('input' + frameNum);
  urlbar.value = unescape(value);
}


function logXHR(path) {
  window.location.toString().match(/level(\d+)/);
  var lNum = RegExp.$1 || "0";

  var oReq = new XMLHttpRequest();
  oReq.open("GET", '/feedback/level' + lNum + path, true);
  oReq.send();
}


function showHint() {
  var firstHiddenHint = document.querySelector('#hints li[data-hidden]');
  if (!firstHiddenHint)
    return;

  firstHiddenHint.style.display = "block";
  firstHiddenHint.removeAttribute('data-hidden');
  window.scroll(0, document.body.clientHeight);

  var hintNumEl = document.getElementById('hint-num');
  var hintNum = parseInt(hintNumEl.innerHTML, 10) + 1;
  setInnerText(hintNumEl, hintNum);

  logXHR('/hint/' + hintNum)
}
function setInputFieldReturnHandler() {
  var inputField = document.getElementById('input1');
  if (!inputField) {
    return;
  }
  inputField.value = document.querySelector('iframe').src;
  inputField.onkeyup = function (e) {
    if (e.keyCode == 13) {
      updateFrame(1);
      return false;
    }
  }
}
