import json

from bs4 import BeautifulSoup


def start_html():
    # Generate the starting part of HTML
    start_html = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <title>Civic Media Scout</title>
        <meta name="description" content="Civic Media Scout is an initiative dedicated to compile and curate public contact information from government websites. Our aim is to gather and present publicly accessible data, including comprehensive social media profiles and essential contact details, in an accessible and user-friendly manner.">
        <style>
            html,
            body {
            height: 100%;
            width: 100%;
            margin: 0;
            display: table;
            font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif;
            font-size: 14px;
            background-color: whitesmoke;
            }
            p {
            margin: 5px 15px
            }
            table {
            border-spacing: 0;
            border-collapse: collapse;
            empty-cells: hide;
            width: 95%;
            margin: 0 auto;
            table-layout: auto
            }
            th {
            top: 0;
            position: sticky;
            padding: 2px;
            box-sizing: border-box;
            color: rgb(255, 255, 255) !important;
            font-size: 13px;
            height: 30px;
            background-color: rgb(20, 90, 141) !important;
            border: 0em solid rgb(204, 204, 204);
            z-index: 1
            }
            td {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100px;
            height: auto;
            max-height: 100px;
            padding: 2px;
            text-align: center;
            font-size: 14px;
            border: .05em solid rgb(204, 204, 204)
            }
            table td:nth-child(1) {
            max-width: 200px;
            text-align: left;
            padding: 0 5px
            }
            table td:nth-child(2) {
            max-width: 150px;
            text-align: left;
            padding: 0 5px
            }
            table td:nth-child(3),table td:nth-child(4),table td:nth-child(5),table td:nth-child(6),table td:nth-child(7),table td:nth-child(8),table td:nth-child(9) {
            max-width: 120px;
            text-align: left;
            padding-left: 5px;
            padding-top: 5px;
            }
            tr {
            border-bottom: 1px solid #ddd;
            padding: 5px;
            background: #fff0;
            background-image: linear-gradient(to right, #ffffff00, #ffffff00, #ffffff00, #ffffff00)
            }
            tr:hover {
            background: #fff0;
            background-image: linear-gradient(to right, #5ed0ff54, #55f5a84d, #37f99c54, #21b46d57);
            box-shadow: 0 2px 3px 0 rgb(4 128 123 / 45%);
            background-blend-mode: screen
            }
            .hoverable {
            position: relative;
            text-align: center
            }
            .hoverable>.hoverable__tooltip {
            display: none;
            padding: 5px 5px;
            margin: 5px
            }
            .hoverable>.hoverable__main {
            position: absolute;
            white-space: pre-line;
            color: black;
            }
            .hoverable:hover>.hoverable__tooltip {
            display: inline;
            position: absolute;
            top: 1.9em;
            left: 2em;
            right: 2em;
            background-color: #98fadb;
            border: 0;
            z-index: 99;
            text-align: left
            }
            h1 {
            text-align: center;
            font-size: 18px;
            color: #2980b9;
            margin: 5px 0 5px 0;
            position: relative;
            display: inline-block;
            }
            sup {
            text-align: center;
            font-size: 12px;
            color: black;
            margin: 5px 0 5px 0;
            position: relative;
            display: inline-block;
            }
            sup:hover {
            -o-transition: .2s;
            -ms-transition: .2s;
            -moz-transition: .2s;
            -webkit-transition: .2s;
            transition: .2s;
            text-shadow: 1px 1px 2px #888888;
            }
            .table-container {
            overflow-x: auto;
            overflow-y: scroll;
            height: 87vh
            }
            a {
            text-decoration: none;
            }
            a:hover{
            -o-transition:.2s;
            -ms-transition:.2s;
            -moz-transition:.2s;
            -webkit-transition:.2s;
            transition: .1s;
            text-shadow: 0px 0px 1px #888;
            text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="hoverable">
            <h1>Civic Media Scout
                <span class="hoverable__main"><sup>&epar;</sup></span>
            </h1>
            <span class="hoverable__tooltip">
                <p><em>Civic Media Scout</em> is an initiative dedicated to compile and curate <em>public</em> contact information from government websites. Our aim is to gather and present publicly accessible data, including comprehensive social media profiles and essential contact details, in an accessible and user-friendly manner.</p>
                <p>By leveraging existing open source code and technologies, this project empowers citizens, researchers, and policymakers with a <em>centralized</em> resource for contacting a government entity. Join us in the journey to enhance civic engagement and information accessibility.</p>
            </span>
        </div>
        <div class="table-container">
        <table cellpadding="1" cellspacing="1" id="content-table">
        <thead>
            <tr>
                <th scope="col">Page Title</th>
                <th scope="col">Source URL</th>
                <th scope="col">Twitter</th>
                <th scope="col">Facebook</th>
                <th scope="col">Instagram</th>
                <th scope="col">Youtube</th>
                <th scope="col">Phone</th>
                <th scope="col">Email</th>
            </tr>
        </thead>
        <tbody>
    """
    return start_html


def add_table_rows(data_rows):
    table_rows = ""
    # Create a row using values from the data dictionary
    for data in data_rows:
        # Limit the text length and add the title attribute
        page_title = data.get("Page Title", "None")
        source_url = data.get("Source URL", "None")
        short_url = (
            data.get("Source URL", "None")
            .replace("https:", "")
            .replace("http:", "")
            .replace("www.", "")
            .strip("/")
        )

        table_rows += f"""
            <tr>
                <td title="{page_title}">{page_title}</td>
                <td><a href="{source_url}" title="{source_url}" target="_blank">{short_url}</a></td>
                <td>{generate_social_links(data, "Twitter", page_title)}</td>
                <td>{generate_social_links(data, "Facebook", page_title)}</td>
                <td>{generate_social_links(data, "Instagram", page_title)}</td>
                <td>{generate_social_links(data, "YouTube", page_title)}</td>
                <td>{generate_contact_links(data, phone=True)}</td>
                <td>{generate_contact_links(data, phone=False)}</td>
            </tr>
        """
    return table_rows


def generate_contact_links(data, phone=True):
    contact_list = []
    uri = ""
    if phone:
        uri = "tel:"
        contact_list = data.get("Phone", [])
    else:
        uri = "mailto:"
        contact_list = data.get("Email", [])

    if contact_list:
        rows = ""
        contact_count = len(contact_list)
        for contact in contact_list[:3]:
            rows += f'<a title="{contact}" href="{uri}{contact}">{contact}</a><br>'
        if contact_count > 3:
            remaining = contact_count - 3
            rows += f"and {remaining} more...<br>"
        return rows
    else:
        return "&nbsp;"


def generate_social_links(data, platform, page_title):
    if link := data.get(platform):
        profile_id = get_profile_id(link)
        print(profile_id)
        return (
            f"""<a href="{link}" title="{link}" aria-label="{platform} Link for {page_title}" """
            f"""alt="{platform}" target="_blank">"""
            f"""{social_media_icon[platform]}{profile_id}</a>"""
        )
    else:
        return "&nbsp;"


def remove_lead_trail_slash(s):
    s = s.strip()
    if s.startswith("/"):
        s = s[1:]
    if s.endswith("/"):
        s = s[:-1]
    s = s.strip()
    return s


def get_profile_id(link):
    profile_id = None
    remove_list = ("c/", "user", "channel", "pages/", "/playlists", "?s=", "?fref=")
    if len(link.split(".com/")) > 1:
        profile_id = ".com/".join(link.split(".com/")[1:])
        if profile_id.strip().startswith(remove_list):
            profile_id = remove_lead_trail_slash(profile_id)
            # youtube has c/ user/ channel/
            profile_id = remove_lead_trail_slash(profile_id.replace("c/", "", 1))
            profile_id = remove_lead_trail_slash(profile_id.replace("user", "", 1))
            profile_id = remove_lead_trail_slash(profile_id.replace("channel", "", 1))
        profile_id = remove_lead_trail_slash(profile_id.replace("playlists", "", 1))
        # facebook has pages and fref
        profile_id = remove_lead_trail_slash(profile_id.replace("pages", "", 1))
        profile_id = profile_id.split("?fref=")[0]
        # twitter has ?s=
        profile_id = profile_id.split("?s=")[0]

        profile_id = remove_lead_trail_slash(profile_id)
    return profile_id


social_media_icon = {
    "Twitter": "<i class='fa fa-twitter fa-fw' style='color:#00acee'></i>",
    "Facebook": "<i class='fa fa-facebook fa-fw' style='color:#4267B2'></i>",
    "Instagram": "<i class='fa fa-instagram fa-fw' style='background:radial-gradient(circle at 30% 107%,#fdf497 0%,#fdf497 5%,#fd5949 45%,#d6249f 60%,#285AEB 90%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;'></i>",
    "YouTube": "<i class='fa fa-youtube-play fa-fw' style='color:#CD201F'></i>",
}


def end_html():
    # Generate the ending part of HTML
    end_html = """
        </tbody></table>
        </div><p></p>
        </body></html>
    """
    return end_html


def read_json_file(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    data_rows = read_json_file("data.json")
    table_rows = add_table_rows(data_rows)
    # Combine the HTML parts
    html_string = start_html() + table_rows + end_html()

    # Write the HTML content to a file
    with open("index.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_string)


if __name__ == "__main__":
    main()
