import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore, collection, getDocs, query, where} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js'

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
const db = getFirestore(app);

// Signed in
onAuthStateChanged(auth, (user) => {
  if(user){
    let issues = 0;
    let bugs = 0;
    let featureRequests = 0;

    let low = 0;
    let medium = 0;
    let high = 0;
    let critical = 0;

    let newStat = 0;
    let inProgress = 0;
    let resolved = 0;
    async function queryData() {
      const q = query(collection(db, "projects"), where("ownerUID", "==", user.uid));
      const querySnapshot = await getDocs(q);
      // Computes the tickets for all projects
      querySnapshot.forEach((docs) => {
        issues += docs.data().typeCounter[0]; 
        bugs += docs.data().typeCounter[1]; 
        featureRequests += docs.data().typeCounter[2];
        
        low += docs.data().priorityCounter[0];
        medium += docs.data().priorityCounter[1];
        high += docs.data().priorityCounter[2];
        critical += docs.data().priorityCounter[3];

        newStat += docs.data().statusCounter[0];
        inProgress += docs.data().statusCounter[1];
        resolved += docs.data().statusCounter[2];
      });

      // Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("ticketsByType");
var pieType = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Issues", "Bugs", "Feature Requests"],
    datasets: [{
      data: [issues, bugs, featureRequests],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});

var ctx = document.getElementById("ticketsByPriority");
var piePriority = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Low", "Medium", "High", "Critical"],
    datasets: [{
      data: [low, medium, high, critical],
      backgroundColor: ['#1cc88a', '#f6c23e', '#fd7e14', '#e74a3b'],
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});

var ctx = document.getElementById("ticketsByStatus");
var pieStatus = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["New", "In Progress", "Resolved"],
    datasets: [{
      data: [newStat, inProgress, resolved],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
  }
    queryData();
    
  } else {
    // Redirect signed out users to login page
    window.location.href='login.html';
  }
  
});
