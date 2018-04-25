var express = require('express');
var path = require('path');
var app = express();
var PORT = process.env.PORT || 5000;

var count = 0;

//Host static website from public/
app.use(express.static(path.join(__dirname, 'public')));

//Get request for getting graph data
app.get('/getGraph', function (req, res) {
	res.send("Here is your graph from server! " + (count++) + " times!");
});

//Start server at PORT
var server = app.listen(PORT, function () {
   var host = server.address().address;
   var port = server.address().port;
   console.log(`Listening on ${ port }.`);
});
