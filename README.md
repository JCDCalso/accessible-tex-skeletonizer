# accessible-tex-skeletonizer: Workflow for Establishing Skeleton Accompanying Document from Presentation File

## General Overview:

This command line workflow allows a user to quickly set up the skeleton for the ["Accompanying Accessibility Document"](https://github.com/JCDCalso/accessible-tex-skeletonizer/wiki/About-the-%22Accompanying-Doc%22) `.tex` file, going from the original `.pptx` or `.key` presentation slide deck. 

## How to go from a Slide Deck to a Latex Skeleton:
The workflow is divided into the following steps:
1. Export your slide deck as a directory of individual images.
2. Create the text file of your list of titles. 
3. Prepare the .tex template. 
4. Render the template and output the skeleton document. 

### Step 1: From Slide Deck to Images

#### Powerpoint
* With your `.pptx` file open, go to `File > Export` which opens a dialogue box.
* Select your directory, change the `File Format` option to `PNG`, which is the best for LaTeX
* Be sure the option for `Save Every Slide` is selected. 
  * This option will save every image as its own `.png`, with the name and numbering scheme `Slide1.png`, `Slide2.png`, ..., etc. 
  * These slides will be placed in a folder with the name you provide in the `Export As` field.
* Click `Export` and after a short while all your slides will be saved as individually named and numbered PNG files.

#### Keynote
If working with keynote, it may be easier to simply convert the `.key` file into a `.pptx` file to facilitate the other steps of this workflow (namely step 2, requiring `python-pptx`. However, some elements may not translate well. In which case, it may be useful to export the slide deck into individual images.
* With your `.key` file open, go to `File > Export To... > Images`, which opens a dialogue box.
* Select `All` for `Slides`, `PNG` for `Format`
* Once you select `Save` and set your directory, your slide deck will be saved as individual images in a folder with the name and numbering scheme `presentation name.001.png`, `presentation name.002.png`, ..., etc

### Step 2: Setting up the slide titles text file
In this step, create a `.txt` file with the title of each slide on its own line.

Ultimately, this `.txt` file will be used to create a Python dictionary which will allow it to autofill a template that helps us set up our document. 

To make this step easier, we can use a different Python helper script, [pptx_elements_to_list.py](#pptx_elements_to_listpy) that will pull the titles from a `.pptx` slide. 

Some notes on this `titles.txt` file:
- Ensure you have exactly the same number of lines for each slide of your original file.
- Some slides in your original slide title may have not had a title. For the LaTeX Accessibility Doc, it's best if each slide is given a name.
- Repeated slide titles are okay, but it may be useful to have a numbering system (i.e. "Slide Title (1)," "Slide Title (2)," "Slide Title (3)," etc.)

### Step 3: Prepare the specially formatted .tex template
Details in [section on accompanying_doc_jinja_template.tex](#accompanying_doc_jinja_templatetex).

### Step 4: Render the jinja template
Details in [section on txt_to_template_rendering.py](#txt_to_template_renderingpy).

### Step 5: Before you compile your LaTeX document
In this version of the workflow, you have to set the graphics path to the directory containing your slide images **after** rendering the jinja template. 

In the preamble (the section before `\begin{document}`): 
```
\graphicspath{path to your folder/directory containing the slide images you made in step 1}
```

## Contents and Description

### pptx_elements_to_list.py

#### Description
Takes a .pptx file, extracts all titles for each slide (if they exist as elements within standard PowerPoint templates), and saves those to a .txt file. 

#### Requirements:
* Python
* `argparse` and `os` (normally included in Python versions >= 2.7)
* `python-pptx` easily installed with pip, [installation and documentation here](https://python-pptx.readthedocs.io/en/latest/user/install.html#install)

#### Use:
In command line:

`python pptx_elements_to_list.py path/to/file.pptx`

Will save a `.txt` file in the same directory, with the name `file-slide_titles.txt`. You can change the name of the output file with:

`python pptx_elements_to_list.py path/to/file.pptx -o my_filename` or `python pptx_elements_to_list.py path/to/file.pptx --output_filename my_filename`

As of now, the text file will only contain the titles of each slide on a new line. It is adviseable to check the text file to ensure:
1. The titles are indeed present as expected.
  * If the slide deck was generated without using default master slide templates, and titles were manually added as basic text boxes/shapes, `python-pptx` will not recognize arbitrary text boxes as titles.
2. The number of lines equals the number of slides in the original .pptx file.

#### Notes

* For slides without titles, an empty line will be printed. It is adviseable to add your own title for this slide.

* Does not seem to work with ppt, so if you have a ppt, it's pretty easy to upconvert to .pptx in PowerPoint "Save As"

### accompanying_doc_jinja_template.tex

#### Description
This is a specially formatted `.tex` file that serves as a template for the rendering Python script. Apart from a few specially formatted lines to work with `Jinja,` the file is like any other `.tex` file you would create; you can modify this template before or after rendering as you see fit. For example, you may want each section to have a subsection after the image, or a horizontal rule after the image. You can set both of these in the template before rendering to save the work of applying that to every section in your final accompanying document.

In its current configuration, the template will create a new page and a new section named for each title of your text file of title slides. It will place the `PNG` of each slide at the top of each page, with a caption and alt text that read "screenshot of slide [title of slide]." You can change this caption and alt text as you see fit, but it is adviseable to keep them the same as each other. The screenshot of the slide will have a box drawn around it, you can modify the appearance of this box with the `fbox` settings in the preamble.

#### Notes:

* Of note, you will have to set the graphics path (to the folder containing all images of your slide deck) in the preamble of the LaTeX doc **after** it renders.

* There are some quirks with how the rendering is done that mean you should look out for certain symbol combinations. Nested braces `{{}}` is one, which jinja interprets as its own command for a dictionary. This explains the previous point. Another to watch out for is `{#` which is the default comment for jinja and will trigger an [end of comment error](https://stackoverflow.com/questions/72762152/jinja2-exceptions-templatesyntaxerror-missing-end-of-comment-tag)

### txt_to_template_rendering.py

#### Description
This is the final Python script you will call to render the `.tex` template described above.

#### Requirements
* Python (>=3.6)
* `argparse` and `os` (normally included in Python versions >= 2.7)
* `jinja2` easily installed with pip, [installation instructions and documentation](https://pypi.org/project/Jinja2/)

#### Use

`python txt_to_template_rendering.py [slide title list text file] [template tex file]`

This will output `New_Accompanying_Doc.tex` in the same directory, which will be rendered as described in the `accompanying_doc_jinja_template.tex` section above.

##### Optional Arguments:

* `--output_name` changes the name of the final `.tex` file
* Image naming format:
  * Default is `slide.###.png` padded with leading `0` for numbering
  * Can set prefix and suffixes with `-p=`/`--prefix=` and `-s=`/`--suffix=`
    * Custom suffixes will allow you to use different image formats as long as they are compatible with LaTeX (i.e. the slides were saved as `.pdf` and not `.png`)
  * Set number of leading zeros or no leading zeros (default is three digits with leading zeros `001`,`002`,`003`, etc):
    * `--num_format="d"` as a standard integer (`1`,`2`, etc)
    * `--num_format="02"` for two digits with leading zeros (`01`,`02`,`03`, etc)
