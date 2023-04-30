## How to clone the project

1. Clone the directory
git clone https://github.com/abdallam1007/NLP_QA_QG.git

2.  Enter the directory
cd NLP_QA_QG

3. Upgrade the pip command
python3 -m pip install --user --upgrade pip

4. Create a virtual environment
python3 -m venv env

5. Activate the virtual environment
source env/bin/activate

6. Download all requirements
python3 -m pip install -r requirements.txt

## How to run the project

### Running the QG component
python3 ask.py data/set_i/article n
### Running the QA component
python3 answer.py data/set_i/article questions/questions.txt


## Aditional Notes and issues with installing requirements

Website for downloading nltk: https://stackoverflow.com/questions/41691327/ssl-sslerror-ssl-certificate-verify-failed-certificate-verify-failed-ssl-c/41692664#41692664