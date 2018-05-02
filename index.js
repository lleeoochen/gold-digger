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
	res.send(Object.keys(graphData));
});

//Get request for getting courses
app.get('/getCourses', function (req, res) {
	res.send(Object.keys(graphData[req.query.subject]));
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
				let dashIndex = line.indexOf('-');
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
