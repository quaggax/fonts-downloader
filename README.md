# Download Fonts from any Stylesheet

explaination of the script

This Script contacts external (web) servers. You are responsible for the servers that are contacted as a result of the use of this script.

## Usage

This script was developed and tested on macOS.
It requires the installation of `python` (at least 3.10) via Homebrew. This can be accomplished using the following command:

```
brew install python
```

Make sure to close and reopen your shell afterwards for all changes to take effect.

Only Google Fonts is supported at the moment.

Example:

```
python3.11 download-fonts.py "https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,400;0,600;1,400;1,600&display=swap"
```

---

## To-Do

- [ ] add option to generate CSS instead of SCSS
- [ ] add support for more stylesheets
