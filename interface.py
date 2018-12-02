import sys
import os
from img_to_vec import Img2Vec
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import pickle
import os.path
import json
from pprint import pprint
import requests
import flask
from io import BytesIO
from operator import itemgetter
from flask import Flask, request, redirect, url_for
from server_startup import startup
from flask_cors import CORS


img2vec = Img2Vec()
UPLOAD_FOLDER = 'query'
ALLOWED_EXTENSIONS = set(['jpg'])
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# The Deep Learning part that returns a list of clothing with their info
male_list_of_clothing_info, female_list_of_clothing_info = startup()

# Checks to see if the user uploaded a jpg
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# A route to return all of the available entries in our catalog.
@app.route('/query/<gender>', methods=['GET', 'POST'])
def upload_file(gender):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "query_image.jpg"))

            # Go through each of the clothing vectors in the database
            # and compare the cosine similarity of it to the query image vector.
            # For now, it compares it to the male clothing
            list_of_clothing_info_with_similarity = []
            query_img = Image.open("query/query_image.jpg")
            query_vec = img2vec.get_vec(query_img);

            if gender == "M":
                list_of_clothing_info = male_list_of_clothing_info
            elif gender == "F":
                list_of_clothing_info = female_list_of_clothing_info
            else:
                list_of_clothing_info = male_list_of_clothing_info + female_list_of_clothing_info

            print(list_of_clothing_info)
            for clothing in tqdm(list_of_clothing_info):
                element = clothing.copy()
                element["similarity"] = cosine_similarity(query_vec.reshape((1, -1)), element["feature_vec"].reshape((1, -1)))[0][0]
                element.pop('feature_vec', None)
                list_of_clothing_info_with_similarity.append(element)


            sorted_list = sorted(list_of_clothing_info_with_similarity, key=itemgetter('similarity'), reverse=True)
            for i in sorted_list:
                i.pop('similarity',None)
            
            json_results = {}
            json_results["results"] = sorted_list
            return flask.jsonify(**json_results)
    else:
        return "THIS IS A GET REQUEST"


if __name__ == '__main__':
    app.run(debug=True)

