import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, setPersistence, browserSessionPersistence, signInWithEmailAndPassword, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

document.addEventListener("DOMContentLoaded", event => {

    const firebaseConfig = {
        apiKey: "AIzaSyDu6ZEnmOvwj-n6VviffbrLgALNP5fnocI",
        authDomain: "bug-hunt-b860b.firebaseapp.com",
        projectId: "bug-hunt-b860b",
        storageBucket: "bug-hunt-b860b.appspot.com",
        messagingSenderId: "648587053344",
        appId: "1:648587053344:web:a547a2d4294cdd24372f45",
        measurementId: "G-1243JCXJFR"
    };

    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);
    
    // Default Login Method
    document.getElementById('defaultLogin').onclick = function (){
        const loginForm = document.querySelector('#login-account');
        const email = loginForm['email-login'].value;
        const password = loginForm['password-login'].value;
        const rememberMe = loginForm['remember-me'];
        if (!email || !password) {
            alert('Please enter your email and password.');
            return;
        }
        signInWithEmailAndPassword(auth, email, password)
            .then(result => {
                if (!auth.currentUser.emailVerified){
                    auth.signOut();
                    document.getElementById("unverified").style.display = "block";
                    return;
                }
                if(!rememberMe.checked){
                    setPersistence(auth, browserSessionPersistence)
                }
                window.location.href='dashboard.html';
            })
            .catch(error => {
            if (error.code === 'auth/user-not-found') {
                alert('There no user exist with that email');
            }
        
            if (error.code === 'auth/invalid-email') {
                alert('That email address is invalid!');
            }
            console.error(error);
        });
    };
    
    // Google Sign-In
    document.getElementById('googleLogin').onclick = function (){
        const provider = new GoogleAuthProvider();
        const rememberMe = document.getElementById('remember-me');
        provider.setCustomParameters({
            prompt: 'select_account'
        });
        signInWithPopup(auth, provider)
            .then(result => {
                if(!rememberMe.checked){
                    setPersistence(auth, browserSessionPersistence)
                }
                window.location.href='dashboard.html';
            })  
            .catch(console.log);
    };

    const togglePassword = document.querySelector(".eye-icon");
    togglePassword.addEventListener('click', function() {
        const passwordInput = document.getElementById('password-login');
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        const toggle = togglePassword.className === 'fa fa-eye eye-icon' ? 'fa-eye-slash' : 'fa-eye';
        togglePassword.classList.replace(togglePassword.className.split(' ')[1], toggle);
    });

});