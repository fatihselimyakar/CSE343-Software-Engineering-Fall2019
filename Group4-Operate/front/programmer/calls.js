var socket = io.connect('http://localhost:4001');

document.getElementById("ProjectPathButton").addEventListener('click', function(){
	socket.emit('post', {
		origin:"4",
		destination: "2",
		action: "upload",
		ProjectName: document.getElementById("ProjectName").value,
		ProjectPath: document.getElementById("ProjectPath").value
		
	});
	document.getElementById("ProjectPath").value = "";
	document.getElementById("ProjectName").value = "";
});
document.getElementById("SqlProjectPathButton").addEventListener('click', function(){
	socket.emit('post', {
		origin:"4",
		destination: "2",
		action: "uploadsql",
		ProjectName: document.getElementById("ProjectName").value,
		ProjectPath: document.getElementById("ProjectPath").value
		
	});
	document.getElementById("ProjectPath").value = "";
	document.getElementById("ProjectName").value = "";
});
