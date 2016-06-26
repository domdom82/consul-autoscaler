'use strict';

var express = require('express');
var bodyParser = require('body-parser');
var request = require('request');
var logger = require('winston');
var path = require('path');

var vagrantFile = process.env.VAGRANTFILE || '../vagrant/Vagrantfile';
var vagrantDir = null;
var app = express();
app.use(bodyParser.json());

app.get("/vms", function (req, res) {
    var method = 'GET /vms';
    logger.info(method, 'Listing VMs in dir new VM using', req.body);

    res.send({msg: 'pong'});
});

app.post('/vms', function(req, res) {
    var method = 'POST /vms';
    logger.info(method, 'Creating new VM using', req.body);

    var newTrigger = req.body;

    res.status(200).json({ok: 'new VM created successfully'});
});

app.delete('/vms/:name', function(req, res) {
    var method = 'DELETE /vms/:name';
 
    if(true) {
        res.status(200).json({ok: 'VM ' + req.params.name + ' successfully deleted'});
    }
    else {
        res.status(404).json({error: 'VM ' + req.params.name + ' not found'});
    }
});


app.listen(8080, function () {
    var method = 'init';
    logger.info(method, 'listening on port 8080');

    vagrantDir = path.dirname(vagrantFile);
    logger.info(method, 'using Vagrantfile in dir ', vagrantDir);
});
