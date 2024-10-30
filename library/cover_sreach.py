import os
import pathlib
import shutil

ROOT = pathlib.Path(__file__).parent

def cover_file(chart_path, cover_path):
    for chartname in os.listdir(chart_path):
        chart = chartname.split('_')[0]
        chart = chart.zfill(6)[2:6]
        chart = chart.zfill(6)

        for covername in os.listdir(cover_path):
            covername
            covername_temp = covername.replace("UI_Jacket_", "").replace(".png", "").zfill(6)
            if covername_temp == chart:
                target_directory = chart_path / chartname
                target_directory.mkdir(parents=True, exist_ok=True)

                source_file = cover_path / f"{covername}"
                target_file = target_directory / f"bg.png"
                shutil.copy2(source_file, target_file)
                print(f"Copied: {source_file} to {target_file}")

chart_path = ROOT.parent / "ChartData"
cover_path = ROOT.parent / "CoverData"

try:
    cover_file(chart_path, cover_path)
except FileNotFoundError as e:
    print(f"找不到 {e.filename}。请确认路径是否正确或存在。")

