//db.collection("UR5").get().then((querySnapshot) => {
//	querySnapshot.forEach((doc) => {
//		console.log(`${doc.id} => ${doc.data().direction}`);
//	});
//});

const displayUR5Info = document.querySelector('#URinfo');
let directionHeader = document.createElement('h2');
let loadedProgramHeader = document.createElement('h2');
let programStateHeader = document.createElement('h2');


var positionDocRef = db.collection("UR5").doc("position");
var loadedProgramDocRef = db.collection("UR5").doc("loadedProgram");
var programStateDocRef = db.collection("UR5").doc("programState");

// Reads the Firebase server once
//docRef.get().then(function (doc) {
//	if (doc.exists) {
//		directionHeader.textContent = "UR5 is facing: " + doc.data().direction;
//		displayDirection.appendChild(directionHeader);
//	} else {
//		// doc.data() will be undefined in this case
//		console.log("No such document");
//	}
//})

// Listens to the Firebase server constantly for updates
positionDocRef
	.onSnapshot(function (doc) {
		directionHeader.textContent = "UR5 is facing: " + doc.data().direction;
		displayUR5Info.appendChild(directionHeader);
	});

loadedProgramDocRef
	.onSnapshot(function (doc) {
		loadedProgramHeader.textContent = doc.data().loadedProgram;
		displayUR5Info.appendChild(loadedProgramHeader);
	});

programStateDocRef
	.onSnapshot(function (doc) {
		programStateHeader.textContent = doc.data().programState;
		displayUR5Info.appendChild(programStateHeader);
	});
