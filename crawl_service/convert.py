import pandas as pd
import os


#df = pd.read_csv(os.path.join(os.getcwd(), "topdev.csv"))
df = pd.read_csv("/home/dactoankma/sosanhviec/SOSANHVIEC/crawl_service/job/job.csv")
new_df = (df.set_index(['ADDRESS', 'SALARY', 'COMPANY', 'TITLE', 'LINK', 'DEGREE', 'EXP', 'TYPE'])
          .stack()
          .str.split(',', expand=True)
          .stack()
          .unstack(-2)
          .reset_index(-1, drop=True)
          .reset_index()
          )
new_df.to_csv('job_new.csv')
#new_df.to_csv('topdev.csv')
