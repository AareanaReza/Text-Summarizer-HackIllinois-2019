const axios = require('axios');

function myFunction() {
  var x = document.getElementById("input").value;
  document.getElementById("output").innerHTML = x;
}

function processUrl(url) {
  // validate URL
  axios.get(url)
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
