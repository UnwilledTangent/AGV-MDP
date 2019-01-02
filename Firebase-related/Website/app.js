//db.collection("UR5").get().then((querySnapshot) => {
//	querySnapshot.forEach((doc) => {
//		console.log(`${doc.id} => ${doc.data().direction}`);
//	});
//});

const displayDirection = document.querySelector('#direction');
let directionHeader = document.createElement('h2');


var docRef = db.collection("UR5").doc("position");

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
db.collection("UR5").doc("position")
	.onSnapshot(function (doc) {
		directionHeader.textContent = "UR5 is facing: " + doc.data().direction;
		displayDirection.appendChild(directionHeader);
	});