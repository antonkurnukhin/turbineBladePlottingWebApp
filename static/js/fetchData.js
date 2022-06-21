function fetchDataFromApi() {
  var formData = new FormData(document.querySelector('form'));
  
  var payload = {};
  formData.forEach( (value, key) => payload[key] = value );
  console.log(payload);

  axios({
    method: 'POST',
    url: '/api',
    headers: { 'Content-type': 'application/json' },
    data: payload,
  })
  .then((response) => {
    draw_chart(response.data)
  }, (error) => {
    console.log(error);
  });
}

window.onload = fetchDataFromApi
