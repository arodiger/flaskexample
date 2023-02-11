let signup = document.querySelector(".signup");
let login = document.querySelector(".login");
let slider = document.querySelector(".slider");
let formSection = document.querySelector(".form-section");
let loginlogin = document.querySelector(".loginclkbtn");
let signupsignup = document.querySelector(".signupclkbtn");

const baseurl = 'http://127.0.0.1:5000/'

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

loginlogin.addEventListener("click", () => {
    getToken();
    document.getElementById("signupbutton").click();
    alert(document.getElementById("loginPassword").value);
});

function getToken(){
    fetch(baseurl + "token").then((res) => res.json()).then((content) => {
        output.innerHTML = JSON.stringify(content, '\n', 2);
        let token = content.data;
        localStorage.setItem('token', token);
    })
    .catch((err) => console.error)
}

