from flask import Blueprint, render_template

errors = Blueprint(name="errors", import_name=__name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/error_404.html',page_title='404'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/error_403.html',page_title='403'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/error_500.html',page_title='500'), 500
