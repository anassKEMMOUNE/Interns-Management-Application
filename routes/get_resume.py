from flask import render_template, redirect, url_for, session,send_from_directory


def get_resume_route(app) :
    @app.route('/resumes/<path:filename>')
    def get_resume(filename):
        if "email" not in session:
            return redirect(url_for('login'))
        return send_from_directory('Resumes', filename)