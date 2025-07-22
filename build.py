from pybtex.database.input import bibtex
import json

def get_personal_data():
    name = ["Ali", "Rahimi-Kalahroudi"]
    email = "alirahimikalahroudi@gmail.com"
    twitter = "alirkay"
    google_scholar="U7FujF8AAAAJ"
    github = "alirahkay"
    linkedin = "ali-rahimi-kalahroudi"
    bio_text = f"""
                <p>My name is Ali Rahimi Kalahroudi (Written as "_علی رحیمی‌کلهرودی_" in my native language—Persian). <br>I am currently an AI Research Scientist at DRW. My ultimate research goal is to develop AI agents capable of solving diverse tasks given minimal supervision. <br><br>I am currently interested in designing reliable machine learning (ML) algorithms for sequential decision-making in open-ended interaction settings. In these contexts, the algorithms must learn and continually adapt their skills and knowledge. To tackle these challenges, my approach centers on leveraging model-based learning mechanisms. This involves empowering AI agents with the capability to construct and utilize world models and employing planning to enhance their decision-making processes.</p>
                <p>
                    <span style="font-weight: bold;">Bio:</span> 
                    Perviously I received my M.Sc. in computer science at the University of Montreal and Mila under the supervision of Prof. Sarath Chandar.
                </p>
                <p>
                    <span style="font-weight: bold;">Hobbies:</span>
                    While I am not doing science, I enjoy reading books, watching movies, playing football and volleyball, and hiking.
                </p>
                <p>
                    <a href="http://alirahkay.github.io/assets/pdf/cv-alirahimikalahroudi.pdf" target="_blank" style="margin-right: 15px"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <a href="mailto:{email}" style="margin-right: 15px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="https://twitter.com/{twitter}" target="_blank" style="margin-right: 15px"><i class="fab fa-twitter fa-lg"></i> Twitter</a>
                    <a href="https://scholar.google.com/citations?user={google_scholar}&hl=en" target="_blank" style="margin-right: 15px"><i class="fa-solid fa-book"></i> Scholar</a>
                    <a href="https://github.com/{github}" target="_blank" style="margin-right: 15px"><i class="fab fa-github fa-lg"></i> Github</a>
                    <a href="https://www.linkedin.com/in/{linkedin}" target="_blank" style="margin-right: 15px"><i class="fab fa-linkedin fa-lg"></i> LinkedIn</a>
                </p>
    """
    footer = """
    
            <div class="col-sm-12" style="font-size: 80%;">
                <pr>Website template adopted from <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank"> Michael Niemeyer</a>.</pr>
            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    return {
        'Sarath Chandar': 'http://www.sarathchandar.in',
        'Janarthanan Rajendran': 'https://sites.google.com/umich.edu/janarthanan-rajendran/',
        'Harm Van Seijen': 'https://scholar.google.ca/citations?user=0UTNLh8AAAAJ&hl=en',
        'Ida Momennejad': 'https://www.momen-nejad.org',
        'Yi Wan': 'https://sites.google.com/ualberta.ca/yiwan/',
        'Doina Precup': 'https://www.cs.mcgill.ca/~dprecup/',
        'Reza Bayat': 'https://rezabyt.github.io',
        'Mohammad Pezeshki': 'https://mpezeshki.github.io',
        'Pascal Vincent': 'https://mila.quebec/en/directory/pascal-vincent',
        }

def generate_person_html(persons, equal_contribs, connection=", ", make_bold=True, make_bold_name='Ali Rahimi-Kalahroudi', add_links=True):
    links = get_author_dict() if add_links else {}
    s = ""
    for p in persons:
        add_star = False
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if string_part_i in equal_contribs:
            add_star = True
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{make_bold_name}</span>'
        if add_star:
            string_part_i += "*"
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    if 'award' in entry.fields.keys():
        s += f"""{entry.fields['title']} <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""{entry.fields['title']} <br>"""

    s += f"""{generate_person_html(entry.persons['author'], entry.fields['equal_contrib'])} <br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    if entry.fields.get('also_at', None):
        s += f"""<span style="font-size: 80%">Also at:</span> <span style="font-style: italic; font-size: 80%">{entry.fields['also_at']}</span><br>"""

    artefacts = {'html': 'Project Page', 'pdf': 'Paper', 'supp': 'Supplemental', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')

    cite = "<pre><code>@InProceedings{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], [], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    s += " /" + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': 'Slides', 'video': 'Recording'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s

def get_news_entry(entry_key, entry, max_news_shown):
    s = f"""<div class="news-item"><table><tr><td>{entry["date"]} &#8194;</td><td>{entry["body"]}<hr class="fun-line"></td></tr></table></div>"""
    if entry_key != max_news_shown:
        return s
    else:
        return """<div class="hidden-news" style="display: none;">\n""" + s 


def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_paper_entry(k, bib_data.entries[k])
    return s

def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('talk_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_talk_entry(k, bib_data.entries[k])
    return s


def get_news_html(max_news_shown=3):
    with open("news_list.json", "r") as file:
        news_list = json.load(file)
    s = ""
    for i in range(len(news_list)):
        s += get_news_entry(i, news_list[i], max_news_shown)
    if len(news_list) > max_news_shown:
        s += """</div>\n"""
    s += """<button class="show-more-button" onclick="showMoreNews()">Show More</button>"""
    return s

def get_index_html():
    pub = get_publications_html()
    talks = get_talks_html()
    news = get_news_html()
    name, bio_text, footer = get_personal_data()

    news_button_style = """
<style>
    /* Button Styles */
    .show-more-button {
        background-color:  #3498db; /* Background color */
        color: #fff; /* Text color */
        border: none;
        padding: 15px 25px; /* Padding */
        font-size: 15px; /* Font size */
        border-radius: 50px; /* Rounded shape */
        cursor: pointer; /* Cursor on hover */
        transition: background-color 0.3s ease, transform 0.2s ease; /* Smooth transitions */
        outline: none; /* Remove default focus outline */
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1); /* Box shadow for a lifted effect */
    }

    /* Button Hover Effect */
    .show-more-button:hover {
        background-color: #3498db; /* Darker background color on hover */
        transform: scale(1.05); /* Slight scale-up on hover */
    }

    .fun-line {
        border: none;
        height: 2px; /* Adjust the height as needed */
        background-color: #AEC6CF; /* Change the color as needed */
    }
</style>
"""
    news_button_script = """
    <script>
            function showMoreNews() {
            var hiddenNews = document.querySelector('.hidden-news');
            var showMoreButton = document.querySelector('.show-more-button');

            if (hiddenNews.style.display === 'none' || hiddenNews.style.display === '') {
                hiddenNews.style.display = 'block';
                showMoreButton.textContent = 'Show Less';
            } else {
                hiddenNews.style.display = 'none';
                showMoreButton.textContent = 'Show More';
            }
        }
    </script>
"""

    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <title>{name[0] + ' ' + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
</head>

{news_button_style}

<body>
    <div class="container">
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="margin-bottom: 1em;">
            <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
            </div>
            <br>
            <div class="col-md-8" style="">
                {bio_text}
            </div>
            <div class="col-md-4" style="">
                <img src="assets/img/profile.jpg" class="img-thumbnail" width="280px" alt="Profile picture">
            </div>
        </div>
        <div class="row" style="margin-top: 1em;">
            <div class="col-sm-12">
                <h4>News</h4>
                {news}
            </div>
        </div>
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Publications</h4>
                <span style="margin-left: 4em; font-style: italic; font-size: 80%; color: #888">* denotes equal contribution.</span><br><br>
                {pub}
            </div>
        </div>
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Talks</h4>
                {talks}
            </div>
        </div>

        <div class="footnotes">
            <hr>
            {footer}
        </div>

    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
    {news_button_script}
</body>

</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')




    # <a href="https://www.e-fellows.net/" target="_blank">the e-fellows scholarship</a> 