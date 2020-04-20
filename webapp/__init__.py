import os

from flask import Flask, render_template, request, url_for, send_file, redirect
from werkzeug.utils import secure_filename
from .pix2chocolate import render_chocolate

app = Flask(__name__)


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'GET':
       return render_template('upload.html')
   elif request.method == 'POST':
       f = request.files['file']
       sec_filename = secure_filename(f.filename)
       save_path = os.path.join(os.path.dirname(__file__), 'downloads', sec_filename)
       f.save(save_path)
       rendered_image = secure_filename(render_chocolate(save_path))
       return redirect(url_for('grab_render', requested_file=rendered_image))

@app.route('/grab-render', methods = ['GET'])
def grab_render():
    requested_file = secure_filename(request.args.get('requested_file'))
    return send_file(os.path.join('..', requested_file), mimetype='image/png', as_attachment=True)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return str(links)


if __name__ == '__main__':
   create_app().run(debug = True)
