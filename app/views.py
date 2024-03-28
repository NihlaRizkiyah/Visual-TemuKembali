from app import app
from app import VisualSearch
import time
import json
import os
from flask import render_template,request,redirect,send_from_directory,make_response,jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import json
import time
import cv2
from flask import Flask, render_template, request, redirect
from flask_cors import cross_origin
from flask import Flask, request
import smtplib
from flask import jsonify


ProductsJSON = {}
@cross_origin()
@app.route("/")
def index():
    return render_template('public/index.html')

@cross_origin()
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(app.config["FAVICON_PATH"], 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@cross_origin()
@app.route("/about")
def about():
    return render_template('public/about.html')

@cross_origin()
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        print(request.form['name'])
        print(request.form['email'])
        print(request.form['message'])
        # Replace the placeholders with your email server details
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'farhanyutub068@gmail.com'
        smtp_password = 'uxwb mksa ieoz wjfm'
        to_email = 'farhanyutub068@gmail.com'

        # Create the email message
        subject = 'New Contact Form Submission'
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        # Send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, to_email, f'Subject: {subject}\n\n{body}')
            return render_template('public/contact.html')
        except Exception as e:
            return f'Error sending the message. Please try again later. Error: {str(e)}'

    return render_template('public/contact.html')


# @cross_origin()
# @app.route("/sendsmtp", methods=["POST"])
# def sendsmtp():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']

#         print(request.form['name'])
#         print(request.form['email'])
#         print(request.form['message'])
#         # Replace the placeholders with your email server details
#         smtp_server = 'smtp.gmail.com'
#         smtp_port = 587
#         smtp_username = 'farhanyutub068@gmail.com'
#         smtp_password = 'uxwb mksa ieoz wjfm'
#         to_email = 'farhanyutub068@gmail.com'

#         # Create the email message
#         subject = 'New Contact Form Submission'
#         body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

#         # Send the email
#         try:
#             with smtplib.SMTP(smtp_server, smtp_port) as server:
#                 server.starttls()
#                 server.login(smtp_username, smtp_password)

#                 server.sendmail(smtp_username, to_email, f'Subject: {subject}\n\n{body}')

#             return 'Your message has been sent successfully!'
#         except Exception as e:
#             return f'Error sending the message. Please try again later. Error: {str(e)}'

#     return render_template('public/contact.html')


@cross_origin()
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory(app.config["DATASET_IMAGES_PATH"], filename)



@cross_origin()
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    global ProductsJSON
    f = open(app.config["JSON_PATH"])
    ProductsJSON = json.load(f)
    res = []
    items = []
    if request.method == "POST":

        if request.files:
            image = request.files["image"]
            image.save(app.config["IMAGE_UPLOAD_LOCATION"])
            
            #return redirect(request.url)
            start = time.process_time()
            search = VisualSearch.VisualSearch(dataset=app.config["DATASET"])
            search.run(app.config["IMAGE_UPLOAD_LOCATION"], model=app.config["MODEL_NAME"], remove_not_white=False)
            items = search.similar_items_path()
            print("Time taken : ", time.process_time() - start)
            print("Gambar berhasil disimpan di 'input_image'")

            # Extracting Products Data
            
            for item in items[0:16]:
                itm_q = {}
                itm = item.split('.')
                itm_p = ProductsJSON[itm[0]]
                itm_q['title'] = item
                itm_q['desc'] = itm[0]
                try:
                    itm_q['rating'] = itm_p['rating']
                except:
                    itm_q['rating'] = 2
                itm_q['URL'] = itm_p['URL']
                res.append(itm_q)

    return render_template("public/recommend.html", items = res)

@cross_origin()
@app.route("/camera", methods=["GET","POST"])
def camera():
    global ProductsJSON
    f = open(app.config["JSON_PATH"])
    ProductsJSON = json.load(f)
    items = []
    res = []
    if request.method == "POST":
        # if request.files:
        #     image = request.files["live-camera"]
        #     image.save(app.config["IMAGE_UPLOAD_LOCATION"])
        #     print("Live Camera berhasil disimpan di 'input_image'")
            #return redirect(request.url)
            start = time.process_time()
            search = VisualSearch.VisualSearch(dataset=app.config["DATASET"])
            search.run(app.config["IMAGE_UPLOAD_LOCATION"], model=app.config["MODEL_NAME"], remove_not_white=False)
            items = search.similar_items_path()
            print("Time taken : ", time.process_time() - start)

            # Extracting Products Data
     
            for item in items[0:16]:
                itm_q = {}
                itm = item.split('.')
                itm_p = ProductsJSON[itm[0]]
                itm_q['title'] = item
                itm_q['desc'] = itm[0]
                try:
                    itm_q['rating'] = itm_p['rating']
                except:
                    itm_q['rating'] = 2
                itm_q['URL'] = itm_p['URL']
                res.append(itm_q)

    return render_template("public/recommend.html", items = res)


@app.route('/capture', methods=['GET', 'POST'])
def capture():
    if request.method == 'POST':
        camera()  # Panggil fungsi untuk menangkap gambar saat permintaan POST diterima
    return render_template('public/recommend.html')

@cross_origin()
@app.route("/perform_task", methods=["GET"])
def perform_task():
    # Panggil fungsi atau lakukan tugas yang diperlukan di sini
    # Misalnya:
    # lakukan sesuatu dan dapatkan data yang ingin dikirim kembali ke JavaScript

    global ProductsJSON
    f = open(app.config["JSON_PATH"])
    ProductsJSON = json.load(f)
    items = []
    res = []
    if request.method == "POST":
        if request.files:
            image = request.files["live-camera"]
            image.save(app.config["IMAGE_UPLOAD_LOCATION"])
            print("Live Camera berhasil disimpan di 'input_image'")
            #return redirect(request.url)
            start = time.process_time()
            search = VisualSearch.VisualSearch(dataset=app.config["DATASET"])
            search.run(app.config["IMAGE_UPLOAD_LOCATION"], model=app.config["MODEL_NAME"], remove_not_white=False)
            items = search.similar_items_path()
            print("Time taken : ", time.process_time() - start)

            # Extracting Products Data
     
            for item in items[0:16]:
                itm_q = {}
                itm = item.split('.')
                itm_p = ProductsJSON[itm[0]]
                itm_q['title'] = item
                itm_q['desc'] = itm[0]
                try:
                    itm_q['rating'] = itm_p['rating']
                except:
                    itm_q['rating'] = 2
                itm_q['URL'] = itm_p['URL']
                res.append(itm_q)
                data = {'message': 'Task performed successfully'}
                return jsonify(data)

    return render_template("public/recommend.html", items = res)


if __name__ == "__main__":
    app.run(debug=True)



 



@cross_origin()
@app.route("/items", methods=["GET", "POST"])
def items():
    global ProductsJSON
    f = open(app.config["JSON_PATH"])
    ProductsJSON = json.load(f)
    if request.method == "POST":
        #img = request.get_json()
        img = request.form['img']
        img_name = img.split('.')[0]
        img_rating = ProductsJSON[img_name]['rating']
        img_url = ProductsJSON[img_name]['URL']
        img_category = ProductsJSON[img_name]['category']
        #resp = make_response(jsonify({"message": "OK"}), 200)
        img_path = os.path.join(app.config["DATASET_IMAGES_PATH"], img)
        start = time.process_time()
        search = VisualSearch.VisualSearch(dataset=app.config["DATASET"])
        search.run(img_path, model=app.config["MODEL_NAME"], remove_not_white=False)
        items = search.similar_items_path()
        print("Time taken : ", time.process_time() - start)

        # Extracting Products Data
        res = []
        for item in items[1:]:
            itm_q = {}
            itm = item.split('.')
            itm_p = ProductsJSON[itm[0]]
            itm_q['title'] = item
            itm_q['URL'] = item
            itm_q['category'] = item
            itm_q['desc'] = itm[0]
            try:
                itm_q['rating'] = itm_p['rating']
            except:
                itm_q['rating'] = 2
            # itm_q['URL'] = itm_p['URL']
            res.append(itm_q)
        #if request.headers['Content-Type'] == 'application/json':
           #return resp

    #return make_response(render_template("public/items.html", items = res))
    return render_template("public/items.html", items = res, image = img, image_name = img_name, image_rating = img_rating, image_url = img_url, category_product = img_category)
