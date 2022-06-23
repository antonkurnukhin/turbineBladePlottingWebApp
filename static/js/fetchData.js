function preLoad() {
  // TODO
  projectName = window.localStorage.getItem('projectName')

  if (projectName == null) {
    fetchDataFromApi()
  } else {
    window.localStorage.getItem('projectData')
  }
}

function fetchDataFromApi() {
  var formData = new FormData(document.querySelector('form'));
  var payload = {};

  formData.forEach( (value, key) => payload[key] = value );

  axios({
    method: 'POST',
    url: '/api',
    headers: { 'Content-type': 'application/json' },
    data: payload,
  })
  .then((response) => {
    draw_all_data(response.data)
  }, (error) => {
    console.log(error);
  });
}

window.onload = fetchDataFromApi
