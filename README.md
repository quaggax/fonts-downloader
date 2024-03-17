# Download Fonts from any Stylesheet
explaination of the script

This Script contacts external (web) servers. You are responsible for the servers that are contacted as a result of the use of this script.

## Usage
This script was developed and tested on macOS.
It requires the installation of `python` via Homebrew. This can be accomplished using the following command:

```brew install python```

Make sure to close and reopen your shell afterwards for all changes to take effect.


```
python3 download-fonts.py "https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,400;0,600;1,400;1,600&display=swap"
```

## To Do
- [ ] Capture entire `@font-face` CSS block (to be able to extract CSS properties)
- [ ] Extract `font-family` name to create sub-folder and rename files
- [ ] Extract other CSS properties and rename files accordingly
    - [ ] `font-style` - Use this value inside the file name.
    - [ ] `font-weight` - Check if the weight value has an assigned name and use it for the file name. If the value doesn't have an assigned name use the number value as a name.
    - [ ] `font-stretch`
    - [ ] `font-display`
    - [ ] `unicode-range` - Check if the ranges match against the predetermined Google Fonts ranges and assign range-name accordingly. If the ranges don't match, assign an index as a name and save the ranges for SCSS and CSS generation.
---
- [ ] Generate SCSS (with all extracted CSS properties)
- [ ] Generate CSS (with all extracted CSS properties)




### Notes
Parts of this code were generated with the help of Generative AI.
