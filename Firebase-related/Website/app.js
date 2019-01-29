// direction facing
const displayUR5Div = document.querySelector('#URinfo');

// loaded program
const loadedProgramDiv = document.querySelector('#loadedProgramInfo');

// program status
const programStatusDiv = document.querySelector('#programStatusInfo');

// conrods picked
const conrodsPickedDiv = document.querySelector('#conrodsPicked');

// nuts picked
const nutsPickedDiv = document.querySelector('#nutsPicked');

// create elements to receive data from Google Firebase
let directionHeader = document.createElement('h4');
let loadedProgramHeader = document.createElement('h4');
let programStateHeader = document.createElement('h4');
let conrodsPickedHeader = document.createElement('h4');
let nutsPickedHeader = document.createElement('h4');

// get document reference to Google Firebase
var positionDocRef = db.collection("UR5").doc("position");
var loadedProgramDocRef = db.collection("UR5").doc("loadedProgram");
var programStateDocRef = db.collection("UR5").doc("programState");
var itemCountDocRef = db.collection("UR5").doc("itemCount");

// add header3 class
directionHeader.classList.add('header3');
loadedProgramHeader.classList.add('header3');
programStateHeader.classList.add('header3');
conrodsPickedHeader.classList.add('header3');
nutsPickedHeader.classList.add('header3');

// Listens to the Firebase server constantly for updates
positionDocRef
	.onSnapshot(function (doc) {
		directionHeader.textContent = doc.data().direction;
		displayUR5Div.appendChild(directionHeader);
	});

loadedProgramDocRef
	.onSnapshot(function (doc) {
		loadedProgramHeader.textContent = doc.data().loadedProgram;
		loadedProgramDiv.appendChild(loadedProgramHeader);
	});

programStateDocRef
	.onSnapshot(function (doc) {
		programStateHeader.textContent = doc.data().programState;
		programStatusDiv.appendChild(programStateHeader);
	});

itemCountDocRef
	.onSnapshot(function (doc) {
		conrodsPickedHeader.textContent = doc.data().conrodCount;
		nutsPickedHeader.textContent = doc.data().nutCount;
		conrodsPickedDiv.appendChild(conrodsPickedHeader);
		nutsPickedDiv.appendChild(nutsPickedHeader);
	});