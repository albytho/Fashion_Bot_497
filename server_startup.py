import sys
import os
from img_to_vec import Img2Vec
from PIL import Image
from tqdm import tqdm
import pickle
import os.path
import json
from pprint import pprint
import requests
from io import BytesIO
from operator import itemgetter
from flask import Flask, request, redirect, url_for

def startup():
    img2vec = Img2Vec()
    male_list_of_clothing_info = []
    female_list_of_clothing_info = []

    # Check to see if we have already generated the feature vectors
    # of our database images for men's clothing
    male_vectors_generated = True
    if os.path.isfile("male_list_of_clothing_info.pkl") == False:
        male_vectors_generated = False

    # Check to see if we have already generated the feature vectors
    # of our database images for women's clothing
    female_vectors_generated = True
    if os.path.isfile("female_list_of_clothing_info.pkl") == False:
        female_vectors_generated = False

    # If we have not generated the feature vectors yet for male clothing,
    # we need to go through and create them and store them
    if male_vectors_generated == False:
        print("Calculating feature vectors of male clothing")

        male_json_path = "json/men"
        for file in tqdm(os.listdir(male_json_path)):
            if file == ".DS_Store":
                continue;
            
            file_path = male_json_path+"/"+file
            with open(file_path) as f:
                data = json.load(f)

                male_list_of_clothing_info = []
                for i in tqdm(data):
                    response = requests.get(i["images"])
                    img = Image.open(BytesIO(response.content))
                    feature_vec = img2vec.get_vec(img)
                    i["feature_vec"] = feature_vec
                    male_list_of_clothing_info.append(i)

        output = open('male_list_of_clothing_info.pkl', 'wb')
        pickle.dump(male_list_of_clothing_info,output)
        output.close()
                
    else:
        pkl_file = open('male_list_of_clothing_info.pkl', 'rb')
        male_list_of_clothing_info = pickle.load(pkl_file)
        pkl_file.close()


    # If we have not generated the feature vectors yet for female clothing,
    # we need to go through and create them and store them
    if female_vectors_generated == False:
        print("Calculating feature vectors of female clothing")

        female_json_path = "json/women"
        for file in tqdm(os.listdir(female_json_path)):
            if file == ".DS_Store":
                continue;
            
            file_path = female_json_path+"/"+file
            with open(file_path) as f:
                data = json.load(f)

                female_list_of_clothing_info = []
                for i in tqdm(data):
                    response = requests.get(i["images"])
                    img = Image.open(BytesIO(response.content))
                    feature_vec = img2vec.get_vec(img)
                    i["feature_vec"] = feature_vec
                    female_list_of_clothing_info.append(i)

        output = open('female_list_of_clothing_info.pkl', 'wb')
        pickle.dump(female_list_of_clothing_info,output)
        output.close()
                
    else:
        pkl_file = open('female_list_of_clothing_info.pkl', 'rb')
        female_list_of_clothing_info = pickle.load(pkl_file)
        pkl_file.close()

    return male_list_of_clothing_info, female_list_of_clothing_info