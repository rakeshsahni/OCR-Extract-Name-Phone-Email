from flask import Flask, redirect, render_template, request,url_for, jsonify, flash
import cv2
import easyocr
from werkzeug.utils import secure_filename
import re
import os
import spacy
import numpy as np
import shutil
import requests


app = Flask(__name__)


app.config['SECRET_KEY'] = '12345'

reader = easyocr.Reader(['en'])

nlp = spacy.load('en_core_web_sm')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_phone(stri) : 
    res = 0
    stri = stri.lower()
    for ch in stri : 
        # if (ch >= 'a' and ch <= 'z') : 
        #     print(ch)
        #     return False
        if ch >= "0" and ch <= "9" : 
            res += 1
    return res > 6

def check_mail(stri) : 
    stri = stri.lower()
    check_url = ['www', 'http', 'https', ":"]
    if "@" in stri : 
        return True

    if "com" in stri[-3:] : 
        for itm in check_url :
            if itm in stri : 
                return False
        return True

    return False 


# def inhance_image(img) :
#     # find the white rectangle
#     res_img = img.copy()
#     # in the image
#     gray = cv2.cvtColor(res_img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.medianBlur(gray, 5)
#     # gray = cv2.GaussianBlur(gray, (5, 5), 0)
#     # edged = cv2.Canny(gray, 75, 200)
#     edged = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARYn + cv2.THRESH_OTSU)
#     # cv2.cvtColor(res_img, cv2.COLOR_RGB2GRAY)

#     return edged



@app.route("/", methods = ['POST', "GET"])
def home() : 
    if request.method == 'POST':
        try :             
            # flash("No files or image url inserted...")
            # check if the post request has the file part
            if ('document_image' not in request.files) and ("document_image_url" not in request.form) :
                flash("No files or image url inserted...")
                # return redirect('index.html')
                return redirect(url_for('home'))
                # flash('No file part')
                # return redirect(request.url)
           
           
            document_image_url = request.form.get('document_image_url')
            print(document_image_url, "document_image_url" in request.form)
            image_file = request.files['document_image']
            current_image_path = ""
            current_image_OCR_path = "" 
            # if user does not select file, browser also
            # submit an empty part without filename
            if image_file.filename == '' and document_image_url == "" :
                flash("No files or image url selected...")
                return redirect(url_for('home'))
                # return redirect("index.html")
                # return jsonify({
                #     'message' : "No Selected Files"
                # })
                # flash('No selected file')
                # return redirect(request.url)
            elif image_file.filename == '' : 
                type_url = document_image_url.split(".")[-1].lower()

                if type_url not in ['png', 'jpg', 'jpeg'] : 
                    flash("Enter png, jpg or jpeg image url...")
                    return redirect(url_for('home'))
                
                file_name = document_image_url.split(".")[-2].split('/')[-1]
                
                # url = 'http://example.com/img.png'
                response = requests.get(document_image_url, stream=True)
                if response.status_code == 200 :
                    with open(f"static/images/{file_name}.{type_url}", 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    del response
                    current_image_path = f"static/images/{file_name}.{type_url}"
                    current_image_OCR_path = f"static/images/OCR_{file_name}.{type_url}"
                else : 
                    flash("Invalid image url...")
                    return redirect(url_for('home'))
                
            elif image_file and allowed_file(image_file.filename) :
                # print(image_file)
                
                image_filename = secure_filename(image_file.filename)
                # print(image_filename)

                current_image_path = f"static/images/{image_filename}"
                current_image_OCR_path = f"static/images/OCR_{image_filename}" 
                
                image_file.save(current_image_path)
            else : 
                flash("Problem In Uploaded files 404 error...")
                return redirect(url_for('home'))
                
            # img1 -> image path or image file 
            # IMAGE_PATH,paragraph="False"
            # IMAGE_PATH = "https://static-cse.canva.com/blob/650833/3HowtomakebusinesscardsCanva.png"
            output = reader.readtext(current_image_path)

            # output = reader.readtext(current_image_path)

            # print(output, len(output))
            
            
            image = cv2.imread(current_image_path)

            # image = inhance_image(image)

            # whole_str = ""
            dic_ = {
                "company_name" : [],
                "person_name" : [],
                "contact_num" : [],
                "emails" : []
            }
            for itm in output : 
                all_cord, text, accuracy = itm
                left_upper_pt = min(all_cord)
                right_buttom_pt = max(all_cord)
                cv2.rectangle(image, (left_upper_pt[0], left_upper_pt[1]), (right_buttom_pt[0], right_buttom_pt[1]), (0, 0, 255), 1)
                cv2.putText(image, text = f"{text}", org = (left_upper_pt[0], left_upper_pt[1]), fontFace = cv2.FONT_ITALIC, fontScale= 0.4, color = (255, 0, 0))
                # print(all_cord)
                # print(text)
                # whole_str += text + " "
                # print(accuracy)
                if check_mail(text) : 
                    dic_["emails"].append(text)
                
                if check_phone(text) : 
                    dic_["contact_num"].append(text)

                doc = nlp(text)
                for token in doc.ents :
                    if token.label_ == "ORG" : 
                        dic_["company_name"].append(token.text)
                    elif token.label_ == "PERSON" :
                        dic_["person_name"].append(token.text)  
                        # print(token.text, "->", token.label_)
                # print()
            # print(dic_)
            # print(whole_str)
            # cv2.imshow("transformed_img", image)
            cv2.imwrite(current_image_OCR_path, image)
            # cv2.waitKey(0)
            
            return render_template(
                "index.html",
                image_path = current_image_path,
                OCR_image_path = current_image_OCR_path,
                dic_ = dic_
            )

        except :
            flash("Problem In Uploaded files 404 error...")
            return redirect(url_for('home'))
            # return redirect('home') 
            # return jsonify({
            #     'message' : 'Problem In Uploaded files 404 error...'
            # })

    return render_template("index.html", img_done = False)


if __name__ == "__main__" : 
    app.run(debug=True)