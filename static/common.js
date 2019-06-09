function toTransactions() {
  storage = localStorage;
  window.location.replace("/list?token="+storage.getItem("token"));
}
