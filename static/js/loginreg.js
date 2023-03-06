let signup = document.querySelector(".signup");
let login = document.querySelector(".login");
let slider = document.querySelector(".slider");
let formSection = document.querySelector(".form-section");
let loginlogin = document.querySelector(".loginclkbtn");
let signupsignup = document.querySelector(".signupclkbtn");


// the baseurl is passed in thru the paramaters from the server based on configuration.ini file 
// swap bw production and development via config ini file 
// const baseurl = 'http://127.0.0.1:5000/'
const baseurl = paramURL;


// on document load we want this to be called first via capture:true 
// we should consider removing this event listener once cookie is set 
// so we don't waste calls to the server if page is reloaded etc.
document.addEventListener(
    'load', 
    e => {

        InitializeBrowserCookies();

        let fingerprint = getCookie('cookiePayloadFingerprint')
        console.log(fingerprint);
    }, 
    {capture: true}
)

signup.addEventListener("click", () => {
	slider.classList.add("moveslider");
	formSection.classList.add("form-section-move");
});

login.addEventListener("click", () => {
	slider.classList.remove("moveslider");
	formSection.classList.remove("form-section-move");
});

signupsignup.addEventListener("click", () => {
    alert(document.getElementById("signupPassword").value);
    alert(document.getElementById("confirmSignupPassword").value);
    });
      

function getCookie(cookieName) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
        let [key,value] = el.split('=');
        cookie[key.trim()] = value;
    })
    return cookie[cookieName];
    }    


loginlogin.addEventListener("click", () => {

    let fingerprint = getCookie('cookiePayloadFingerprint')
    let my_token = retrieveToken();

    document.getElementById("signupbutton").click();
    // alert(document.getElementById("loginPassword").value);
});

// called with body onload
async function InitializeBrowserCookies(){
    try{

        const requestOptions = {
            method: 'POST', 
            Headers: { 
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({ 
                title: 'Initialize Browser Cookies' })
        };

        const url = baseurl + 'initcookies';
        const response = await fetch( url , requestOptions);

    }
    catch(err){
        return err;
    }

}

async function retrieveToken(){
    try{
        // retrieve the login data to send with the token request in the body field of the POST
        const login_Email = document.getElementById("loginEmail").value;
        const login_Password = document.getElementById("loginPassword").value;
        const encodedLoginEmail = btoa(login_Email);
        const encodedLoginPassword = btoa(login_Password);
        const requestOptions = {
            method: 'POST', 
            Headers: { 
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({ 
                title: 'Fetch token POST', 
                username: encodedLoginEmail, 
                password: encodedLoginPassword })
        };

        const url = baseurl + 'gentoken';
        const response = await fetch( url , requestOptions);
        const data = await response.json();
        // const { jwt_token } = await response.json();

        console.log(data);
        console.log(data.token);
        localStorage.setItem('token', data.token);
        
        return data;
    }
    catch(err){
        return err;
    }
}


function getToken(){
    const requestOptions = { method:'POST', Headers:{ Accept: 'application.json', 'Content-Type':'application/json' }};
    fetch(baseurl + 'gentoken', requestOptions).then(res => res.json()).then((content) => {
        // output.innerHTML = JSON.stringify(content, '\n', 2);
        let token = content.data;
        console.log(token);
        localStorage.setItem('token', token);
        console.log(token);
    })
    .catch((err) => console.error)
}

