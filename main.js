const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

axios.get('https://ca.finance.yahoo.com')
    .then(function (res){
        // console.log(Object.keys(res))
        // console.log('status:', res['status']);
        // console.log('config:', res['config']);
        // console.log('statusText:', res['statusText']);
        // console.log('request:', res['request']);
        // console.log('data:', res['data']);
        // const $ = await cheerio.load(html.data);
        fs.writeFile("logs.txt",res['data'], function(err){console.log(err);})
        // console.log(res);
    })