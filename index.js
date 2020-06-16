var dataMaster = new DataMaster();

main();

//Main
function main() {
	dataMaster.loadData().then(res => {
		loadSubjects('subject-selector1', 'course-selector1');
		loadSubjects('subject-selector2', 'course-selector2');
		loadSubjects('subject-selector3', 'course-selector3');
		loadSubjects('subject-selector4', 'course-selector4');
	});
}

//Handle click from html button
async function loadGraph() {

	let results = [];
	let courseNames = [];

	for (let i = 1; i <= 4; i++) {
		let subject = document.getElementById('subject-selector' + i).value;
		let course  = document.getElementById('course-selector' + i).value;
		results.push(dataMaster.getGraph(subject, course));
		courseNames.push(subject + " " + course);
	}

	drawGraph(results, courseNames);
	analyze(results, courseNames);
}

//Load courses to subject selector
function loadSubjects(subjectSelectorId, courseSelectorId) {
	let selector = document.getElementById(subjectSelectorId);
	selector.innerHTML = null;

	let subjectList = dataMaster.getSubjects();
	for (let i = 0; i < subjectList.length; i++) {
		let subject = subjectList[i];
		let option = document.createElement('option');
		option.setAttribute('value', subject);
		option.innerText = subject;
		selector.appendChild(option);
	}
	loadCourses(subjectSelectorId, courseSelectorId);
}

//Load courses to course selector
function loadCourses(subjectSelectorId, courseSeletorId) {
	let subject = document.getElementById(subjectSelectorId).value;
	let selector = document.getElementById(courseSeletorId);
	selector.innerHTML = null;

	let courseList = dataMaster.getCourses(subject);
	for (let i = 0; i < courseList.length; i++) {
		let course = courseList[i];
		let option = document.createElement('option');
		option.setAttribute('value', course);
		option.innerText = course;
		selector.appendChild(option);
	}
}

//Get color based on index
function randomColor(index) {
	let color = "";
	if (index == 0)      color = 'line line-cyan';
	else if (index == 1) color = 'line line-red';
	else if (index == 2) color = 'line line-blue';
	else if (index == 3) color = 'line line-yellow';
	return color;
}

//Return group style based on index
function groupOptions(courseName, index) {
	return {
		id: index,
		content: courseName,
		options: {
			style:'line',
			drawPoints: {
				enabled: false,
			}
		},
		className: randomColor(index)
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
				style: 'color:' + color
			}
		},
		style: 'color: white;'
	};
}

function drawGraph(dataLists, courseNames) {
	let container = document.getElementById('visualization');
	container.innerHTML = null;
	var groups = new vis.DataSet();
	var dataset = new vis.DataSet();

	//list of dataLists for each subject selected
	for(let i in dataLists){
		groups.add(groupOptions(courseNames[i], i));
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
					style: "color: #000000"
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
				if (date == 0)       return 'Pass 1';
				else if (date == 8)  return 'Pass 2';
				else if (date == 19) return 'Pass 3';
				else                 return '';
			},
			majorLabels: (date, scale, step) => {
				return 'Time (Course Selection Period)';
			}
		}
	};

	var graph2d = new vis.Graph2d(container, dataset, groups, options);
}

function analyze(dataLists, courseNames) {
	let filledUpDays = [];

	// Collect the first day that each course fills up
	for(let i in dataLists)
		for (let j in dataLists[i])
			if (dataLists[i][j] >= 1) {
				filledUpDays.push({
					course: courseNames[i],
					date: j
				});
				break;
			}

	// Sort list by first days
	filledUpDays.sort((a, b) => a.date - b.date);

	// Construct a string of courses ordered by its priority
	let analysis = "Please select courses in this order: ";
	for (let i in filledUpDays)
		analysis += filledUpDays[i].course.bold() + ", ";
	analysis = analysis.slice(0, -2);

	// Attach analysis string to HTML
	let analysisElement = document.getElementById("analysis");
	analysisElement.innerHTML = analysis;
}
