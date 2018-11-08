import sys
import os
from img_to_vec import Img2Vec
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import pickle
import os.path

img2vec = Img2Vec()
input_path = 'database'
pics = {}

# Check to see if we have already generated the feature vectors
# of our database images
vectors_generated = True
if os.path.isfile("variables.pkl") == False:
    vectors_generated = False

# If we have not generated the feature vectors yet,
# we need to go through and create them and store them
if vectors_generated == False:
    for file in tqdm(os.listdir(input_path)):
        if file == ".DS_Store":
            continue;

        filename = os.fsdecode(file)
        img = Image.open(os.path.join(input_path, filename))
        vec = img2vec.get_vec(img)
        pics[filename] = vec
    
    output = open('variables.pkl', 'wb')
    pickle.dump(pics, output)
    output.close()
else:
    pkl_file = open('variables.pkl', 'rb')
    pics = pickle.load(pkl_file)
    pkl_file.close()


sims = {}
query_file = "query/query_image.jpg"
query_img = Image.open(query_file)
query_vec = img2vec.get_vec(query_img);
for key in list(pics.keys()):
    sims[key] = cosine_similarity(query_vec.reshape((1, -1)), pics[key].reshape((1, -1)))[0][0]

d_view = [(v, k) for k, v in sims.items()]
d_view.sort(reverse=True)
index = 0
for v, k in d_view:
    if index == 10:
        break
    print(v, k)
    index = index + 1