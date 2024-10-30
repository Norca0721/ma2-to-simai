import os
import xml.etree.ElementTree as ET
from pathlib import Path

def update_music_xml(music_directory):
    for root, _, files in os.walk(music_directory):
        for filename in files:
            if filename == 'Music.xml':
                xml_path = os.path.join(root, filename)
                try:
                    tree = ET.parse(xml_path)
                    root = tree.getroot()

                    for add_version in root.findall('.//AddVersion'):
                        id_element = add_version.find('id')
                        if id_element is not None and id_element.text >= '22':
                            id_element.text = '21'
                            print(f"Updated id in {xml_path}")

                    tree.write(xml_path, encoding='utf-8', xml_declaration=True)
                except Exception as e:
                    print(f"Error processing {xml_path}: {e}")

if __name__ == "__main__":
    music_directory = Path(__file__).parent.parent / "ChartData" / "music"
    update_music_xml(music_directory)
