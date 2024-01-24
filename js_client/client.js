const contentContainer = document.getElementById('content-container')
const loginForm = document.getElementById('login-form')
const baseEndpoint = "http://localhost:8000/api"
if (loginForm) {
  // handle login form
  loginForm.addEventListener('submit', handleLogin)
}

function handleLogin(event) {
  event.preventDefault()
  // extract the login data
  const loginEndpoint = `${baseEndpoint}/token/`
  let loginFormData = new FormData(loginForm)
  let loginObjectData = Object.fromEntries(loginFormData)
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(loginObjectData)
  }
  fetch(loginEndpoint, options)
  .then(response=>{
    console.log(response)
    return response.json()
  })
  .then(authData => {
    handleAuthData(authData, getProductList)
  })
  .catch(err=> {
    console.log('err', err)
  })
}

function handleAuthData(authData, callback) {
  localStorage.setItem('access', authData.access);

  localStorage.setItem('refresh', authData.refresh);
  if (callback) {
    callback();
  }
}

function writeToContentContainer(data){
  if (contentContainer) {
    contentContainer.innerHTML = "<pre>" + 
    JSON.stringify(data, null, 4) + "</pre>"
  }
  
}

function getFetchOptions(method, body){
  return {
    method: method === null ? "GET" : method,
    headers: {
      "content-type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem('access')}`
    },
    body: body ? body: null
  }
}

function isTokenNotValid(jsonData){
  if(jsonData.code && jsonData.code === "token_not_valid"){
    alert("please log in again")
    return false
  }
  return true
}

function validateJWTToken() {
  // fetch
  const endpoint = `${baseEndpoint}/token/verify/`
  const options = {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({
          token: localStorage.getItem('access')
      })
  }
  fetch(endpoint, options)
  .then(response=>response.json())
  .then(x=> {
      // refresh token
      isTokenNotValid(x)
  })
}

function getProductList(){
  const endpoint = `${baseEndpoint}/products/`
  options = getFetchOptions()
  fetch(endpoint, options)
  .then(response=> {
    return response.json()
  })
  .then(data =>  {
    const validData = isTokenNotValid(data)
    if (validData){
      writeToContentContainer(data)
    }

  })
}

validateJWTToken()