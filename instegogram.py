import os
from time import sleep
from img_prep import img_prep
from stego import stego
from api_access import insta_access


def insta_upload(filepath, uname, pword, message=None):
    """
    Uploads a given image to the supplied user account with the supplied password.
    If a message txt file is supplied, the image will be prepped and encoded with that text before upload.
    """
    if not os.path.isfile(filepath):
        print 'Please correct img filepath'

    elif message and not os.path.isfile(message):
        print 'Please correct message filepath'

    else:
        valid_message = message and message[-3:]
        if valid_message:
            prepped_filepath = img_prep.prep_img(filepath)
            encoded_filepath = stego.encode(prepped_filepath, message)
        else:
            print 'Message pre-encoded'
            encoded_filepath = filepath
        insta_access.upload(encoded_filepath, uname, pword)


def insta_download_latest(uname):
    """ Downloads and decodes the latest image posted to a given Instagram account """
    latest_img = insta_access.download(uname)
    decoded_text = stego.decode(latest_img)
    return decoded_text


def insta_roundtrip(filepath, uname, pword, message=None):
    """
    Encoded, uploads, and downloads an image.
    Finally decodes the image and checks again the original message.
    """
    insta_upload(filepath=filepath, uname=uname, pword=pword, message=message)
    sleep(5)
    decoded_text = insta_download_latest(uname)
    if message and message[-3:] and os.path.isfile(message):
        with open(message, 'r') as f:
            message_txt = ''.join(f.readlines())
        if decoded_text == message_txt:
            print 'Successful round trip'
        else:
            print 'Round trip error'
