import os
os.system('mkdir Output')
os.system('python scraper.py')
os.system('python3 parser.py')
os.system('python email_notify.py')
os.system('rm Output/*.html')
