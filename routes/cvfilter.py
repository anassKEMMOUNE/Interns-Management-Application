from flask import Flask, render_template, request, redirect, url_for, session,Response,send_from_directory
from CVfilter.Filtering import filterAll
import os

def cvfilter_route(app) :
    @app.route('/cvfilter')
    def cvfilter():
        if "email" not in session :
            return redirect(url_for('login'))
        filtered_resumes =  []
        direct = os.path.abspath("") +'/Resumes'
        if len(direct)>0:
            keywords = session.get('keywords', [])
            filtered_resumes =  filterAll(direct,keywords)

        return render_template('cvfilter.html',files = filtered_resumes)