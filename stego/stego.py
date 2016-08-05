import subprocess
import os


def encode(filepath, message):
    """ Encodes an image specified by filepath with a message in a text file """
    print 'Encoded message: '
    with open(message, 'r') as f:
        message_txt = ''.join(f.readlines())
    print message_txt
    encoded_filepath = filepath[:-4] + '_encoded' + '.jpg'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    subprocess.call([dir_path + '/embed', filepath, message, encoded_filepath])
    return encoded_filepath


def decode(filepath):
    """ Decodes an image based on the stego used in this repo """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    decoded_text = subprocess.check_output([dir_path + '/decode', filepath])[0:-1]
    print 'Decoded_text: '
    print decoded_text
    return decoded_text
