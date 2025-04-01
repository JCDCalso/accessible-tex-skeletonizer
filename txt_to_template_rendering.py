from jinja2 import Environment, FileSystemLoader
import os

def txt_to_list_to_dict(filepath, prefix, num_format, suffix):
    def to_list(title_list_txt_file):
        with open(title_list_txt_file, 'r') as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines

    # first convert *slide_titles.txt back to a list
    titles = to_list(filepath) # a list of titles

    # Section takes name from slide
    content = {'sections':[]}
    for i, title in enumerate(titles, start=1):
        x = {'title': title, 'slideimg': f"{prefix}{format(i, num_format)}{suffix}"}
        content['sections'].append(x)

    return content

def jinja2_content_write(texTemplate, new_name, content_dict):
    # Load the Jinja2 template, with modularity for abs and relative paths
    fullpath = os.path.abspath(texTemplate)
    head_dir, texTemplate = os.path.split(fullpath)

    env = Environment(loader=FileSystemLoader(head_dir))
    template = env.get_template(texTemplate)

    # Render the template with the content
    rendered_tex = template.render(content_dict)

    # Write the rendered LaTeX to a file
    new_name+=".tex"
    with open(new_name, 'w') as f:
        f.write(rendered_tex)

    print(f"{texTemplate} rendered as {new_name}")

def main():
    import argparse
    """
        Mandatory args:
        .txt file of pptx conversion output
        template to use (texTemplate)
    """

    # Argument Parser
    my_desc = "Establishes skeleton for tex template."
    parser = argparse.ArgumentParser(description=my_desc)
    parser.add_argument("title_list_txt_file", type=str, help="path to .txt file")
    parser.add_argument("texTemplate", type=str, help=".tex template to fill out")

    # Optional args
    parser.add_argument("--output_name", type=str, default="New_Accompanying_Doc", help="Title of Outputted .tex")
    parser.add_argument("--lectureTitle", type=str, default="Lecture Slides", help="Title of Lecture")
    parser.add_argument("--profName", type=str, default="Professor Name", help="Name of Lecturer/Instructor/Lecturer")
    parser.add_argument("-p","--prefix", type=str, default="slide.", help="Prefix of image files. Default is \'slide.\'")
    parser.add_argument("-s","--suffix", type=str, default=".png", help="Suffix of image files. Default is \'.png\'")
    parser.add_argument('--num_format', type=str, default='03', help='Formatting argument for slide numbering.')
    args = parser.parse_args()

    # Main function: create content dictionary from .txt of titles, render into provided template

    # Begin with output of python-pptx, for now:
    # list of slide titles from input slide deck, turn into long dict
    # optional: will pass user defined prefix or suffix, or stick with default format: 'slide.xx.png'
    content_dict = txt_to_list_to_dict(args.title_list_txt_file, args.prefix, args.num_format, args.suffix)

    # hacky: add directly to list_to_dict
    content_dict['lectureTitle']=args.lectureTitle
    content_dict['profName']=args.profName

    jinja2_content_write(args.texTemplate,args.output_name, content_dict)


    # ## ## TEST
    # for entry in content_dict:
    #    print(content_dict[entry])

if __name__ == "__main__":
    main()
