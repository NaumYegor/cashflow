function sign_in (){
  let formdata = new FormData();
  formdata.append('login', document.getElementsByClassName('login')[0].value);
  formdata.append('password', document.getElementsByClassName('password')[0].value);
  let req = new XMLHttpRequest();
  req.open('POST', '/signin', false)
  req.send(formdata);
  storage = localStorage;
  if (req.responseText[req.responseText.length-1]!='.'){
    storage.setItem('token', req.responseText);
    window.location.replace("/list?token="+req.responseText);
  }
  else {
    alert(req.responseText);
  }
}
