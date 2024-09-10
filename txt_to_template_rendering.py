from jinja2 import Environment, FileSystemLoader
import os

def txt_to_list_to_dict(filepath):
    # first convert *slide_titles.txt back to a list
    import title_list_txt
    titles = title_list_txt.to_list(filepath) # a list of titles

    # Some slides unique, some repeat sequentially
    # Treat repeats as one section
    # Structure is list of dicts --> [{title of section 1, slides of section 1}{2...}]
    # slides key into another list of dicts --> [{title of slide 1}]
    # Section takes name from slide

    content = {'sections':[]}
    for i, title in enumerate(titles, start=1):
        x = {'title': title, 'slideimg': f"slide.{i:03}.png"}

        content['sections'].append(x)

    return content


def make_content_dict(lectureTitle, profName, List_of_Titles):

    content = {
        'title': 'My Beamer Presentation',
        'author': 'John Doe',
        'date': 'July 23, 2024',
        'sections': [
            {
                'title': 'Introduction',
                'slides': [
                    {'title': 'Welcome', 'content': 'Welcome to the presentation!'},
                    {'title': 'Overview', 'content': 'This presentation covers...'}
                ]
            },
            {
                'title': 'Main Content',
                'slides': [
                    {'title': 'Topic 1', 'content': 'Details about topic 1...'},
                    {'title': 'Topic 2', 'content': 'Details about topic 2...'}
                ]
            }
        ]
    }

    return 0

def jinja2_content_write(texTemplate, new_name, content_dict):
    # Load the Jinja2 template
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
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
        Required args:
        .txt file of pptx conversion output
        Title of Lecture (lectureTitle)
        Lecturer name (profName)
        template to use (texTemplate)
    """

    # Argument Parser

    my_desc = "Establishes skeleton for tex template."
    parser = argparse.ArgumentParser(description=my_desc)
    parser.add_argument("title_list_txt_file", type=str, help="path to .txt file")
    parser.add_argument("texTemplate", type=str, help=".tex template to fill out")

    # Optional args
    parser.add_argument("--output_name", type=str, default="New_Presentation", help="Title of Outputted Beamer/Latex Presentation")
    parser.add_argument("--lectureTitle", type=str, default="Lecture Slides", help="Title of Lecture")
    parser.add_argument("--profName", type=str, default="Professor Name", help="Name of Lecturer/Instructor/Lecturer")
    args = parser.parse_args()

    # Continue with main function and call other functions

    # Begin with output of python-pptx, for now:
    # list of slide titles from input slide deck, turn into long dict
    content_dict = txt_to_list_to_dict(args.title_list_txt_file)

    # try 1 content_dict = {'section':content_list}
    # TODO: create content dict

    # hacky: add directly to list_to_dict
    content_dict['lectureTitle']=args.lectureTitle
    content_dict['profName']=args.profName

    #TODO: render and write template using content dict
    jinja2_content_write(args.texTemplate,args.output_name, content_dict)


    # ## ## TEST
    for entry in content_dict:
        print(content_dict[entry])




if __name__ == "__main__":
    main()
