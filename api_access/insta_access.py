import InstagramAPI
import requests
import urllib


# Hat tip to the following for initial Instagram API work
# https://github.com/LevPasha/Instagram-API-python (WTFPL License)
# https://github.com/mgp25/Instagram-API (MIT License)


def upload(filepath, uname, pword):
    """
    Uploads a given image to the supplied user account with the supplied password
    Image must be a jpg and square
    """
    print 'Uploading ' + filepath + '\n'
    insta = InstagramAPI.InstagramAPI(uname, pword)
    insta.uploadPhoto(filepath)


def download(uname=None, img_url=None, save_location=None):
    """
    Downloads an input img_url or the latest img from an Instagram account.
    """
    if img_url:
        print 'Downloading input img'
    elif uname:
        print 'Downloading latest img from ' + uname + '\n'
        insta_url = 'https://www.instagram.com/' + uname
        img_url = get_latest_img_url(insta_url)
    else:
        print 'Please input either a uname or img_url'
    if not save_location:
        save_location = 'download.jpg'
    if img_url and save_location:
        urllib.urlretrieve(img_url, save_location)
        return save_location


def get_latest_img_url(address):
    """
    Grabs the text of the front page for an Instagram user and finds the url for the latest image posted.
    """
    r = requests.get(address)
    p1 = '"display_src": "'
    p2 = "?"
    loc1 = r.text.find(p1)
    loc2 = loc1 + r.text[loc1:].find(p2)
    return r.text[loc1 + len(p1):loc2]
