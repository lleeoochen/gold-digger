# GOLD-Digger
### Abstract
We will utilize data from the UCSB course catalog to determine which factors (i.e. time, location, subject, days of the week) affect student enrollment.

### Contributors:
Wei Tung Chen
Nicholas Duncan

### Agenda:
1) scrap data from UCSB course catalog x
2) parse scraped data form UCSB course catalog x
3) clean the data 1-2 weeks
  a) remove empty rows
  b) convert the strings into meaningful data
  c) parse filenames into quarters and years
4) build models 2 - 4 weeks
  a) we will use the 'pandas' python module to analyze the collected data
  b) TBD
5) analyze built models 1 - week
  a) create a graphical representation of the data
  b) TBD
6) PUBLISH IT! 1 - 2 weeks

### Conclusion (To be determined):

To run scrape/parser:

Run scraper first using python scraper.py then run parser using python3 parser.py
html files are found in the 'output' directory
csv file with data is found in the 'Data directory'


### To Run
- execution (normal): `python driver.py`
- execution (with single quarter flag): `singleQuarterFlag=True python driver.py`
- set up automatic scheduler every hour:
  1) open crontab editor: `crontab -e`
  2) copy and paste line: `0 * * * * export DISPLAY=:0 && cd /path/to/directory/GOLD-Digger && cronFlag=True singleQuarterFlag=True python driver.py`





# node-js-getting-started

A barebones Node.js app using [Express 4](http://expressjs.com/).

This application supports the [Getting Started with Node on Heroku](https://devcenter.heroku.com/articles/getting-started-with-nodejs) article - check it out.

## Running Locally

Make sure you have [Node.js](http://nodejs.org/) and the [Heroku CLI](https://cli.heroku.com/) installed.

```sh
$ git clone git@github.com:heroku/node-js-getting-started.git # or clone your own fork
$ cd node-js-getting-started
$ npm install
$ npm start
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```
$ heroku create
$ git push heroku master
$ heroku open
```
or

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Node.js on Heroku, see these Dev Center articles:

- [Getting Started with Node.js on Heroku](https://devcenter.heroku.com/articles/getting-started-with-nodejs)
- [Heroku Node.js Support](https://devcenter.heroku.com/articles/nodejs-support)
- [Node.js on Heroku](https://devcenter.heroku.com/categories/nodejs)
- [Best Practices for Node.js Development](https://devcenter.heroku.com/articles/node-best-practices)
- [Using WebSockets on Heroku with Node.js](https://devcenter.heroku.com/articles/node-websockets)
