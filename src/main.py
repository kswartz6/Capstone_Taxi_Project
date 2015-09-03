import os
import sys
import logging
import json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, session

webapp = Flask(__name__)
@webapp.route("/")
def root():
	return render_template('index.html')
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    webapp.run(host='0.0.0.0', port=port)


