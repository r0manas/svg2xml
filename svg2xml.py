import xml.etree.ElementTree as ET
import re
import sys
import os

def convert_and_adjust_svg(svg_path, output_path, new_height, new_width, new_viewport_width, new_viewport_height):
    # Parse SVG file
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Create a new Android Vector Drawable root element
    vector = ET.Element('vector', xmlns="http://schemas.android.com/apk/res/android",
                        height=f"{new_height}dp", width=f"{new_width}dp",
                        viewportWidth=str(new_viewport_width), viewportHeight=str(new_viewport_height))

    # Extract and adjust path data
    for path in root.findall('.//{http://www.w3.org/2000/svg}path'):
        path_data = path.attrib['d']
        fill_color = path.attrib.get('fill', '#000000')
        
        scaled_path_data = scale_path_data(path_data, new_viewport_width / float(root.attrib['viewBox'].split()[2]))
        
        path_element = ET.SubElement(vector, 'path', {
            'android:fillColor': fill_color,
            'android:pathData': scaled_path_data
        })
    
    tree = ET.ElementTree(vector)
    tree.write(output_path, xml_declaration=True, encoding='utf-8')
    print(f"Icon adjusted and saved as '{output_path}'")

def scale_path_data(path_data, factor):
    def scale_coordinate(match):
        value = float(match.group())
        return str(value * factor)
    
    # Scale all numbers in the pathData
    scaled_data = re.sub(r'-?\d+(\.\d+)?', scale_coordinate, path_data)
    return scaled_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python svg2xml.py <input_svg_path>")
        sys.exit(1)

    svg_path = sys.argv[1]
    base_name = os.path.splitext(svg_path)[0]
    output_path = f"{base_name}.xml"
    new_height = 108
    new_width = 108
    new_viewport_width = 1024.0
    new_viewport_height = 1024.0
    
    convert_and_adjust_svg(svg_path, output_path, new_height, new_width, new_viewport_width, new_viewport_height)
