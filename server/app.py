from io import BytesIO

from celery.result import AsyncResult
from flask import Flask, render_template, send_file, jsonify, request

from server.tasks import convert_blog, CELERY

app = Flask(__name__, static_url_path='/static')


@app.route('/convert', methods=['POST'])
def convert():
    blog = request.files['blog']
    result = convert_blog.delay(blog.read())
    return result.id


@app.route('/converted/<blog_id>/status')
def status(blog_id):
    return jsonify({
        'blog_id': blog_id,
        'status': AsyncResult(blog_id, app=CELERY).state,
        'download': '/converted/{}/download'.format(blog_id)
    })


@app.route('/converted/<blog_id>/download')
def download(blog_id):
    result = AsyncResult(blog_id, app=CELERY)
    if result.state == 'SUCCESS':
        return send_file(BytesIO(result.result), as_attachment=True,
                         attachment_filename='blog.pdf',
                         mimetype='application/pdf')
    return 'Processing', 204


@app.route("/")
def index():
    return render_template('index.html', var='X')
