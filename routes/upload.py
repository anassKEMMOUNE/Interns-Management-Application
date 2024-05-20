from flask import request, redirect, url_for, session
from utils.save_files import save_files
def upload_route(app) : 
    @app.route('/upload', methods=['POST'])
    def upload():
        if "email" not in session :
            return redirect(url_for('login'))
        if 'files[]' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('files[]')

        if len(files) == 0:
            return redirect(request.url)

        try:
            save_files(files)
            keywords = request.form.getlist('keywords[]')
            session['keywords'] = keywords
            return redirect(url_for("cvfilter"))

        except Exception as e:
            return f"An error occurred: {str(e)}"