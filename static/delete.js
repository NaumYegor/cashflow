function delete_id(){
  storage = localStorage;
  let formdata = new FormData();

  formdata.append('token', storage.getItem('token'));
  formdata.append('id', document.getElementsByClassName('ID')[0].value);

  let req = new XMLHttpRequest();
  req.open('POST', '/delete', false)
  req.send(formdata);
  if (req.responseText=="Deleted.") {
    window.location.replace("/list?token="+storage.getItem('token'));
  } else {
    document.getElementsByClassName('ID')[0].value = '';
    alert(req.responseText);
  }
  return 0;
}
