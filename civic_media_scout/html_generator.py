import json


def start_html():
    # Generate the starting part of HTML
    start_html = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <title>Civic Media Scout Project</title>
        <meta name="description" content="Civic Media Scout is an initiative dedicated to compile and curate public contact information from government websites. Our aim is to gather and present publicly accessible data, including comprehensive social media profiles and essential contact details, in an accessible and user-friendly manner.">
        <style>
        :root {
          --darkbg:#232224;
          --darkt: #dbd7db;
          --lightbg: #f4f3f3;
          --lightt: #141414;
          
          --toggleHeight: 16em;
          --toggleWidth: 30em;
          --toggleBtnRadius: 10em;

          --bgColor--night: #423966;
          --toggleBtn-bgColor--night: var(--bgColor--night);
          --mooncolor: #e8fafc;
          --bgColor--day: #9ee3fb;
          --toggleBtn-bgColor--day: var(--bgColor--day);
        }
            html,
            body {
              height: 100%;
              width: 100%;
              margin: 0;
              display: table;
              font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif;
              font-size: 13px;
            }
            body{
                transition: all .2s ease-in-out;
                background: var(--darkbg);
                color: var(--darkt);
            }
            .light{
              background: var(--lightbg);
              color: var(--lightt);
            }
            .tdnn {
              margin: 0 auto;
              font-size: 15%;
              position: absolute;
              top: 3em;
              right: 15em;
              display: inline-block;
              height: var(--toggleHeight);
              width: var(--toggleWidth);
              border-radius: var(--toggleHeight);
              transition: all 500ms ease-in-out;
              background: var(--bgColor--night);
            }
            .day{
              background: #FFBF71;
            }
            .moon {
              position: absolute;
              display: block;
              border-radius: 50%;
              transition: all 400ms ease-in-out;
              
              top: 3em;
              left: 3em;
              transform: rotate(-75deg);
              width: var(--toggleBtnRadius);
              height: var(--toggleBtnRadius);
              background: var(--bgColor--night);
              box-shadow: 
                3em 2.5em 0 0em var(--mooncolor) inset,
                rgba(255, 255, 255, 0.1) 0em -7em 0 -4.5em,
                rgba(255, 255, 255, 0.1) 3em 7em 0 -4.5em,
                rgba(255, 255, 255, 0.1) 2em 13em 0 -4em,
                rgba(255, 255, 255, 0.1) 6em 2em 0 -4.1em,
                rgba(255, 255, 255, 0.1) 8em 8em 0 -4.5em,
                rgba(255, 255, 255, 0.1) 6em 13em 0 -4.5em,
                rgba(255, 255, 255, 0.1) -4em 7em 0 -4.5em,
                rgba(255, 255, 255, 0.1) -1em 10em 0 -4.5em;
            }
            .sun {
              top: 4.5em;
              left: 18em;
              transform: rotate(0deg);
              width: 7em;
              height: 7em;
              background: #fff;
              box-shadow: 3em 3em 0 5em #fff inset,
                0 -5em 0 -2.7em #fff,
                3.5em -3.5em 0 -3em #fff,
                5em 0 0 -2.7em #fff,
                3.5em 3.5em 0 -3em #fff,
                0 5em 0 -2.7em #fff,
                -3.5em 3.5em 0 -3em #fff,
                -5em 0 0 -2.7em #fff,
                -3.5em -3.5em 0 -3em #fff;
            }
            p {
              margin: 0.3em 1em;
            }
            
            table {
              border-spacing: 0;
              border-collapse: collapse;
              empty-cells: hide;
              width: 100%;
              margin: 0 auto;
              table-layout: fixed;
              font-size: 1.1em;
              line-height: 1.3em;
            }
            
            th {
              top: 0;
              position: sticky !important;
              padding: 0.14em;
              box-sizing: border-box;
              color: #fff !important;
              height: 2em;
              background-color: #145a8d !important;
              border: 0em solid rgb(204, 204, 204);
              z-index: 1;
            }
            
            td {
              white-space: nowrap;
              overflow: hidden;
              text-overflow: ellipsis;
              max-width: 8em;
              height: auto;
              max-height: 5em;
              padding: 0.14em;
              text-align: center;
              border: 0.0036em solid rgb(204, 204, 204);
            }
            
            table td:nth-child(1) {
              max-width: 14em;
              text-align: left;
              padding: 0 0.36em;
            }
            
            table td:nth-child(2) {
              max-width: 11em;
              text-align: left;
              padding: 0 0.36em;
            }
            
            table td:nth-child(3),
            table td:nth-child(4),
            table td:nth-child(5),
            table td:nth-child(6),
            table td:nth-child(7),
            table td:nth-child(8) {
              max-width: 9em;
              text-align: left;
              padding-left: 0.33em;
              padding-top: 0.33em;
            }
            table td:nth-child(8) {
              max-width: 11em;
            }
            
            tr {
              border-bottom: 0.07em solid #ddd;
              padding: 0.36em;
              background: #fff0;
              background-image: linear-gradient(to right, #ffffff00, #ffffff00, #ffffff00, #ffffff00);
            }
            
            tr:hover {
              background: #fff0;
              background-image: linear-gradient(to right, #5ed0ff54, #55f5a84d, #37f99c54, #21b46d57);
              box-shadow: 0 0.14em 0.21em 0 rgba(4, 128, 123, 0.45);
              background-blend-mode: screen;
            }

            .hoverable {
              text-align: center;
              max-width: fit-content;
              margin: 0 auto;
            }
            
            .hoverable > .hoverable__tooltip {
              display: none;
              padding: 0.33em 0.33em;
              margin: 0.33em;
              background-color: #2980b9;
            }
            
            .hoverable > .hoverable__main {
              position: absolute;
              white-space: pre-line
              color: black;
            }
            
            .hoverable:hover > .hoverable__tooltip {
              display: inline;
              position: absolute;
              top: 2.5em;
              left: 10em;
              right: 10em;
              border: 0;
              z-index: 99;
              text-align: left;
            }
            
            h1 {
              text-align: center;
              font-size: 1.3em;
              color: #2980b9;
              margin: 0.36em 0 0.36em 0;
              position: relative;
              display: inline-block;
            }
            
            sup {
              text-align: center;
              font-size: 0.86em;
              color: black;
              margin: 0.36em 0 0.36em 0;
              position: relative;
              display: inline-block;
            }
            
            sup:hover {
              -o-transition: 0.2s;
              -ms-transition: 0.2s;
              -moz-transition: 0.2s;
              -webkit-transition: 0.2s;
              transition: 0.2s;
              text-shadow: 0.07em 0.07em 0.14em #888888;
            }
            
            .table-container {
              overflow-x: auto;
              overflow-y: scroll;
              height: 87vh;
            }
            
            a {
              text-decoration: none;
            }
            
            a:hover {
              -o-transition: 0.05s;
              -ms-transition: 0.05s;
              -moz-transition: 0.05s;
              -webkit-transition: 0.05s;
              transition: 0.05s;
              text-shadow: 0px 0px 0.07em #888;
              text-decoration: underline;
            }
            
            footer {
              background-color: #D3D3D3;
              color: #000;
              padding: 0.3em;
              text-align: center;
              font-size: 0.8em;
            }
                        
            table td,
            table th {
              outline: 0;
              -webkit-tap-highlight-color: transparent;
            }
            
            /* Media query for smaller screens (e.g., mobile devices) */
            @media (max-width: 600px) {
              table {
                width: 100%;
                font-size: 0.8em !important;
              }
              td {
                padding: 0.5em 0.1em !important;
              }
              th {
                padding: 1em 0em !important;
              }
              .hoverable:hover > .hoverable__tooltip {
                top: 2.5em !important;
                left: 1em !important;
                right: 1em !important;
              }
              table th:nth-child(1),
              table th:nth-child(4),
              table th:nth-child(5),
              table th:nth-child(6) {
                width: 5em;
              }
              .tdnn {
                font-size: 10%;
                top: 10em;
                right: 20em;
              }
            }
            
        </style>
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
        <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

    </head>
    <body class="light">
        <div style="margin: 0 auto;">
        <div class="hoverable">
            <h1>Civic Media Scout
                <span class="hoverable__main"><sup>&epar;</sup></span>
            </h1>
            <span class="hoverable__tooltip">
                <span><em>Civic Media Scout</em> is an initiative dedicated to compile and curate <em>public</em> contact information from government websites. Our aim is to gather and present publicly accessible data, including comprehensive social media profiles and essential contact details, in an accessible and user-friendly manner.</span><br>
                <span>By leveraging existing open source code and technologies, this project empowers citizens, researchers, and policymakers with a <em>centralized</em> resource for contacting a government entity. Join us in the journey to enhance civic engagement and information accessibility.</span><br>
                
                <span><strong>Disclaimer:</strong>
                The information provided under this website is exclusively for general informational purposes only, should not be interpreted as soliciting or advertisement. The data collected and presented on this website may lack accuracy, comprehensiveness, or timeliness.

                The operator(s) of this website abstain from making any representations or assurances concerning the accuracy or dependability of the information herein. We are not liable for any consequence of any action taken by the user relying on material / information provided under this website.
                </span>
            </span>
        </div>
         <div class="tdnn day">
          <div class="moon sun"></div>
        </div>
        </div>
        <div class="table-container">
        <table id="content-table">
        <thead>
            <tr>
                <th data-column="title" scope="col" title="Source Page Title">Page Title</th>
                <th data-column="sourceurl" scope="col" title="Source Website URL">Source URL</th>
                <th data-column="twitter" scope="col" title="Twitter Profile">Twitter</th>
                <th data-column="facebook" scope="col" title="Facebook Profile">Facebook</th>
                <th data-column="instagram" scope="col" title="Instagram Profile">Instagram</th>
                <th data-column="youtube" scope="col" title="Youtube Channels">Youtube</th>
                <th data-column="phone" scope="col" title="Phone Numbers">Phone</th>
                <th data-column="email" scope="col" title="Email Addresses">Email</th>
            </tr>
        </thead>
        <tbody>
    """
    return start_html


def add_table_rows(data_rows):
    table_rows = ""
    existing_contact_info = list()
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
        contact_info = [
            data.get("Twitter", ""),
            data.get("Facebook", ""),
            data.get("Instagram", ""),
            data.get("YouTube", ""),
            data.get("Phone", ""),
            data.get("Email", ""),
        ]

        # avoid duplicate rows of information
        if contact_info not in existing_contact_info:
            existing_contact_info.append(contact_info)
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
            # remove space in href links
            link = contact.replace(" ", "")
            rows += f'<a title="{contact}" href="{uri}{link}">{contact}</a><br>'
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
            f"""target="_blank">{social_media_icon[platform]}{profile_id}</a>"""
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
        <script>
        $(document).ready( function () {
            $('#content-table').DataTable({
                order: [[1, 'asc']]
            });
        } );
        
        $('.tdnn').click(function () {
          $("body").toggleClass('light');
          $(".moon").toggleClass('sun');
          $(".tdnn").toggleClass('day');
        });
        </script>
        <footer>
    <!-- GitHub Source Code Link -->
    <a href="https://github.com/navchandar/civic-media-scout" target="_blank">
        View Source on GitHub
    </a>
    <!-- License Information -->
    <span>|</span>
    <a href="https://github.com/navchandar/civic-media-scout/blob/main/LICENSE" target="_blank">
        License - MIT
    </a>
    <span>|</span>
    <!-- Font Awesome Icons Attribution -->
    <a href="https://fontawesome.com/v4/" target="_blank">Icons by Font Awesome</a>
</footer>
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
