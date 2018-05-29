# python3

from flask import Flask, render_template, request
from PIL import Image
from sklearn import cluster as sk_cluster
import numpy as np
import random
import datetime

np.set_printoptions(threshold=np.nan)

app = Flask(__name__, static_url_path = "/images", static_folder = "images")

w, h = 6, 1024;
x = 0
sum_data = 0
is_looping = {}
rgb_im = {}
im = {}
list_data = [[0 for x in range(w)] for y in range(h)]  #list_data[[6]1024]

colors  = ["red","green","blue","orange","purple","pink","yellow"]

for k in range(0,6):
    if k == 5:
        url = 'images/gb'+str(k+2)+'.GIF'
    else :
        url = 'images/gb'+str(k+1)+'.GIF'
       
    im[k]           = Image.open(url)
    rgb_im[k]       = im[k].convert('RGB')
    width, height   = im[k].size

# get pixel change to grayscale then enter to array
for i in range(0,width):
    for j in range(0,height):
        for k in range(0,6):
            pixel_im   = rgb_im[k].getpixel((i,j))
            red_im     = pixel_im[0]
            green_im   = pixel_im[1]
            blue_im    = pixel_im[2]
            gray_im    = (red_im + green_im + blue_im)/3

            list_data[x][k] = gray_im

        is_looping[x] = True
        x = x + 1

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method =='POST':
        cluster     = request.form['cluster']
        cluster_tmp = []
        x = 0

        result = sk_cluster.AgglomerativeClustering(n_clusters=int(cluster),linkage='complete').fit_predict(list_data)

        print(result)

        # for x in range(0,width*height):
        #     for y in range(0,int(cluster)):
        #         if result[x] == y:
        #             cluster_tmp.append([])
        #             cluster_tmp[y].append(x)

        # for x in range(0,int(cluster)):
        #     print('Cluser '+str(x)+' : '+str(cluster_tmp[x]))

        # make image
        img = Image.new('RGB', [32,32], 0x000000)
        # loop = 0
        for i in range(0,width):
            for j in range(0,height):
                if result[x] == 0:
                    img.putpixel((i,j),(255,0,0))
                elif result[x] == 1:
                    img.putpixel((i,j),(0,255,0))
                elif result[x] == 2:
                    img.putpixel((i,j),(0,0,255))
                elif result[x] == 3:
                    img.putpixel((i,j),(255,255,0))
                elif result[x] == 4:
                    img.putpixel((i,j),(255,0,255))
                elif result[x] == 5:
                    img.putpixel((i,j),(0,255,255))
                elif result[x] == 6:
                    img.putpixel((i,j),(0,0,0))
                else:
                    img.putpixel((i,j),(255,255,255))

                x += 1

        now = datetime.datetime.now()
        img.save('images/'+str(now)+'.jpg')
        # img.show()
        url_image = str(now)+'.jpg'

        return render_template('hasil.html', cluster=cluster, url_image=url_image)

    else:
        return "ok"

# run app
if __name__ == "__main__":
    app.run()