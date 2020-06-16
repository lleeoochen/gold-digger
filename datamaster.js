class DataMaster {

	constructor() {
		this.graphData = {};
	}

	loadData() {
		return fetch('source/DataGraph/graph_20182.csv').then(async res => {
			let text = await res.text();
			let lines = text.split('\n');

			for (let i in lines) {
				let line = lines[i];

				try {
					let commaIndex = line.indexOf(',');
					let dashIndex = line.lastIndexOf('-');
					let subject = line.substring(0, dashIndex);
					let courseID = line.substring(dashIndex + 1, commaIndex);
					let enrollData = (line.includes('nan')) ? [] : JSON.parse(line.substring(commaIndex + 1));

					if (this.graphData[subject] === undefined)
						this.graphData[subject] = {};
					this.graphData[subject][courseID] = enrollData;
				}
				catch (err) {
					console.log(err);
				}
			}
		});
	}

	//Get request for getting subjects
	getSubjects() {
		return Object.keys(this.graphData).sort();
	}

	//Get request for getting courses
	getCourses(subject) {
		return Object.keys(this.graphData[subject]).sort(this.course_comparator);
	}

	//Get request for getting graph data
	getGraph(subject, courseID) {
		return this.graphData[subject][courseID];
	}

	//Sort comparator
	course_comparator(a, b) {
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
}