function add (){
    storage = localStorage;
    let formdata = new FormData();

    formdata.append('token', storage.getItem('token'));
    formdata.append('title', document.getElementsByClassName('title')[0].value);
    formdata.append('transaction', document.getElementsByClassName('amount')[0].value);

    let req = new XMLHttpRequest();
    req.open('POST', '/transaction', false)
    req.send(formdata);
    if (req.responseText=="Transaction added.") {
      window.location.replace("/list?token="+storage.getItem('token'));
    } else {
      document.getElementsByClassName('amount')[0].value = 0;
      alert(req.responseText);
    }
    return 0;
  }
