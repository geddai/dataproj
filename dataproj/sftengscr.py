import gdscr as gs
import pandas as pd

df = gs.get_jobs('software-engineer', 100, False, 10)
df.to_csv('se_jobs.csv', index=False)