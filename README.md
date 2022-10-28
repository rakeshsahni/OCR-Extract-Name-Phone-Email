

https://user-images.githubusercontent.com/80037791/198703605-96f94856-d62e-4192-8de1-e4b711bd353a.mp4

# OCR-Extract-Name-Phone-Email

Hi! I am Rakesh Sahni B.E Final year computer science.
Out website : https://sohipm.com

#### used library
flask, cv2, easyocr, spacy, requests, numpy, pandas, matplotlib etc.

#### Intro : 
In this app if we will upload  business cards / visiting cards then our DL ( deep learning model ) will return name, company name, contact number and email id of corresponding card. 

process to build this app

1.) To build this app I have used easyocr which is nothing but a font-dependent printed character reader based on a template matching algorithm.

2.) This EasyOCR return all texts which is found into inserted Image.

3.) After If we had all texts which is in given images then we will apply Named Entity Recognition (NER).

4.) With the help of Spacy NLP library I would applyed NER ( Name Entity Recognition ) to see extract Name of Person and Name of Company.

5.) See we have to also extract Email and Phone Number right. In that situation I have used RegEx ( re ) python pattern matching.

6.) At end I have show two image one is original and other is OCR image which is detect all texts and also show a table in which company_name, person_name, contact_num and emails details show.

7.) Deployment To build A Web App with the help of Flask and do some HTML and CSS for design which is shown in Given Video.

## Installation

open terminal and type simply

```bash
pip install -r requirements.txt
```

After installation all python package simply write command in terminal

```bash
python app.py
```
Remember you are in app ( root ) folder

#### Thank you!
