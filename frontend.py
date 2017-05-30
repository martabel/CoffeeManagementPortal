from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

import sys
from bson.json_util import dumps

from forms import SignupForm
from nav import nav
import database as db

frontend = Blueprint('frontend', __name__)

nav.register_element('frontend_top', Navbar(
    View('Coffee', '.index'),
    View('Home', '.index'),
    View('Downloads', '.downloads'),
    Subgroup(
        'Management',
        View('Benutzer', '.index'),
        View('Einstellungen', '.index')
    )))

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/downloads')
def downloads():
    #get url params
    dListId = None
    cListId = None
    try:
        dListId = request.args.get('dListId', '')
    except KeyError as e:
        dListId = None
        pass
    try:
        cListId = request.args.get('cListId', '')
    except KeyError as e:
        cListId = None
        pass
    #prepair data
    dList = None
    dLists = db.getDrinkerLists()
    cList = None
    cLists = db.getCoffeeLists()

    if cListId == None or cListId == '':
        #No Id given, get first list
        cList = db.getCoffeeListbyId(str(cLists[0]['_id']))
    else:
        try:
            #Id is given, get list
            cList = db.getCoffeeListbyId(cListId)
            if cList == None:
                #no list found, get first list
                cList = db.getCoffeeListbyId(str(cLists[0]['_id']))
                flash("Keine Kaffeeliste zur ID gefunden!")
        except Exception as e:
            flash("Keine Kaffeeliste zur ID gefunden!")
    if dListId == None or dListId == '':
        #No Id given, get first list
        dList = db.getDrinkerListbyId(str(dLists[0]['_id']))
    else:
        try:
            #Id is given, get list
            dList = db.getDrinkerListbyId(dListId)
            if cList == None:
                #no list found, get first list
                dList = db.getDrinkerListbyId(str(dLists[0]['_id']))
                flash("Keine Trinkerliste zur ID gefunden!")
        except Exception as e:
            flash("Keine Trinkerliste zur ID gefunden!")
    #render template with prepaired data
    return render_template('downloads.html', dList=dList, cList=cList, dLists=dLists, cLists=cLists)

# Shows a long signup form, demonstrating form rendering.
@frontend.route('/example-form/', methods=('GET', 'POST'))
def example_form():
    form = SignupForm()

    if form.validate_on_submit():
        # We don't have anything fancy in our application, so we are just
        # flashing a message when a user completes the form successfully.
        #
        # Note that the default flashed messages rendering allows HTML, so
        # we need to escape things if we input user values:
        flash('Hello, {}. You have successfully signed up'
              .format(escape(form.name.data)))

        # In a real application, you may wish to avoid this tedious redirect.
        return redirect(url_for('.index'))

    return render_template('signup.html', form=form)
