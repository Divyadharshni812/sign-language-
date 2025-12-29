const status = document.getElementById("gesture");

function fetchGesture() {
  fetch("http://127.0.0.1:5000/gesture")
    .then(res => res.json())
    .then(data => {
      if (data.gesture && data.gesture !== "") {
        status.innerText = data.gesture;
        status.style.color = "green";
      } else {
        status.innerText = "No gesture";
        status.style.color = "orange";
      }
    })
    .catch(() => {
      status.innerText = "Backend not running";
      status.style.color = "red";
    });
}

setInterval(fetchGesture, 800);
