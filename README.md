# Civic Media Scout

Civic Media Scout is an initiative dedicated to compile and curate public contact information from government websites. Our aim is to gather and present publicly accessible data, including comprehensive social media profiles and essential contact details, in an accessible and user-friendly manner.

By leveraging existing open source code and technologies, this project empowers citizens, researchers, and policymakers with a centralized resource for contacting a government entity. Join us in the journey to enhance civic engagement and information accessibility.


## How?

This repo contains code that can systematically crawl and read publicly available information from a list of government websites and parse them to identify the contact information, social media profiles. 

This tool utilizes the following open source packages:

 - [requests](https://pypi.org/project/requests/) - to query a website and download text/html
 - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) - to parse the html and extract information
 - [tldextract](https://pypi.org/project/tldextract/) - to distinguish URL's subdomain, domain and suffix
 - [DataTables](https://datatables.net/) - advanced table sorting, searching and pagination capabilities

To run this script, execute the below commands on the shell
```shell
git clone https://github.com/navchandar/civic-media-scout.git
cd civic_media_scout
pip install poetry
poetry install
py ./civic_media_scout/civic_media_scout.py
```

 ## Why?
 
__Accessibility and Convenience:__ Centralizing contact and social media information from multiple government websites makes it easier for citizens to access crucial government resources and officials' contact details.

__Transparency:__  Promotes transparency by making government information more readily available to the public, enhancing government accountability.

__Citizen Engagement:__ Facilitates citizen engagement with government officials and departments, enabling citizens to voice concerns, seek information, or provide feedback more efficiently and directly.

__Research and Analysis:__ Researchers and journalists may use this data for analysis, reporting, or academic purposes.

__Emergency Information:__ Provides a quick reference point for emergency contact information, which can be vital during disasters or crises.

__Community Building:__ Supports the development of online communities interested in government affairs and public policy discussions.


## Where?

 - The information takes long time to gather and update and this is by design
 - The tool waits for 1 to 3 seconds between every URL queried
 - The script uses websites from `base_urls.txt` file and crawls each website on loop
 - The gathered information is then stored in `data.json` file
 - The data file is then used to generate `index.html` file and hosted by [GitHub Pages](https://navchandar.github.io/civic-media-scout/)

## Legal Disclaimer

Civic Media Scout is a civic technology initiative that compiles and curates publicly accessible contact information from official government websites. The information presented herein is intended **solely for non-commercial purposes**, including academic research, public interest, civic engagement, transparency, and accessibility. **Any commercial use, replication, or monetization of this data is strictly prohibited.**

### Data Sources and Processing 

All data processed and displayed by this project is:

 - Publicly available and sourced from official government websites or platforms.
 - Factual in nature, including contact details and social media links, which are generally considered non-copyrightable.
 - Processed using open-source tools with deliberate throttling (1–3 seconds between requests) to avoid undue load on public servers.
 - This project operates under the exemption provisions of the [Digital Personal Data Protection Act, 2023](https://en.wikipedia.org/wiki/Digital_Personal_Data_Protection_Act,_2023), specifically:
   - **Section 3(3)(b):** Processing is conducted under the exemption for personal data made publicly available (i) voluntarily by the Data Principal or (ii) made public under a legal obligation
   - **Section 7 (Legitimate Use):** Processing is limited to legitimate uses such as public interest, transparency, and civic engagement, and does not involve the collection or processing of Sensitive Personal Data as defined under relevant regulations.

### No Warranty and Limitation of Liability

The information provided does not constitute solicitation, advertisement, or endorsement of any individual, institution, or government entity. While efforts are made to ensure accuracy, completeness, and timeliness, the data is provided **"AS IS" and without warranty** of any kind, express or implied. Users are advised to exercise discretion and verify information independently before acting upon it. The maintainers shall not be liable for any direct, indirect, incidental, special, consequential, or punitive damages, including loss of data or profit, arising from the use or inability to use the information provided. 


### Takedown and Redressal Mechanism

This project acts in good faith. If any individual or government entity finds that the published information is inaccurate, non-public, or wishes to have their details removed from this public compilation, they may [raise an issue on this GitHub repository](https://github.com/navchandar/civic-media-scout/issues). We are committed to reviewing and addressing all valid requests promptly.
 

