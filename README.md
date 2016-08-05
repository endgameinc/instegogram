## Instegogram

### Overview
Using Instagram and steganography as a way to transmit images encoded with text by hiding it in prevelant social media traffic.

<br>
### Basic Use
Upload image with encoded text:
```python
import instegogram
instegogram.insta_upload(filepath='examples/piercing.jpg', uname='username', pword='password', message='examples/message.txt')
```
Download latest image and decode text:
```python
instegogram.insta_download_latest(uname='username')
```

Do both to check that it works:
```python
instegogram.insta_roundtrip(filepath='examples/piercing.jpg', uname='username', pword='password', message='examples/message.txt')
```

<br>
### Image Prep
Image prep converts an image to square (not perserving aspect ratio) with a maximum size of 1080x1080, which is Instagram's max upload size. It also re-quantizes the image with Instagram's quantization table. This requires [ImageMagic](http://www.imagemagick.org/script/index.php).
```python
from img_prep import img_prep
img_prep.prep_img(filepath='examples/piercing.jpg')
```

<br>
### Stego
The example stego technique in C is implemented and called via Python. If you have another method for encoding/decoding you can replace the `subprocess` calls in stego.py with your own.

To encode a text file into an image:
```python
from stego import stego
stego.encode(filepath='examples/piercing.jpg', message='examples/message.txt')
```
To decode text from an image:
```python
stego.deocde(filepath='download.jpg')
```

Note: Different images will have different capacities for encoding text. Try to select an image with high average texture in the luminance channel for the 8px by 8px blocks of the image. Or just trial and error until you find a good one (think lots of contrast and not computer generated)

<br>
### Instagram API
Instagram is accessed via their API and scraping their website.

To upload an image:
```python
from api_access import insta_access
insta_access.upload(filepath='examples/piercing.jpg', uname='username', pword='password')
```

To download the latest image:
```python
insta_access.download(uname='username')
```
or a specific image (found via page source or other means):
```python
insta_access.download(img_url='https://scontent-sjc2-1.cdninstagram.com/t51.2885-15/s1080x1080/e15/fr/12960199_1704537009805057_827148056_n.jpg')
```

