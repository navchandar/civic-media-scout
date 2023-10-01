# Civic Media Scout

Civic Media Scout is an initiative dedicated to compile and curate public contact information from government websites. Our aim is to gather and present publicly accessible data, including comprehensive social media profiles and essential contact details, in an accessible and user-friendly manner.

By leveraging existing open source code and technologies, this project empowers citizens, researchers, and policymakers with a centralized resource for contacting a government entity. Join us in the journey to enhance civic engagement and information accessibility.


## How?

This repo contains code that can systematically crawl and read publicly available information from a list of government websites and parse them to identify the contact information, social media profiles. 

This tool utilizes the following open source packages:

 - [requests](https://pypi.org/project/requests/) - to query a website and download text/html
 - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) - to parse the html and extract information
 - [tldextract](https://pypi.org/project/tldextract/) - to distinguish URL's subdomain, domain and suffix

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

## Disclaimer

The information provided under this repository is exclusively for general informational purposes only, should not be interpreted as soliciting or advertisement. The data collected and presented on this repository may lack accuracy, comprehensiveness, or timeliness. The operator(s) of this repository abstain from making any representations or assurances concerning the accuracy or dependability of the information herein. We are not liable for any consequence of any action taken by the user relying on material / information provided under this repository.