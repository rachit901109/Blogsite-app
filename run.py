# set FLASK_APP=filename.py
# $env:FLASK_APP = "filename.py"
# flask run
from blogsite import app


if __name__=='__main__':
    app.run(debug=True)