import os
import pathlib
import shutil
import subprocess
from pydub import AudioSegment

ROOT = pathlib.Path(__file__).parent
key = "0x7F4551499DF55E68"

def awb_files(chart_path, awb_path):
    matched_files = []
    for chartname in os.listdir(chart_path):
        chart = chartname.split('_')[0]
        chart = chart.zfill(6)[2:6]
        chart = chart.zfill(6)

        for awbname in os.listdir(awb_path):
            awbname_temp = awbname.replace("music", "").replace(".awb", "").zfill(6)
            if awbname_temp == chart:
                print(f"找到匹配的文件: {awbname}")
                matched_files.append((chart_path / chartname, awb_path / awbname))
    return matched_files

def decrypt_to_wav(input_file, temp_path, key):
    vgmstream_path = ROOT / "vgmstream" / "vgmstream-cli.exe"
    
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    
    output_wav = temp_path / (input_file.stem + ".wav")
    try:
        subprocess.run([
            str(vgmstream_path), 
            "-k", key,
            "-o", str(output_wav),
            str(input_file)
        ], check=True)
        print(f"{input_file} 解密并保存为 {output_wav}")
        return output_wav
    except subprocess.CalledProcessError as e:
        print("解密过程出错：", e)
        return None

def wav_to_mp3(output_wav, chart_subdir):
    try:
        output_mp3 = chart_subdir / ("track.mp3")
        os.makedirs(os.path.dirname(output_mp3), exist_ok=True)
        sound = AudioSegment.from_wav(output_wav)
        sound.export(output_mp3, format="mp3", parameters=["-ar", "44100"])
        print(f"{output_wav} 转换并保存为 {output_mp3}")
    except Exception as e:
        print("转换为 mp3 过程出错：", e)

def clean_temp_folder(temp_path):
    for temp_file in temp_path.iterdir():
        try:
            temp_file.unlink()
            print(f"已删除临时文件: {temp_file}")
        except Exception as e:
            print(f"删除文件 {temp_file} 时出错：", e)

chart_path = ROOT.parent / "ChartData"
awb_path = ROOT.parent / "SoundData"
temp_path = ROOT / "temp"

try:
    matched_files = awb_files(chart_path, awb_path)
    if matched_files:
        for chart_subdir, awb_file in matched_files:
            output_wav = decrypt_to_wav(awb_file, temp_path, key)
            if output_wav:
                wav_to_mp3(output_wav, chart_subdir)
            clean_temp_folder(temp_path)
    else:
        print("未找到匹配的 AWB 文件或子目录。")
except FileNotFoundError as e:
    print(f"找不到 {e.filename}。请确认路径是否正确或存在。")
