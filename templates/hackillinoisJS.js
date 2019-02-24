// const instance = require(axios)

function myFunction() {
  var x = document.getElementById("input").value;
  document.getElementById("output").innerHTML = x;
}

function processUrl(url) {
  // validate URL
  var host = "http://localhost:5000/data?host=" + url;
  axios.get(host)
    .then(function (response) {
      // handle success
      console.log(response);
      // getElementById("output") =
    })
    .catch(function (error) {
      // handle error
      console.log(error);
    })
    .then(function () {
      // always executed
    });
}
