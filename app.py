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

im1             = Image.open("images/gb1.GIF")
im2             = Image.open("images/gb2.GIF")
im3             = Image.open("images/gb3.GIF")
im4             = Image.open("images/gb4.GIF")
im5             = Image.open("images/gb5.GIF")
im7             = Image.open("images/gb7.GIF")
width, height   = im1.size
rgb_im1         = im1.convert('RGB')
rgb_im2         = im2.convert('RGB')
rgb_im3         = im3.convert('RGB')
rgb_im4         = im4.convert('RGB')
rgb_im5         = im5.convert('RGB')
rgb_im7         = im7.convert('RGB')

list_gray = {}
x = 0
for i in xrange(0,width):
    for j in xrange(0,height):
        # image1
        pixel_im1   = rgb_im1.getpixel((i,j))
        red_im1     = pixel_im1[0]
        green_im1   = pixel_im1[1]
        blue_im1    = pixel_im1[2]
        gray_im1    = (red_im1 + green_im1 + blue_im1)/3

        # image2
        pixel_im2   = rgb_im2.getpixel((i,j))
        red_im2     = pixel_im2[0]
        green_im2   = pixel_im2[1]
        blue_im2    = pixel_im2[2]
        gray_im2    = (red_im2 + green_im2 + blue_im2)/3

        # image3
        pixel_im3   = rgb_im3.getpixel((i,j))
        red_im3     = pixel_im3[0]
        green_im3   = pixel_im3[1]
        blue_im3    = pixel_im3[2]
        gray_im3    = (red_im3 + green_im3 + blue_im3)/3

        # image4
        pixel_im4   = rgb_im4.getpixel((i,j))
        red_im4     = pixel_im4[0]
        green_im4   = pixel_im4[1]
        blue_im4    = pixel_im4[2]
        gray_im4    = (red_im4 + green_im4 + blue_im4)/3

        # image5
        pixel_im5   = rgb_im5.getpixel((i,j))
        red_im5     = pixel_im5[0]
        green_im5   = pixel_im5[1]
        blue_im5    = pixel_im5[2]
        gray_im5    = (red_im5 + green_im5 + blue_im5)/3

        # image7
        pixel_im7   = rgb_im7.getpixel((i,j))
        red_im7     = pixel_im7[0]
        green_im7   = pixel_im7[1]
        blue_im7    = pixel_im7[2]
        gray_im7    = (red_im7 + green_im7 + blue_im7)/3

        # list_gray[i][j] = [str(gray_im1), str(gray_im2), str(gray_im3), str(gray_im4), str(gray_im5), str(gray_im7)]
        list_gray[x] = [gray_im1, gray_im2, gray_im3, gray_im4, gray_im5, gray_im7]

        x = x + 1

        # list_gray.append(str(gray_im1), str(gray_im2), str(gray_im3), str(gray_im4), str(gray_im5), str(gray_im7))
        # print str(gray_im1), str(gray_im2), str(gray_im3), str(gray_im4), str(gray_im5), str(gray_im7)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'GET':
        return('<form action="/test" method="post"><input type="submit" value="Send" /></form>')

    elif request.method =='POST':
        cluster = request.form['cluster']
        return "jumlah cluster : " + str(cluster) + '\n' + str(list_gray[7])

    else:
        return "ok"
    # return render_template('index.html')
    # return str(gray_im1), str(gray_im2), str(gray_im3), str(gray_im4), str(gray_im5), str(gray_im7)
    
    # return render_template('result.html')

# run app
if __name__ == "__main__":
    app.run()