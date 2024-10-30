import os
import subprocess
from pathlib import Path
import shutil

ROOT = Path(__file__).parent
key = "0x7F4551499DF55E68"

def dat_files(chart_path, dat_path):
    matched_files = []
    for chartname in os.listdir(chart_path):
        chart = chartname.split('_')[0]
        chart = chart.zfill(6)[2:6]
        chart = chart.zfill(6)

        for datname in os.listdir(dat_path):
            dat_file_path = dat_path / datname
            if dat_file_path.stat().st_size > 1 * 1024 * 1024:
                datname_temp = datname.replace(".dat", "").zfill(6)
                if datname_temp == chart:
                    print(f"找到匹配的文件: {datname} (大小: {dat_file_path.stat().st_size / (1024 * 1024):.2f} MB)")
                    matched_files.append((chart_path / chartname, dat_file_path))
                    
    return matched_files

def decrypt_dat_files(wannacri, dat_file, output_directory, decryption_key):
    output_path = output_directory / dat_file.stem
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        subprocess.run([
            str(wannacri), 'extractusm', '-p', str(dat_file), '-o', str(output_path), '--key', decryption_key
        ], check=True)
        print(f"Successfully decrypted {dat_file} to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error decrypting {dat_file}: {e}")
    return output_path

def convert_ivf_to_mp4(ffmpeg, temp_directory, chart_subdir):
    for root, _, files in os.walk(temp_directory):
        for filename in files:
            if filename.endswith('.ivf'):
                ivf_path = Path(root) / filename
                mp4_path = chart_subdir / "pv.mp4"
                try:
                    subprocess.run([
                        str(ffmpeg), '-i', str(ivf_path), '-c:v', 'h264_nvenc', str(mp4_path)
                    ], check=True)
                    print(f"Successfully converted {ivf_path} to {mp4_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error converting {ivf_path}: {e}")

def process_all_files(chart_path, dat_path, temp_path, wannacri, ffmpeg, decryption_key):
    matched_files = dat_files(chart_path, dat_path)
    if matched_files == []:
        print("未找到匹配的 DAT 文件或子目录。")
        return
    
    for chart_subdir, dat_file in matched_files:
        temp_output = decrypt_dat_files(wannacri, dat_file, temp_path, decryption_key)
        convert_ivf_to_mp4(ffmpeg, temp_output, chart_subdir)
        for file in temp_output.iterdir():
            if file.is_file():
                try:
                    file.unlink()
                except PermissionError:
                    print(f"无法删除文件: {file}，请确保该文件未被其他程序占用。")
        print(f"已清空 {temp_output} 文件夹")

chart_path = ROOT.parent / "ChartData"
dat_path = ROOT.parent / "MovieData"
temp_path = ROOT / "temp"
wannacri = ROOT / 'wannacri.exe'
ffmpeg = ROOT / 'ffmpeg.exe'

try:
    process_all_files(chart_path, dat_path, temp_path, wannacri, ffmpeg, key)
except FileNotFoundError as e:
    print(f"找不到 {e.filename}。请确认路径是否正确或存在。")