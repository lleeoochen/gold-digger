var path = require('path');
var fs = require('fs');
var readline = require('readline');
var express = require('express');
var app = express();
var PORT = process.env.PORT || 5000;

//Global Variables
var count = 0;
var graphData = {};

//Host static website from public/
app.use(express.static(path.join(__dirname, 'public')));

//Get request for getting subjects
app.get('/getSubjects', function (req, res) {
	res.send(Object.keys(graphData).sort());
});

//Get request for getting courses
app.get('/getCourses', function (req, res) {
	res.send(Object.keys(graphData[req.query.subject]).sort(course_comparator));
});

//Get request for getting graph data
app.get('/getGraph', function (req, res) {
	res.send(graphData[req.query.subject][req.query.courseID]);
});

//Start server at PORT
var server = app.listen(PORT, function () {
	var host = server.address().address;
	var port = server.address().port;
	console.log(`Listening on ${ port }.`);

	loadGraphData();
});

//Load CSV file
function loadGraphData() {
	readline.createInterface({input: fs.createReadStream('source/DataGraph/data.csv')})
		.on('line', function (line) {
			try {
				let commaIndex = line.indexOf(',');
				let dashIndex = line.lastIndexOf('-');
				let subject = line.substring(0, dashIndex);
				let courseID = line.substring(dashIndex + 1, commaIndex);
				let enrollData = (line.includes('nan')) ? [] : JSON.parse(line.substring(commaIndex + 1));

				if (graphData[subject] === undefined)
					graphData[subject] = {};
				graphData[subject][courseID] = enrollData;
			}
			catch (err) {
				console.log(err);
			}
		})
		.on('close', function () {
			console.log('Graph data loaded.');
			// console.log(graphData);
		});
}

//Sort comparator
function course_comparator(a, b) {
	let acode = "Z", bcode = "Z";

	if (a.charCodeAt(a.length - 1) > "9".charCodeAt(0)) {
		acode = a[a.length - 1];
		a = a.substr(0, a.length - 1);
	}

	if (b.charCodeAt(b.length - 1) > "9".charCodeAt(0)) {
		bcode = b[b.length - 1];
		b = b.substr(0, b.length - 1);
	}

	if (a.length !== b.length)
		return a.length - b.length;

	if (a !== b)
		return a - b;

	return acode.charCodeAt(0) - bcode.charCodeAt(0);
}