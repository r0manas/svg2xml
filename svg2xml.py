import xml.etree.ElementTree as ET
import re
import sys
import os

def convert_and_adjust_svg(svg_path, output_path, new_height, new_width, new_viewport_width, new_viewport_height):
    # Parse SVG file
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # --- Fix viewBox attribute ---
    view_box = root.attrib['viewBox']
    view_box = view_box.replace(',', ' ')  # Replace commas with spaces
    root.attrib['viewBox'] = view_box
    # --- End of fix ---

    # Create a new Android Vector Drawable root element
    vector = ET.Element('vector', xmlns="http://schemas.android.com/apk/res/android",
                        height=f"{new_height}dp", width=f"{new_width}dp",
                        viewportWidth=str(new_viewport_width), viewportHeight=str(new_viewport_height))

    # Extract and adjust path data
    for path in root.findall('.//{http://www.w3.org/2000/svg}path'):
        path_data = path.attrib['d']
        fill_color = path.attrib.get('fill', '#000000')

        # Use the corrected viewBox
        scaled_path_data = scale_path_data(path_data, new_viewport_width / float(root.attrib['viewBox'].split()[2]))

        path_element = ET.SubElement(vector, 'path', {
            'android:fillColor': fill_color,
            'android:pathData': scaled_path_data
        })

    tree = ET.ElementTree(vector)
    tree.write(output_path, xml_declaration=True, encoding='utf-8')
    print(f"Icon adjusted and saved as '{output_path}'")

def scale_path_data(path_data, factor):
    # ... (rest of the code remains the same)
