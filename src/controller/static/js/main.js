function control(action) {
    var req = new XMLHttpRequest();
    req.open("POST", "/control", true);
    req.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"action": action});
    req.send(data);
}
