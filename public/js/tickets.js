import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore, collection, getDoc, getDocs, doc, query, where, updateDoc, setDoc, addDoc} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js'
import { getPerformance} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-performance.js";
import { buildDataTable} from "./ticketDataTable.js";

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

            // Create cache for specified project
            async function retrieveData() {
                const q = query(collection(db, "projects"), where("ownerUID", "==", user.uid), where("selected", "==", true));
                const querySnapshot = await getDocs(q);
                querySnapshot.forEach((project) => {
                    const projectRef = doc(db, 'projects', project.id);
                    localStorage.setItem('Project ID', project.id);
                    updateDoc(projectRef, {
                    selected: false
                    });
                return projectRef;
                });
            }

            function addElement(text){
                let element = document.createElement('td');
                element.textContent = text;
                return element;
            }
            
            function displayTicket(ticketData, ticketId) {
                const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric'};
                let ticketAge = new Date(ticketData.publish).toLocaleString(undefined, options);
                let ticketModified = new Date(ticketData.lastUpdate).toLocaleString(undefined, options);
                let elementParams = [
                    ticketData.title,
                    ticketData.description,
                    ticketData.priority,
                    ticketData.type,
                    ticketData.author,
                    ticketData.status,
                    ticketAge,
                    ticketModified,
                    ticketData.comments,
                    ticketData.archived
                ];

                const tickets = document.getElementById('tickets');
                let tableRow = document.createElement('tr');
                tableRow.setAttribute('role', 'button');
                tableRow.setAttribute('id', ticketId);
                tickets.appendChild(tableRow);

                elementParams.forEach(param => {
                    let element = addElement(param); // Call addElement function with parameter
                    tableRow.appendChild(element);
                });
            }

            async function loadDynamicElements() {
                await retrieveData();
                const projectID = localStorage.getItem('Project ID');
                const docRef = doc(db, 'projects', projectID);
                const docSnap = await getDoc(docRef);

                // Update a subdocument such as tickets.
                // async function updateTicketsArchive(docSnap) {
                //     const q = query(collection(db, "projects", docSnap.id, 'tickets'));
                //     const querySnapshot = await getDocs(q);
                    
                //     querySnapshot.forEach(async (docs) => {
                //     const ticketRef = doc(db, "projects", docSnap.id, 'tickets', docs.id); // Get the reference to the document
                //       console.log(docs.data());
                //       await updateDoc(ticketRef, {
                //         archived: false
                //       });
                //     });
                // }
                //updateTicketsArchive(docSnap);


                // Set Title
                const title = document.getElementById('title');
                title.innerHTML = 'Project' + ' - ' + docSnap.data().title;

                // Create a new ticket
                const newTicket = document.querySelector('#create-ticket');
                let statusArray = docSnap.data().statusCounter;
                let priorityArray = docSnap.data().priorityCounter;
                let typeArray = docSnap.data().typeCounter;
                newTicket.addEventListener('submit', (e) => {
                    e.preventDefault();
                    const title = newTicket['ticket-title'].value;
                    const priority = newTicket['ticket-priority'].value;
                    const type = newTicket['ticket-type'].value;
                    const description = newTicket['description'].value;

                    async function setDocument(){
                        let tickets = docSnap.data().ticketsFiled;
                        const subRef = doc(db, 'projects', docSnap.id, 'tickets', String(tickets));
                        await setDoc((subRef), {
                            title: title,
                            priority: priority,
                            type: type,
                            description: description,
                            author: user.displayName,
                            status: 'New',
                            publish: Date(),
                            lastUpdate: Date(),
                            comments: '',
                            archived: false
                        });

                        // Ticket Counter
                        const projectRef = doc(db, 'projects', docSnap.id);
                        ++statusArray[0];
                        if(priority === 'Low') ++priorityArray[0]
                        else if(priority === 'Medium') ++priorityArray[1]
                        else if(priority === 'High') ++priorityArray[2]
                        else if(priority === 'Critical') ++priorityArray[3];
                        if(type === 'Bug') ++typeArray[0];
                        else if(type === 'Issue') ++typeArray[1];
                        else if(type === 'Feature Request') ++typeArray[2];
                        updateDoc(projectRef, {
                            ticketsFiled: tickets + 1,
                            statusCounter: statusArray,
                            priorityCounter: priorityArray,
                            typeCounter: typeArray
                        });
                        location.reload();
                    }
                    setDocument();
                });

                // Display tickets
                const q = query(collection(db, "projects", docSnap.id, 'tickets'));
                const querySnapshot = await getDocs(q);
                querySnapshot.forEach((docs) => {
                // Format the dates to be more user-friendly
                displayTicket(docs.data(), docs.id);

                // Edit tickets
                const editTicket = document.querySelector('#edit-ticket');
                document.getElementById(docs.id).onclick = function (){
                    $("#editTicketModal").modal();
                    editTicket['ticket-number'].value = docs.id;
                    editTicket['ticket-title'].value = docs.data().title;
                    editTicket['ticket-priority'].value = docs.data().priority;
                    editTicket['ticket-status'].value = docs.data().status;
                    editTicket['ticket-type'].value = docs.data().type;
                    editTicket['description'].value = docs.data().description;
                    if (docs.data().comments != undefined) editTicket['comments'].value = docs.data().comments;
                    editTicket['archiveTicket'].checked = docs.data().archived;

                    // Needed for tracking original value
                    let status = editTicket['ticket-status'].value;
                    let priority = editTicket['ticket-priority'].value;
                    let type = editTicket['ticket-type'].value;
                    statusArray = docSnap.data().statusCounter;
                    priorityArray = docSnap.data().priorityCounter;
                    typeArray = docSnap.data().typeCounter;
                    if (status === 'New') --statusArray[0];
                    else if (status === 'In Progress') --statusArray[1];
                    else if (status === 'Resolved') --statusArray[2];
                    if(priority === 'Low') --priorityArray[0];
                    else if(priority === 'Medium') --priorityArray[1];
                    else if(priority === 'High') --priorityArray[2];
                    else if(priority === 'Critical') --priorityArray[3];
                    if(type === 'Bug') --typeArray[0];
                    else if(type === 'Issue') --typeArray[1];
                    else if(type === 'Feature Request') --typeArray[2];
                }
                });
                
                // From ticketDataTable.js
                buildDataTable();

                // Submit Edit
                // Take the value from edit ticket and save it, for use later
                // Might be able to share, for optimization?
                const editTicket = document.querySelector('#edit-ticket');
                editTicket.addEventListener('submit', (e) => {
                    e.preventDefault();

                    const projectRef = doc(db, 'projects', docSnap.id);
                    let status = editTicket['ticket-status'].value;
                    let priority = editTicket['ticket-priority'].value;
                    let type = editTicket['ticket-type'].value;
                    if (status === 'New') ++statusArray[0];
                    else if (status === 'In Progress') ++statusArray[1];
                    else if (status === 'Resolved') ++statusArray[2];
                    if(priority === 'Low') ++priorityArray[0];
                    else if(priority === 'Medium') ++priorityArray[1];
                    else if(priority === 'High') ++priorityArray[2];
                    else if(priority === 'Critical') ++priorityArray[3];
                    if(type === 'Bug') ++typeArray[0];
                    else if(type === 'Issue') ++typeArray[1];
                    else if(type === 'Feature Request') ++typeArray[2];
                    updateDoc(projectRef, {
                        statusCounter: statusArray,
                        priorityCounter: priorityArray,
                        typeCounter: typeArray
                    });

                    async function updateDocument(){
                        const subRef = doc(db, 'projects', docSnap.id, 'tickets', String(editTicket['ticket-number'].value));
                        await updateDoc((subRef), {
                            title: editTicket['ticket-title'].value,
                            priority: editTicket['ticket-priority'].value,
                            type: editTicket['ticket-type'].value,
                            description: editTicket['description'].value,
                            status: status,
                            lastUpdate: Date(),
                            comments: editTicket['comments'].value,
                            archived: editTicket['archiveTicket'].checked
                        });
                    // Possible Change, don't reload create a function for update? innerhtml etc.
                        location.reload();
                    }
                    updateDocument();
                });
            }

            loadDynamicElements();

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