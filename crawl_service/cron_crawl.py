from crontab import CronTab

my_cron = CronTab(user='dactoankma')
job = my_cron.new(command='0 1 * * * python /home/dactoankma/sosanhviec/SOSANHVIEC/crawl_service/job/run.py')

my_cron.write()