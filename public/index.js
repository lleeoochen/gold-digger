//Main
loadSubjects('subject-selector1', 'course-selector1');
loadSubjects('subject-selector2', 'course-selector2');
loadSubjects('subject-selector3', 'course-selector3');
loadSubjects('subject-selector4', 'course-selector4');

//Handle click from html button
function loadGraph() {
	let subject1 = document.getElementById('subject-selector1').value;
	let courseID1 = document.getElementById('course-selector1').value;
	
	let subject2 = document.getElementById('subject-selector2').value;
	let courseID2 = document.getElementById('course-selector2').value;

	let subject3 = document.getElementById('subject-selector3').value;
	let courseID3 = document.getElementById('course-selector3').value;

	let subject4 = document.getElementById('subject-selector4').value;
	let courseID4 = document.getElementById('course-selector4').value;

	//list of promises from requesting subject/course information for all selected courses
	let urls = []
	urls.push('/getGraph?subject=' + subject1 + '&courseID=' + courseID1);
	urls.push('/getGraph?subject=' + subject2 + '&courseID=' + courseID2);
	urls.push('/getGraph?subject=' + subject3 + '&courseID=' + courseID3);
	urls.push('/getGraph?subject=' + subject4 + '&courseID=' + courseID4);

	sendListRequest(urls, (result) => {
		drawGraph(results);
	});
}

//Load courses to subject selector
function loadSubjects(subjectSelectorId, courseSelectorId) {
	let selector = document.getElementById(subjectSelectorId);
	selector.innerHTML = null;

	sendRequest('/getSubjects', function(subjectList) {
		for (let i = 0; i < subjectList.length; i++) {
			let subject = subjectList[i];
			let option = document.createElement('option');
			option.setAttribute('value', subject);
			option.innerText = subject;
			selector.appendChild(option);
		}
		loadCourses(subjectSelectorId, courseSelectorId);
	});
}

//Load courses to course selector
//	subjectSelectorId: id specifying which subject selector html list
//	courseSelectorId: id specifying which course selctor html list
//	subject: currently selected subject
function loadCourses(subjectSelectorId, courseSeletorId) {
	let subject = document.getElementById(subjectSelectorId).value;
	let selector = document.getElementById(courseSeletorId);
	selector.innerHTML = null;

	sendRequest('/getCourses?subject=' + subject, function(courseList) {
		for (let i = 0; i < courseList.length; i++) {
			let course = courseList[i];
			let option = document.createElement('option');
			option.setAttribute('value', course);
			option.innerText = course;
			selector.appendChild(option);
		}
	});
}

//Function to send server request
function sendRequest(url, callback) {
	fetch(url).then(function(response) {
		return response.json();
	})
	.then(function(result) {
		callback(result);
	});
}

//Function to send multiple server request
function sendListRequest(url_list, callback) {

	//get json promises of all fetch requests
	let promises = url_list.map(url => fetch(url).then(result => result.json()));

	//create 2-D array of results for the graph to use
	Promise.all(promises).then(results => {
		drawGraph(results);
	});
}

//Get color based on index
function randomColor(index) {
	switch(index) {
		case 0:
			return '#33ccff';
		case 1:
			return '#ff4000';
		case 2:
			return '#4000ff';
		case 3:
			return '#ffbf00';
		default:
			return 'black';
	}
}

//Return group style based on index
function groupOptions(subject, course, index) {
	name = subject + " " + course;
	return {
		id: index,
		content: name,
		options: {
			style:'line',
			drawPoints: {
				enabled: false,
			}
		},
		style: 'stroke:' + randomColor(index) + ';'
	};
}

function passtimeOptions(index) {
	let color = (index % 2 == 0) ? 'grey' : 'white';

	return {
		id: index,
		options: {
			style:'line',
			drawPoints: {
				enabled: false,
			},
			excludeFromLegend: true,
			shaded: {
				enabled: true,
				orientation: 'bottom',
				style: 'fill:' + color
			}
		},
		style: 'stroke:white;'
	};
}

//Function that handles displaying graph in html element with id 'visualization'
//	datalist: items to be displayed
//	groupNum: the group for the data to be displayed in
function drawGraph(dataLists) {
	let container = document.getElementById('visualization');
	container.innerHTML = null;
	var groups = new vis.DataSet();
	var dataset = new vis.DataSet();

	//list of dataLists for each subject selected
	for(let i = 0; i < dataLists.length; i++){
		//getting subject name for display on graph key
		let id = "subject-selector" + (i+1)
		let subject = document.getElementById(id).value;

		//getting the course name for display on the graph key
		id = "course-selector" + (i+1)
		let course = document.getElementById(id).value;

		groups.add(groupOptions(subject, course, i));
		for (let j = 0; j < dataLists[i].length; j++)
			dataset.add({x: j, y: dataLists[i][j], group: i});
	}

	//Add vertical lines for pass time
	groups.add(passtimeOptions(100));
	groups.add(passtimeOptions(101));
	groups.add(passtimeOptions(102));
	dataset.add({x: 0, y: 1.1, group: 100});
	dataset.add({x: 8, y: 1.1, group: 100});
	dataset.add({x: 8, y: 1.1, group: 101});
	dataset.add({x: 19, y: 1.1, group: 101});
	dataset.add({x: 19, y: 1.1, group: 102});
	dataset.add({x: (dataLists[0].length - 1), y: 1.1, group: 102});

	var options = {
		zoomable: false,
		width: '100%',
		height: '300px',
		dataAxis: {
			left: {
				title: {
					text: "Enrollment Percentage",
					style: "stroke: #000000"
				},
				range: {
					min: 0, max: 1.1
				},
				format: (value) => (value * 100 + '%')
			}
		},
		legend: {
			left:{
				position:"bottom-right"
			}
		},
		format: {
			minorLabels: (date, scale, step) => {

				if (date == 0)
					return 'Pass 1';

				else if (date == 8)
					return 'Pass 2';

				else if (date == 19)
					return 'Pass 3';

				else
					return '';
			},
			majorLabels: (date, scale, step) => {
				return 'Time (Course Selection Period)';
			}
		}
	};

	var graph2d = new vis.Graph2d(container, dataset, groups, options);
}
