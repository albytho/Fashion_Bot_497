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
from io import BytesIO
from operator import itemgetter

print("What gender of clothing are you looking for?  Male, female, or does it not matter? (M/F/NA):")
gender = input().capitalize()

img2vec = Img2Vec()
json_path = 'json'
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

    male_json_path = json_path+"/men"
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

    female_json_path = json_path+"/women"
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

# Go through each of the clothing vectors in the database
# and compare the cosine similarity of it to the query image vector.
# For now, it compares it to the male clothing
list_of_clothing_info_with_similarity = []
query_file = "query/query_image.jpg"
query_img = Image.open(query_file)
query_vec = img2vec.get_vec(query_img);

if gender == "M":
    list_of_clothing_info = male_list_of_clothing_info
elif gender == "F":
    list_of_clothing_info = female_list_of_clothing_info
else:
    list_of_clothing_info = male_list_of_clothing_info + female_list_of_clothing_info

for clothing in tqdm(list_of_clothing_info):
    element = clothing
    element["similarity"] = cosine_similarity(query_vec.reshape((1, -1)), element["feature_vec"].reshape((1, -1)))[0][0]
    element.pop('feature_vec', None)
    list_of_clothing_info_with_similarity.append(element)


sorted_list = sorted(list_of_clothing_info_with_similarity, key=itemgetter('similarity'), reverse=True)
index = 0
for i in sorted_list:
    pprint(i)
    index = index + 1
    if index == 10:
        break

