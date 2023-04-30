## How to clone the project

1. Clone the directory
git clone https://github.com/abdallam1007/NLP_QA_QG.git

2. Enter the directory
    `cd NLP_QA_QG`

3. Upgrade the pip command
    `python3 -m pip install --user --upgrade pip`

4. Create a virtual environment
    `python3 -m venv env`

5. Activate the virtual environment
    `source env/bin/activate`

6. Download all requirements
    `python3 -m pip install -r requirements.txt`

7. Download the Stanford CoreNLP Library files

    1. Go to the Stanford CoreNLP downloads page: https://stanfordnlp.github.io/CoreNLP/download.html

    2. Under the "Previous Versions" section, click on the link for version 4.5.4.

    3. Scroll down to the "Downloads" section and download the file     "stanford-corenlp-4.5.4.zip"

    4. Extract the contents of the zip file to the libs directory
## How to run the project

### Running the QG component
python3 ask.py data/set_i/article n
### Running the QA component
python3 answer.py data/set_i/article questions/questions.txt


## Aditional Notes and issues with installing requirements

Website for downloading nltk: https://stackoverflow.com/questions/41691327/ssl-sslerror-ssl-certificate-verify-failed-certificate-verify-failed-ssl-c/41692664#41692664
