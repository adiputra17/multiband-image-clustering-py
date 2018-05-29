from flask import Flask, render_template, request
from PIL import Image
import json
import webbrowser
import numpy as np
import math
import copy

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
x = 0
sum_data = 0
# is_looping = [[0 for c in range(h)] for d in range(h)]
is_looping = {}
rgb_im = {}
im = {}
# distance = [[0 for c in range(10)] for d in range(10)]
data_matriks = [[0 for c in range(h)] for d in range(h)]

# get image
for k in xrange(0,6):
    if k == 5:
        url = 'images/gb'+str(k+2)+'.GIF'
    else :
        url = 'images/gb'+str(k+1)+'.GIF'
       
    im[k]           = Image.open(url)
    rgb_im[k]       = im[k].convert('RGB')
    width, height   = im[k].size

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'GET':
        return('<form action="/test" method="post"><input type="submit" value="Send" /></form>')

    elif request.method =='POST':
        cluster   = request.form['cluster']
        w, h = 6, 1024;
        list_data = [[0 for x in range(w)] for y in range(h)]  #list_data[[6]1024]
        x         = 0
        T         = 0
        list_tmp  = []
        sum_list_tmp = 0
        hash_tmp  = []

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

                is_looping[x] = True
                x = x + 1

        # print str(list_data[1023][1])
        # fill_array_is_looping(is_looping)

        while len(list_data) > int(cluster):
            min_value = 9999.0
            index1, index2, T, i, j, k = 0, 0, 0, 0, 0, 0
            for i in xrange(0,1024): #baris 1
                for j in xrange(0,1024): #baris 2
                    if is_looping[i] == True and is_looping[j] == True:
                        for k in xrange(0,6): #kolom
                            # print(str(i)+"-"+str(j))
                            # if list_data[i][k] != [] and list_data[j][k] != []:
                            # print str(list_data[i])+'-'+str(list_data[j])
                            T = list_data[i][k] - list_data[j][k]
                            
                            sum_list_tmp += math.pow(abs(T),2)

                        data_matriks[i][j] = math.sqrt(sum_list_tmp)

                        if i !=j and data_matriks[i][j] > 0.0:
                            if data_matriks[i][j] < min_value:
                                min_value = data_matriks[i][j]
                                index1 = i
                                index2 = j

                        # empty value
                        sum_list_tmp = 0

            # print str(min_value)
            if min_value != 9999.0:
                print 'DATA MINIMAL : '+str(index1)+' : '+str(index2)+' : '+str(min_value) 

                is_looping[index2] = False
                
                for h in xrange(0,6):
                    hash_tmp.append((int(list_data[index1][h]) + int(list_data[index2][h]))/2)

                print 'NEW DATA : '+str(hash_tmp)
                list_data[index1] = copy.copy(hash_tmp)
                hash_tmp[:]       = []
                
            else:
                return True

        return False

        return 'jumlah cluster : '+str(cluster)+'<br>'+'JUMLAH DATA : '+str(len(list_data))
        # show_data_cluster()


    else:
        return "ok"
    # return render_template('index.html')
    # return str(gray_im1), str(gray_im2), str(gray_im3), str(gray_im4), str(gray_im5), str(gray_im7)
    
    # return render_template('result.html')

def fill_array_is_looping(is_looping):
    for i in xrange(0,1024):
        for j in xrange(0,1024):
            is_looping[i][j] = True

def show_data_cluster():
    return 

# run app
if __name__ == "__main__":
    app.run()