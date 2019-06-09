function logOut(){
  storage = localStorage;
  storage.setItem('token', null);
  window.location.replace("/login");
  return 0;
}
