from flask import Flask, render_template, request
from PIL import Image
import json
import webbrowser
import numpy as np
np.set_printoptions(threshold=np.nan)

app = Flask(__name__, static_url_path = "/images", static_folder = "images")

# webbrowser.open("images/gb1.GIF")
# rgb_im.putpixel((i,j),(red,green,45))
# rgb_im.save('images/1.jpg')
# r, g, b   = rgb_im.getpixel((i, j))
# list_rgb[i][j]  = r, g, b
# print(list_rgb)
# g.save('images/1.jpg')
# g.show()

# im1             = Image.open("images/gb1.GIF")
# im2             = Image.open("images/gb2.GIF")
# im3             = Image.open("images/gb3.GIF")
# im4             = Image.open("images/gb4.GIF")
# im5             = Image.open("images/gb5.GIF")
# im7             = Image.open("images/gb7.GIF")
# width, height   = im1.size
# rgb_im2         = im2.convert('RGB')
# rgb_im3         = im3.convert('RGB')
# rgb_im4         = im4.convert('RGB')
# rgb_im5         = im5.convert('RGB')
# rgb_im7         = im7.convert('RGB')

w, h = 6, 1024;
list_data = [[0 for x in range(w)] for y in range(h)] 
x = 0
T = 0
sum_data = 0
isLooping = [[0 for a in range(w)] for b in range(h)] 
rgb_im = {}
im = {}
# distance = [[0 for c in range(10)] for d in range(10)]
distance = [[0 for c in range(1024)] for d in range(1024)]
list_tmp = []

# get image
for k in xrange(0,6):
    if k == 5:
        url = 'images/gb'+str(k+2)+'.GIF'
    else :
        url = 'images/gb'+str(k+1)+'.GIF'
       
    im[k]           = Image.open(url)
    rgb_im[k]       = im[k].convert('RGB')
    width, height   = im[k].size

# get pixel then enter to array
for i in xrange(0,width):
    for j in xrange(0,height):
        for k in xrange(0,6):

            pixel_im   = rgb_im[k].getpixel((i,j))
            red_im     = pixel_im[0]
            green_im   = pixel_im[1]
            blue_im    = pixel_im[2]
            gray_im    = (red_im + green_im + blue_im)/3

            list_data[x][k] = gray_im

            isLooping[x][k] = True

        x = x + 1


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'GET':
        return('<form action="/test" method="post"><input type="submit" value="Send" /></form>')

    elif request.method =='POST':
        cluster  = request.form['cluster']
        sum_data = len(list_data)
        x = 0

        # while sum_data > 3:
        for i in xrange(0,1024): #baris 1
            for j in xrange(0,1024): #baris 2
                for k in xrange(0,6): #kolom
                    # if isLooping[x][k] == True:
                        T = list_data[i][k] - list_data[j][k]
                        list_tmp.append(abs(T))

                print list_tmp
                distance[i][j] = np.array(list_tmp)
                list_tmp[:] = []
                x = x + 1

        return "jumlah cluster : " + str(cluster) + '\n' + str(distance)

    else:
        return "ok"
    # return render_template('index.html')
    # return str(gray_im1), str(gray_im2), str(gray_im3), str(gray_im4), str(gray_im5), str(gray_im7)
    
    # return render_template('result.html')

# run app
if __name__ == "__main__":
    app.run()