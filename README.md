# GOLD-Digger
### Abstract
We will utilize data from the UCSB course catalog to determine which factors (i.e. time, location, subject, days of the week) affect student enrollment.

### Contributors:
Wei Tung Chen
Nicholas Duncan

### Agenda:
1) scrap data from UCSB course catalog x
2) parse scraped data form UCSB course catalog x
3) clean the data 1-2 weeks x
  a) remove empty rows
  b) convert the strings into meaningful data
  c) parse filenames into quarters and years
**4) build models 2 - 4 weeks
  a) we will use the 'pandas' python module to analyze the collected data
  b) TBD**
5) analyze built models 1 - week
  a) create a graphical representation of the data
  b) TBD
6) PUBLISH IT! 1 - 2 weeks

### Scraper and Parser Script Usage
- execution (normal): `python driver.py`
- execution (with single quarter flag): `singleQuarterFlag=True python driver.py`
- set up automatic scheduler every hour:
  1) open crontab editor: `crontab -e`
  2) copy and paste line: `0 * * * * export DISPLAY=:0 && cd /path/to/directory/GOLD-Digger && cronFlag=True singleQuarterFlag=True python driver.py`

### Heroku Server Instructions
- Install libraries: `npm install`
- Execution (local): `npm start` (and open http://localhost:5000/).
- Execution (heroku): `heroku open` (or open https://ucsb-gold-digger.herokuapp.com/).
