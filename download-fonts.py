import os
try:
    import requests
except ImportError:
    import pip
    package = 'requests'
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
    print(package)
finally:
    import requests
import re
import argparse

WEIGHT_NAMES = {
	"thin": 100,
	"extra-light": 200,
	"light": 300,
	"regular": 400,
	"medium": 500,
	"semi-bold": 600,
	"bold": 700,
	"extra-bold": 800,
	"heavy": 900,
	"extra-black": 950,
}


# create an argument parser (add '--' before the name to make it optional)
parser = argparse.ArgumentParser(description='Download Fonts files from a CSS file')
parser.add_argument('input_url', metavar='input-url', type=str, help='the URL of the input CSS file')
parser.add_argument('--prefix_path', metavar='prefix-path', type=str, help='path prefix of the font files URL (in the SCSS/CSS)')
parser.add_argument('--dir_path', metavar='dir-path', type=str, help='path of the destination directory for the font files')

# parse the command-line arguments
args = parser.parse_args()

# URL prefix for font files
if args.prefix_path is None:
    prefix_path = "/assets/fonts"
else:
    prefix_path = args.prefix_path

# directory to save font files
if args.dir_path is None:
    save_base = "fonts/"
else:
    save_base = args.dir_path

# download the CSS file
css_file = requests.get(args.input_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'}).text

# capture all @font-face declaration blocks
# font_face_declarations = re.findall('@font-face\s*{.*?}', css_file, re.DOTALL)
font_face_declarations = re.findall('/\*\s*(?P<UNICODE_NAME>[^\s]+)\s*\*/(?P<CSS_LINES>[^}]*)', css_file, re.S)

# create array with font-face objects
fonts = []
for font_face_declaration in font_face_declarations:
    unicode_name = font_face_declaration[0]
    val = font_face_declaration[1]

    font_family = re.findall('font-family: [\"\']([^\"\']+)', val)[0]
    font_style = re.findall('font-style: ([^;]+)', val)[0]
    font_weight = re.findall('font-weight: ([^;]+)', val)[0]
    font_stretch = re.findall('font-stretch: ([^;]+)', val)[0]
    font_display = re.findall('font-display: ([^;]+)', val)[0]
    font_src = re.findall('url\((.*?)\)', val)[0]
    font_unicode_range = re.findall('unicode-range: ([^;]*)', val)[0]

    fonts.append(
        {
            "font-family": font_family,
            "font-style": font_style,
            "font-weight": font_weight,
            "font-stretch": font_stretch,
            "font-display": font_display,
            "src": font_src,
            "unicode-range": font_unicode_range,
            "unicode-name": unicode_name
        }
    )

# download fonts and generate SCSS
scss_fonts = ""
font_family_websafe = ""
save_dir = ""

for i, item in enumerate(fonts):
    css_file_format = ""

    font_family_websafe = item["font-family"].replace(" ", "-").lower()
    filetype = item["src"].split(".")[-1]
    match filetype:
        case "woff2":
            css_file_format = "woff2"
        case "woff":
            css_file_format = "woff"
        case "ttf":
            css_file_format = "truetype"
        case "otf":
            css_file_format = "opentype"
    filename = font_family_websafe + "-" + item["font-weight"] + "-" + item["font-style"] + "-" + item["unicode-name"] + "." + filetype

    # make sure the save directory exists
    save_dir = save_base + font_family_websafe
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # download and save font file
    save_path = os.path.join(save_dir, filename)
    font_file = requests.get(item["src"], allow_redirects=True).content
    open(save_path, "wb").write(font_file)
    print("Downloading " + filename)

    # add scss map to list of fonts
    scss_fonts += f"""(
        "font-family": "{item['font-family']}",
        "font-style": "{item['font-style']}",
        "font-weight": "{item['font-weight']}",
        "font-stretch": "{item['font-stretch']}",
        "font-display": "{item['font-display']}",
        "font-path": "{prefix_path + '/' + font_family_websafe + '/' + filename}",
        "font-format": "{css_file_format}",
        "unicode-range": "{item['unicode-range']}",
        "unicode-name": "{item['unicode-name']}"
    )"""

    # add scss list divider
    if i+1 < len(fonts):
        scss_fonts += ", "

# scss_fonts = re.sub(r"\n", "", scss_fonts) # remove newlines
# scss_fonts = re.sub(r'\s+', ' ', scss_fonts) # remove consecutive spaces

scss_file = f"""@use "sass:map";

$fonts: [{scss_fonts}];
"""

scss_file += """
@each $item in $fonts {
    /* #{map.get($item, "unicode-name")} */
    @font-face {
       	font-family: map.get($item, "font-family");
       	font-style: map.get($item, "font-style");
       	font-weight: map.get($item, "font-weight");
       	font-display: map.get($item, "font-display");
       	src: url("#{map.get($item, 'font-path')}") format(map.get($item, "font-format"));
       	unicode-range: map.get($item, "unicode-range");
    }
}
"""

# save SCSS file
scss_path = save_base + font_family_websafe + ".scss"
open(scss_path, "w").write(scss_file)
print("Saving generated SCSS file")

print("Successfully downloaded fonts to " + save_dir + "/ and saved SCSS as " + scss_path)
