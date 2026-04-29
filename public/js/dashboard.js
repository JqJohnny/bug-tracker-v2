import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore, collection, setDoc, getDocs, doc, query, where, updateDoc} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js'
import { getPerformance} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-performance.js";
import { buildDataTable} from "./projectDataTable.js";

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
    const db = getFirestore(app);
    const perf = getPerformance(app);

    // Signed in
    onAuthStateChanged(auth, (user) => {
        if(user){
            // Display Username
            document.getElementById('username').innerHTML = user.displayName;
            
            // Tracks all projects
            let unresolved = 0;
            let ticketTotal = 0;
            let ticketsComplete = 0;
            // Create Project Button
            const newProjectForm = document.querySelector('#create-project');
            newProjectForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const title = newProjectForm['project-title'].value;
                const contributors = user.displayName + ' ' + newProjectForm['contributors'].value;
                const description = newProjectForm['description'].value;
                const visibility = newProjectForm['project-visibility'].value;
                async function setDocument(){
                    await setDoc(doc(collection(db, 'projects')), {
                        title: title,
                        ownerUID: user.uid,
                        ownerName: user.displayName,
                        contributors: contributors,
                        description: description,
                        lastModified: Date(),
                        selected: false,
                        visibility: visibility,
                        ticketsFiled: 0,
                        statusCounter: [0, 0, 0], // New, In Progress, Resolved
                        priorityCounter: [0, 0, 0, 0], // Low, Medium, High, Critical
                        typeCounter: [0, 0, 0], // Bug, Issue, Feature Request
                    });
                    location.reload();
                }
                setDocument();
            });
            
            function addElement(text){
                let element = document.createElement('td');
                element.textContent = text;
                return element;
            }

            // Display Projects
            async function displayProject() {
                function buildTable(docs, projects){
                    let title = addElement(docs.data().title);
                    let contributors = addElement(docs.data().contributors);
                    let description = addElement(docs.data().description);
                    let tableRow = document.createElement('tr');
                    tableRow.setAttribute('role', 'button');
                    tableRow.setAttribute('id', docs.id);
                    projects.appendChild(tableRow);
                    tableRow.appendChild(title);
                    tableRow.appendChild(description);
                    tableRow.appendChild(contributors);
                    let ticketsFiled = docs.data().ticketsFiled;
                    let ticketsResolved = docs.data().statusCounter[2];
                    unresolved += docs.data().statusCounter[1] + docs.data().statusCounter[0];
                    ticketTotal += ticketsFiled;
                    ticketsComplete += ticketsResolved;
                    document.getElementById(docs.id).onclick = async function (){
                        const selectRef = doc(db, 'projects', docs.id);
                        await updateDoc(selectRef, {
                        selected: true
                    });
                    location.href = "tickets.html";
                    }
                }
                var q = query(collection(db, "projects"), where("ownerUID", "==", user.uid));
                var querySnapshot = await getDocs(q);
                const publicProjects = document.getElementById('publicProjects');
                // Build Public Projects
                querySnapshot.forEach((docs) => {
                    buildTable(docs, publicProjects);
                });
                
                q = query(collection(db, "projects"), where("visibility", "==", "Public"));
                querySnapshot = await getDocs(q);
                // Build Private Projects
                const privateProjects = document.getElementById('privateProjects');
                querySnapshot.forEach((docs) => {
                    buildTable(docs, privateProjects);
                });
                dashboard();
                buildDataTable()
            }

            displayProject();
            function dashboard() {
                const unresolvedTickets = document.getElementById("unresolved-tickets");
                unresolvedTickets.innerHTML = unresolved;

                const progressBar = document.getElementById("progress-bar");
                let percentage = Math.round((100 * ticketsComplete) / ticketTotal);
                if (!isNaN(percentage)) {
                    progressBar.innerHTML = percentage + '%';
                    const bar = document.getElementById('progressBar');
                    bar.setAttribute('style', 'width: ' + percentage +'%')
                }
            }
            // Sign Out Button
            const signOut = document.getElementById("sign-out");
            signOut.onclick = () => auth.signOut();
        } else {
            // Redirect signed out users to login page
            localStorage.clear();
            window.location.href='login.html';
        }
        
    });

});