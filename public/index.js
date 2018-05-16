//Main
loadSubjects('subject-selector1', 'course-selector1');
loadSubjects('subject-selector2', 'course-selector2');
loadSubjects('subject-selector3', 'course-selector3');
loadSubjects('subject-selector4', 'course-selector4');

//Handle click from html button
//FIX THIS LATER SO THAT YOU CAN GET BOTH DATALISTS IN ONE GRAPH
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

//Function that handles displaying graph in html element with id 'visualization'
//	datalist: items to be displayed
//	groupNum: the group for the data to be displayed in
function drawGraph(dataLists) {
	let container = document.getElementById('visualization');
	container.innerHTML = null;

	//list of dataLists for each subject selected

	var items = [];
	for(let i = 0; i < dataLists.length; i++){
		for (let j = 0; j < dataLists[i].length; j++) {

			if (j < 8)
				items.push({x: j, y: dataLists[i][j], group: i});

			if (j >= 8 && i < 19)
				items.push({x: j, y: dataLists[i][j], group: i});

			if (j >= 19)
				items.push({x: j, y: dataLists[i][j], group: i});

		}
	}

	var dataset = new vis.DataSet(items);
	var options = {
		zoomable: false,
		width: '100%',
		height: '300px',
		dataAxis: {
			left: {
				range: {
					min: 0, max: 1.1
				},
				format: (value) => (value * 100 + '%')
			}
		},
		shaded: {
			enabled: false
		}
	};

	var graph2d = new vis.Graph2d(container, dataset, options);
}
