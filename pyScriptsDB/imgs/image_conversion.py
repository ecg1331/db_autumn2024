import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image

def change_svg_fill(input_svg_path, output_svg_path, new_color):
    tree = ET.parse(input_svg_path)
    root = tree.getroot()
    
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    
    for path in root.findall('.//svg:path', namespaces):
        style = path.get('style')
        if style:
            if 'fill:' in style:
                path.set('style', style.replace(style.split(';')[0], f'fill:{new_color}'))
            else:
                path.set('style', style + f';fill:{new_color}')
        else:
            path.set('fill', new_color)
    
    tree.write(output_svg_path)

def svg_to_png(input_svg_path, output_png_path, dpi=300):
    cairosvg.svg2png(url=input_svg_path, write_to=output_png_path, dpi=dpi)

def open_png_and_display(png_path):
    img = Image.open(png_path)
    img.save(png_path, quality=95)  # Save the image again (useful for any post-processing)
    print(f"PNG image saved as {png_path}")
    img.show()

# Example Usage:
input_svg = 'icon1.svg'
output_svg = 'icon1_modified.svg'
new_color = '#FF5733'

# Change the fill color in the SVG
change_svg_fill(input_svg, output_svg, new_color)

# Convert the modified SVG to PNG
output_png = 'icon1.png'
svg_to_png(output_svg, output_png)

# Display the resulting PNG
open_png_and_display(output_png)
