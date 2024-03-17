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

# create an argument parser (add '--' before the name to make it optional)
parser = argparse.ArgumentParser(description='Download Fonts files from a CSS file')
parser.add_argument('input_url', metavar='input-url', type=str, help='the URL of the input CSS file')
parser.add_argument('--dir_path', metavar='dir-path', type=str, help='path of the destination directory for the font files')

# parse the command-line arguments
args = parser.parse_args()

# directory to save font files
save_dir = "fonts/"
if args.dir_path is not None:
    save_dir = args.dir_path

# make sure the directory exists
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# download the CSS file
css_file = requests.get(args.input_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'}).text

# extract all links to WOFF or WOFF2 file types from the stylesheet
font_links = re.findall('url\((.*?)\)', css_file)
print(font_links)

# download all font files
for link in font_links:
    # if ".woff2" in link or ".woff" in link:
        filename = link.split("/")[-1]
        save_path = os.path.join(save_dir, filename)
        font_file = requests.get(link, allow_redirects=True).content
        open(save_path, "wb").write(font_file)
