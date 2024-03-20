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
    # assigns val the @font-face delcaration (second regex capture group)
    val = font_face_declaration[1]

    font_dict = {
        "font-family": re.findall('font-family: [\"\']([^\"\']+)', val),
        "font-style": re.findall('font-style: ([^;]+)', val),
        "font-weight": re.findall('font-weight: ([^;]+)', val),
        "font-stretch": re.findall('font-stretch: ([^;]+)', val),
        "font-display": re.findall('font-display: ([^;]+)', val),
        "src": re.findall('url\((.*?)\)', val),
        "unicode-range": re.findall('unicode-range: ([^;]*)', val),
    }

    # makes sure regex returned something before accesing it and assinging the first (and only) value
    for attribute in font_dict:
        if len(font_dict[attribute]) == 0:
            font_dict[attribute] = ""
        else:
            font_dict[attribute] = font_dict[attribute][0]

    # adds the unicode name after checking all regex extracted CSS properties exist
    font_dict["unicode-name"] = font_face_declaration[0]

    fonts.append(
        {
            "font-family": font_dict["font-family"],
            "font-style": font_dict["font-style"],
            "font-weight": font_dict["font-weight"],
            "font-stretch": font_dict["font-stretch"],
            "font-display": font_dict["font-display"],
            "src": font_dict["src"],
            "unicode-range": font_dict["unicode-range"],
            "unicode-name": font_dict["unicode-name"]
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
@use "sass:string";

$fonts: [{scss_fonts}];
"""

scss_file += """
@each $item in $fonts {
    /* #{map.get($item, "unicode-name")} */
    @font-face {
        @if string.length(map.get($item, "font-family")) > 0 {
            font-family: map.get($item, "font-family");
        }
        @if string.length(map.get($item, "font-style")) > 0 {
            font-style: map.get($item, "font-style");
        }
        @if string.length(map.get($item, "font-weight")) > 0 {
            font-weight: map.get($item, "font-weight");
        }
        @if string.length(map.get($item, "font-stretch")) > 0 {
            font-stretch: map.get($item, "font-stretch");
        }
        @if string.length(map.get($item, "font-display")) > 0 {
            font-display: map.get($item, "font-display");
        }
        @if string.length(map.get($item, "font-path")) > 0 {
            src: url("#{map.get($item, 'font-path')}") format(map.get($item, "font-format"));
        }
        @if string.length(map.get($item, "unicode-range")) > 0 {
            unicode-range: map.get($item, "unicode-range");
        }
    }
}
"""

# save SCSS file
scss_path = save_base + "_" + font_family_websafe + ".scss"
open(scss_path, "w").write(scss_file)
print("Saving generated SCSS file")

print("Successfully downloaded fonts to " + save_dir + "/ and saved SCSS as " + scss_path)
