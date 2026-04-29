import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import {getAuth,onAuthStateChanged} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import {getFirestore, collection, getDocs, doc, query, where} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyDu6ZEnmOvwj-n6VviffbrLgALNP5fnocI",
  authDomain: "bug-hunt-b860b.firebaseapp.com",
  projectId: "bug-hunt-b860b",
  storageBucket: "bug-hunt-b860b.appspot.com",
  messagingSenderId: "648587053344",
  appId: "1:648587053344:web:a547a2d4294cdd24372f45",
  measurementId: "G-1243JCXJFR",
};

// Set new default font family and font color to mimic Bootstrap's default styling
(Chart.defaults.global.defaultFontFamily = "Nunito"),
  '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#858796";

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + "").replace(",", "").replace(" ", "");
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = typeof thousands_sep === "undefined" ? "," : thousands_sep,
    dec = typeof dec_point === "undefined" ? "." : dec_point,
    s = "",
    toFixedFix = function (n, prec) {
      var k = Math.pow(10, prec);
      return "" + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : "" + Math.round(n)).split(".");
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || "").length < prec) {
    s[1] = s[1] || "";
    s[1] += new Array(prec - s[1].length + 1).join("0");
  }
  return s.join(dec);
}

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

onAuthStateChanged(auth, (user) => {
  if (user) {
    let ticketsPerMonth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    async function queryProjects() {
      const q = query(collection(db, "projects"), where("ownerUID", "==", user.uid));
      const querySnapshot = await getDocs(q);
      // Computes the tickets for all projects
      const queryPromises = [];
      querySnapshot.forEach((project) => {
        const projectRef = doc(db, 'projects', project.id);
        queryPromises.push(queryTickets(projectRef)); // Push the promise returned by queryTickets
      });
      await Promise.all(queryPromises);
      barChart(ticketsPerMonth)
    }

    async function queryTickets(docSnap) {
      const q = query(collection(db, "projects", docSnap.id, 'tickets'), where("status", "==", "Resolved"));
      const querySnapshot = await getDocs(q);
      querySnapshot.forEach((ticket) => {
        let dateObject = new Date(ticket.data().publish);
        let yearIndex = dateObject.getFullYear();
        //console.log(yearIndex);
        let monthIndex = dateObject.getMonth(); // This will return the month index (0-indexed)
        ticketsPerMonth[monthIndex]++;
      });
    }

    queryProjects();

    // Bar Chart Example
    function barChart(ticketsMonth) {
    var ctx = document.getElementById("ticketPeriodicalCounter");
    var myBarChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        datasets: [
          {
            label: "Tickets Resolved",
            backgroundColor: "#4e73df",
            hoverBackgroundColor: "#2e59d9",
            borderColor: "#4e73df",
            data: ticketsMonth,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0,
          },
        },
        scales: {
          xAxes: [
            {
              time: {
                unit: "month",
              },
              gridLines: {
                display: false,
                drawBorder: false,
              },
              ticks: {
                maxTicksLimit: 12,
              },
              maxBarThickness: 25,
            },
          ],
          yAxes: [
            {
              ticks: {
                min: 0,
                max: 25,
                maxTicksLimit: 10,
                padding: 10,
                callback: function (value, index, values) {
                  return number_format(value);
                },
              },
              gridLines: {
                color: "rgb(234, 236, 244)",
                zeroLineColor: "rgb(234, 236, 244)",
                drawBorder: false,
                borderDash: [2],
                zeroLineBorderDash: [2],
              },
            },
          ],
        },
        legend: {
          display: false,
        },
        tooltips: {
          titleMarginBottom: 10,
          titleFontColor: "#6e707e",
          titleFontSize: 14,
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: "#dddfeb",
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          caretPadding: 10,
          callbacks: {
            label: function (tooltipItem, chart) {
              var datasetLabel =
                chart.datasets[tooltipItem.datasetIndex].label || "";
              return datasetLabel + ": " + number_format(tooltipItem.yLabel);
            },
          },
        },
      },
    });
  }
  }
});
