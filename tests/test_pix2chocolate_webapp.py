from filecmp import cmp
from io import BytesIO
import os
import re
import tempfile
import urllib.parse as parse

import PIL.Image


FILE_TO_SEND = 'LaBonneImpressionLogoHeightmap.svg'
DOWNLOADS_DIR = 'webapp/downloads'
RENDER_FILE_TO_RECEIVE = 'expected_render_test0001.png'

def get_images_difference_percent(filename1, filename2):
    # From https://rosettacode.org/wiki/Percentage_difference_between_images
    # Return: value between 0 and 100
    i1 = PIL.Image.open(filename1)
    i2 = PIL.Image.open(filename2)
    #assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."

    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = i1.size[0] * i1.size[1] * 3

    return (dif / 255.0 * 100.0) / ncomponents

def test_page_display(client):
    rv = client.get('/uploader')
    assert rv.status_code == 200

def test_file_upload(client):

    with open(FILE_TO_SEND, 'rb') as fb:
        svg = fb.read()
        data = {
            'field': 'file',
            'file': (BytesIO(svg), FILE_TO_SEND)
        }

        # We are expecting a POST/REDIRECT/GET pattern
        rv = client.post('/uploader', buffered=True,
                         content_type='multipart/form-data',
                         data=data)
        uploaded_received_svg = os.path.join(DOWNLOADS_DIR, FILE_TO_SEND)
        # checking server-side stored file
        assert cmp(FILE_TO_SEND, uploaded_received_svg)
        os.unlink(uploaded_received_svg)

        # checking proper redirection for file download
        assert rv.status_code == 302
        redirected_url = rv.headers.get('location')

        assert 'grab-render' in redirected_url
        rv = client.get(redirected_url)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as received_data_file:
            received_data_file.write(rv.data)
            assert get_images_difference_percent(received_data_file.name, RENDER_FILE_TO_RECEIVE) < 20 

        # checking proper page template with render image tag
        parsed_redirected_url = parse.urlparse(redirected_url)
        path_and_query = '{}?{}'.format(parsed_redirected_url.path, parsed_redirected_url.query) 
        parsed_query = parse.parse_qs(parsed_redirected_url.query)
        assert 'requested_file' in parsed_query
        requested_file = parsed_query['requested_file'][0]
        rv = client.get('/show-render?requested_file=' + requested_file)
        assert 'src="{}"'.format(path_and_query) in rv.data.decode('utf-8')
