import os
import pathlib
import subprocess
import time

ROOT = pathlib.Path(__file__).parent

awb_sreach  = ROOT / 'library' / 'awb_sreach.py'
cover_sreach = ROOT / 'library' / 'cover_sreach.py'
dat_sreach = ROOT / 'library' / 'dat_sreach.py'

print("开始添加封面")
time.sleep(0.5)
subprocess.run(['python', str(cover_sreach)], check=True)
print("封面添加完成")

print("开始添加音频")
time.sleep(0.5)
subprocess.run(['python', str(awb_sreach)], check=True)
print("音频添加完成")

print("开始添加视频")
time.sleep(0.5)
subprocess.run(['python', str(dat_sreach)], check=True)
print("视频添加完成")

os.system('pause')