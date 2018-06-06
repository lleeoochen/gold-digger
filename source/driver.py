import os

# Crontab
# 0 12 * * * . $HOME/.bashrc && export DISPLAY=:0 && cd ~/Desktop/Projects/Current/GOLD-Digger/source/ && python driver.py

# Setup output files
os.system('mkdir Output')
os.system('touch log.txt')

# Execute scripts
os.environ['cronFlag'] = 'True'
os.environ['singleQuarterFlag'] = 'True'
os.system('python scraper.py >> log.txt')
os.system('python3 parser.py >> log.txt')

# Wrap up and send log to emails.
os.system('git add .')
os.system('git status >> log.txt')
os.system('python email_notify.py')

# Cleanup output files
os.system('rm -r Output/')
os.system('rm log.txt')
