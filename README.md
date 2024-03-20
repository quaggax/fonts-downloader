# Download Fonts from Google Fonts

This script downloads the otherwise inaccessible Web Font Formats from a provided Google Fonts stylesheet and generates a SCSS partial to easily import into a project.

This Script contacts external (web) servers. You are responsible for the servers that are contacted as a result of the use of this script.

## Usage

This script was developed and tested on macOS.
It requires the installation of `python` (at least 3.10) via Homebrew. This can be accomplished using the following command:

```
brew install python
```

Make sure to close and reopen your shell afterwards for all changes to take effect.

### Options

| Option      | Default Value | Notes                                                                                                     |
| ----------- | ------------- | --------------------------------------------------------------------------------------------------------- |
| input_url   | -             | escape using quotes                                                                                       |
| prefix_path | /assets/fonts | (optional) sets a path prefix in the generated SCSS file; don't use a trailing slash here                 |
| dir_path    | fonts/        | (optional) folder to save files to; a subfolder will be created with the fonts name; use a trailing slash |

Scheme: `python3.11 download-fonts.py input_url [prefix_path] [dir_path]`

Example:

```
python3.11 download-fonts.py "https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,400;0,600;1,400;1,600&display=swap"
```

---

## To-Do

- [ ] add option to generate CSS instead of SCSS
- [ ] add support for more stylesheets
