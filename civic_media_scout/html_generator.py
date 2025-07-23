import json

import chardet
import tldextract

json_file = "data.json"


def start_html():
    # Generate the starting part of HTML
    start_html = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <title>Civic Media Scout Project</title>
        <meta name="description" content="Civic Media Scout is an initiative dedicated to compile and curate public contact information from government websites. Our aim is to gather and present publicly accessible data, including comprehensive social media profiles and essential contact details, in an accessible and user-friendly manner.">
        <link rel="shortcut icon" href="data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEVHcEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAt9G3DAAAAC3RSTlMAOWHbDyfF5pq2ft43pKsAAAFjSURBVEjHY2AYBdhAoCheaRZNY+NGBzzyahaigc2TcKpgXZwVwMDA2AwisQHG5iQHhiBVBtZlFgLY5J0mA832MDZWALrEQgSbfCOQbFaJKgK6RdJSBV0+KrkVZEshA8NikBslzJaiykMFmFIYGITBDogybkT2ngTUSC64AganZCQVHJVQKxkNoVaAVExfAFcgrgBjNasEFcHYTIVwBcrwsAN7E2axERYFoIDCrwA55BEKxGd0YAGdCDcwdXRWAkXSZ0wHqmyr7CwDcoBMBRTjWFwclAOCFVxcmEygHNSUMHlmWqalg6fltLTJU6AcVBdFVKxqb2Vgbe9aURUA5aAlBkMG4QBQODOagjniAqMKRhVQoEBIq0pp+SIlIAYylECcJkUU/WZpGMAc2QyuFBcM4LaAkIIlCHmvyWWYVqSbIVSIL1JahAm0ConP3cqioVhAIEJBcDlWYIowTAkrCBitHREAAIkeqW4JskK7AAAAAElFTkSuQmCC" />
        <link rel="stylesheet" href="style.css">
        
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
              <span>
                <em>Civic Media Scout</em> is a civic-tech initiative focused on compiling and curating <em>publicly
                  available</em> contact information from official government websites. The objective is to present this
                data—including verified social media handles and essential contact details—in a structured, accessible, and
                user-friendly format.
              </span><br>
              <span>
                By leveraging open-source technologies and publicly accessible data, this platform aims to support citizens,
                researchers, and policymakers by offering a <em>centralized</em> resource for engaging with government
                entities. We invite you to be part of this effort to promote transparency, civic participation, and digital
                accessibility.
              </span><br>
              <span>
                <strong>Disclaimer:</strong>
                The information provided on this website is intended solely for general informational purposes and does not
                constitute solicitation, advertisement, or legal advice. While efforts are made to ensure the accuracy and
                relevance of the data, no guarantees are made regarding its completeness, accuracy, or timeliness.

                The operators of this website disclaim any liability for actions taken based on the information presented
                herein. Users are advised to independently verify any information before relying on it for official or
                personal use.
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
    existing_contact_info = set()
    # Create a row using values from the data dictionary
    for data in data_rows:
        page_title = data.get("Page Title", "None")
        page_title = (
            page_title.replace("https:", "")
            .replace("http:", "")
            .replace("www.", "")
            .replace('"', "")
            .replace(".::", "")
            .replace("::.", "")
            .replace("-", "")
            .strip()
        )
        source_url = data.get("Source URL", "None")
        short_url = (
            data.get("Source URL", "None")
            .replace("https:", "")
            .replace("http:", "")
            .replace("www.", "")
            .strip("/")
        )
        # save contact data in a tuple
        contact_info = tuple(
            [
                data.get("Twitter", ""),
                data.get("Facebook", ""),
                data.get("Instagram", ""),
                data.get("YouTube", ""),
                tuple(data.get("Phone", [])),
                tuple(data.get("Email", [])),
            ]
        )

        # avoid duplicate rows of information
        if contact_info not in existing_contact_info:
            existing_contact_info.add(contact_info)
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
        print(f"{platform} : {profile_id}")
        if profile_id:
            return (
                f"""<a href="{link}" title="{link}" aria-label="{platform} link of {page_title}" """
                f"""target="_blank">{social_media_icon[platform]}"""
                f"""<span class="link-text">{profile_id}</span></a>"""
            )
        else:
            return "&nbsp;"
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
        profile_id = profile_id.split("?view_as=")[0]
        profile_id = profile_id.split("?si=")[0]
        profile_id = profile_id.split("?feature=")[0]
        profile_id = profile_id.split("?locale=")[0]

        # facebook has pages and fref
        profile_id = remove_lead_trail_slash(profile_id.replace("pages", "", 1))
        profile_id = profile_id.split("?ref=")[0]
        profile_id = profile_id.split("?fref=")[0]
        profile_id = profile_id.split("?mibextid=")[0]
        profile_id = profile_id.split("?ti=")[0]
        profile_id = profile_id.split("?extid=")[0]
        profile_id = profile_id.split("?modal=")[0]

        # twitter has ?s=  and lang and status
        profile_id = profile_id.split("?s=")[0]
        profile_id = profile_id.split("?lang=")[0]
        profile_id = profile_id.split("/status/")[0]
        profile_id = profile_id.split("?ref_src=")[0]
        profile_id = profile_id.split("?t=")[0]
        profile_id = profile_id.split("?itsct=")[0]
        profile_id = profile_id.split("?mx=")[0]
        profile_id = profile_id.split("?original_referer=")[0]

        profile_id = profile_id.split("?utm_medium=")[0]

        # instagram has ?hl=
        profile_id = profile_id.split("?hl=")[0]
        profile_id = profile_id.split("?igshid=")[0]

        profile_id = remove_lead_trail_slash(profile_id)
    return profile_id


social_media_icon = {
    "Twitter": "<i class='fa fa-twitter fa-fw twitter_color'></i>",
    "Facebook": "<i class='fa fa-facebook fa-fw facebook_color'></i>",
    "Instagram": "<i class='fa fa-instagram fa-fw instagram_color'></i>",
    "YouTube": "<i class='fa fa-youtube-play fa-fw youtube_color'></i>",
}


def end_html():
    # Generate the ending part of HTML
    end_html = """
        </tbody></table>
        </div>
        
    <footer>
        <!-- GitHub Source Code Link -->
        <a href="https://github.com/navchandar/civic-media-scout" target="_blank">
        Source: GitHub
        </a>
        <!-- License Information -->
        <span>|</span>
        <a href="https://github.com/navchandar/civic-media-scout/blob/main/LICENSE" target="_blank">
        Open Source (MIT License)
        </a>
        <span>|</span>
        <!-- Font Awesome Icons Attribution -->
        <a href="https://fontawesome.com/v4/" target="_blank">Icons by Font Awesome</a>
    </footer>

    <script src="script.js"></script>

    </body></html>
    """
    return end_html


def make_css():
    # CSS content for styling the table and layout
    css_content = """
/* style.css */
:root {
    --darkbg: #232224;
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
    font-family: "Lucida Sans Unicode", "Lucida Grande", "Lucida Sans", Geneva,
        Verdana, sans-serif;
    font-size: 13px;
    overflow: -moz-scrollbars-vertical;
    overflow-y: scroll !important;
}

body {
    transition: all 0.2s ease-in-out;
    background: var(--darkbg);
    color: var(--darkt);
}

.light {
    background: var(--lightbg);
    color: var(--lightt);
}

.tdnn {
    margin: 0 auto;
    font-size: 15%;
    position: absolute;
    top: 6em;
    right: 15em;
    display: inline-block;
    height: var(--toggleHeight);
    width: var(--toggleWidth);
    border-radius: var(--toggleHeight);
    transition: all 500ms ease-in-out;
    background: var(--bgColor--night);
}

.day {
    background: #ffbf71;
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
    box-shadow: 3em 2.5em 0 0em var(--mooncolor) inset,
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
    box-shadow: 3em 3em 0 5em #fff inset, 0 -5em 0 -2.7em #fff,
        3.5em -3.5em 0 -3em #fff, 5em 0 0 -2.7em #fff, 3.5em 3.5em 0 -3em #fff,
        0 5em 0 -2.7em #fff, -3.5em 3.5em 0 -3em #fff, -5em 0 0 -2.7em #fff,
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
    background-image: linear-gradient(
        to right,
        #ffffff00,
        #ffffff00,
        #ffffff00,
        #ffffff00
    );
}

tr:hover {
    background: #fff0;
    background-image: linear-gradient(
        to right,
        #5ed0ff54,
        #55f5a84d,
        #37f99c54,
        #21b46d57
    );
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
    padding: 0.75em 0.75em;
    margin: 0.33em;
    background-color: darkcyan;
    border-radius: 15px;
    font-size: larger;
}

.light .hoverable > .hoverable__tooltip {
    background-color: mediumturquoise;
}

.hoverable > .hoverable__main {
    position: absolute;
    white-space: pre-line;
    color: black;
}

.hoverable.active > .hoverable__tooltip {
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
    -webkit-overflow-scrolling: touch; 
    height: 89vh;
    width: 100%;
}

a {
    text-decoration: none;
    color: inherit;
    transition: color 0.1s ease, text-shadow 0.1s ease;
}

a:hover {
    text-decoration: underline;
    text-shadow: 0 0 0.05em currentColor;
    color: var(--link-hover-color, #007bff);
}

footer {
    background-color: #d3d3d3;
    color: #000;
    padding: 0.3em;
    text-align: center;
    position: fixed;
    bottom: 0;
    width: 100%;
}
.dataTables_length {
    position: fixed;
    left: 20px;
    top: 16px;
    font-size: 1.2em;
}
.dataTables_filter {
    position: fixed;
    right: 200px;
    top: 16px;
    font-size: 1.2em;
}
.dataTables_filter input{
    width: 300px;
    height: 25px;
}
.dataTables_filter input:hover, .dataTables_wrapper .dataTables_length select{
    border: 2px solid #6c6c6c;
}

table td,
table th {
    outline: 0;
    -webkit-tap-highlight-color: transparent;
}

.twitter_color {
    color: #00acee !important;
}

.facebook_color {
    color: #4267b2 !important;
}

.instagram_color {
    background: radial-gradient(
        circle at 30% 107%,
        #fdf497 0%,
        #fdf497 5%,
        #fd5949 45%,
        #d6249f 60%,
        #285aeb 90%
    );
    background-clip: border-box;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.youtube_color {
    color: #cd201f !important;
}

#content-table_paginate {
    text-align: center;
    float: none;
    width: 100%;
}

.link-text {
    display: inline;
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

    
    .hoverable.active > .hoverable__tooltip {
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
    
    .dataTables_length, .dataTables_filter {
        position: static;
        font-size: 0.8em;
    }
    .dataTables_filter input{
        width: 250px;
        height: 25px;
    }

    footer {
        font-size: 0.8em;
    }
    
    .link-text {
        display: none;
    }

    table td:nth-child(3),
    table td:nth-child(4),
    table td:nth-child(5),
    table td:nth-child(6) {
        text-align: center;
    }

}
    """
    with open("style.css", "w", encoding="utf-8") as css_file:
        css_file.write(css_content)
    print("style.css file saved")


def make_js():
    # JS content for initializing DataTable and toggling theme
    js_content = """
    // script.js

    // Set data table pagination button count based on screen width
    if (window.innerWidth < 576) {
        $.fn.DataTable.ext.pager.numbers_length = 5; // Small screens
    } else if (window.innerWidth < 768) {
        $.fn.DataTable.ext.pager.numbers_length = 8; // Medium screens
    } else {
        $.fn.DataTable.ext.pager.numbers_length = 13; // Large screens
    }

    $(document).ready(function() {
        $('#content-table').DataTable({
            order: [], // Use existing order of the table
            pageLength: 25, // Show 25 rows per page
            lengthChange: true, // Allow user to change page length
            responsive: true, // Make table responsive
            autoWidth: false, // Prevent automatic column width
            language: {
                search: "Search records:",
                lengthMenu: "Show _MENU_ entries per page",
                info: "Showing _START_ to _END_ of _TOTAL_ entries"
            }
        });
    });

    $('.tdnn').click(function() {
        $("body").toggleClass('light');
        $(".moon").toggleClass('sun');
        $(".tdnn").toggleClass('day');
    });


    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".hoverable").forEach(function (el) {
            el.addEventListener("click", function (e) {
                // Close other tooltips
                document.querySelectorAll(".hoverable").forEach(function (other) {
                    if (other !== el) other.classList.remove("active");
                });

                // Toggle current tooltip
                el.classList.toggle("active");
            });
        });

        // Optional: Close tooltip when clicking outside
        document.addEventListener("click", function (e) {
            if (!e.target.closest(".hoverable")) {
                document.querySelectorAll(".hoverable").forEach(function (el) {
                    el.classList.remove("active");
                });
            }
        });
    });
    """

    with open("script.js", "w", encoding="utf-8") as js_file:
        js_file.write(js_content)
    print("script.js file saved")


def make_html(table_rows) -> None:
    html_string = start_html() + table_rows + end_html()

    # Write the HTML content to a file
    with open("index.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_string)
    print("index.html file saved")


def read_json_file(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_main_domain(url) -> str:
    # Use tldrextract to get the domain from url
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"


def detect_encoding(byte_data):
    result = chardet.detect(byte_data)
    return result["encoding"]


def decode_if_garbled(value):
    COMMON_ENCODINGS = ["latin1", "windows-1252", "iso-8859-1", "utf-8"]
    if isinstance(value, str):
        for encoding in COMMON_ENCODINGS:
            try:
                # interpret the string as if it was mis-decoded
                byte_data = value.encode(encoding)
                detected = detect_encoding(byte_data)
                if detected and detected.lower() != encoding:
                    return byte_data.decode(detected)
            except Exception:
                continue
    return value


def clean_json_dict(data):
    if isinstance(data, dict):
        return {k: clean_json_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_json_dict(item) for item in data]
    else:
        return decode_if_garbled(data)


def sort_saved_json(indent=4):
    # Load JSON file
    with open(json_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    print(f"Found {len(raw_data)} values in {json_file}")
    cleaned_json = clean_json_dict(raw_data)

    for item in cleaned_json:
        if ("X Corp" in item) and item["X Corp"]:
            item["Twitter"] = item["X Corp"]
            del item["X Corp"]

    # Sort by domain and then by Source URL
    sorted_data = sorted(
        cleaned_json,
        key=lambda x: (
            f"{extract_main_domain(x['Source URL'])}",
            x["Source URL"],
        ),
    )

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=indent)
    print("Output saved to:", json_file)


def main():
    sort_saved_json()
    data_rows = read_json_file(json_file)
    table_rows = add_table_rows(data_rows)
    # Combine the HTML parts
    make_css()
    make_js()
    make_html(table_rows)


if __name__ == "__main__":
    main()
