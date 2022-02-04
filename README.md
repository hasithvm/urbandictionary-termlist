# UrbanDictionary.com TermList
Scrapes the Urban Dictionary robots.txt sitemap to generate a list of terms. Created to make cheating at Lewdle a little bit easier.

Last run on 02/04/2022.

Original content by the original authors and UrbanDictionary.com.

## Pre-requisites

Dependencies are captured in requirements.txt, please run pip install to download and install these dependencies.

    $> pip install requirements.txt

## Usage

    $> python main.py 


### Output
Generates `low.txt` in the current working directory. UrbanDictionary words are unicode so the text file is encoded UTF-8.

## License
Licensed under the WTFPL, please see LICENSE.txt.
