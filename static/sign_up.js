function sign_up (){
      if (document.getElementsByClassName("password")[0].value != document.getElementsByClassName("confirm")[0].value) {
        alert("Passwords do not match");
        return;
      }
      let formdata = new FormData();
      formdata.append('login', document.getElementsByClassName('login')[0].value);
      formdata.append('email', document.getElementsByClassName('email')[0].value);
      formdata.append('password', document.getElementsByClassName('password')[0].value);
      let req = new XMLHttpRequest();
      req.open('POST', '/signup', false)
      req.send(formdata);
      setTimeout(() => {alert(req.responseText)}, 5000);
      if (req.responseText=="Check an email."){
        window.location.replace("/login");
      } else {
        alert(req.responseText);
      }
      return 0;
    }