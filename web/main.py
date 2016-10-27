# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from contextlib import closing

import sys
sys.path.append('../lib/')
from DBConsultas import DB

from flask.ext.bcrypt import Bcrypt


DEBUG = True
SECRET_KEY = 'c9d883d5-634b-477a-ab87-2fecba340e0d'

# create our little application :)
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(__name__)




@app.before_request
def before_request():
    dbName = 'consultasT'
    host = 'vanir'
    user = 'consultas'
    pwd = 'teich:i6I'

    g.mydb = DB ( dbName, host, user, pwd )    


@app.teardown_request
def teardown_request(exception):
    #db = getattr(g, 'db', None)
    #if db is not None:
    #    db.close()
    pass



@app.route('/')
def show_mainMenu():
    if not session.get('logged_in'):
        return render_template('login.html')

    return render_template('show_mainMenu.html')

# def show_entries():
#     if not session.get('logged_in'):
# 	    return render_template('login.html')

#     entries = g.mydb.getMyEntries ( session['user_id'])

#     return render_template('show_entries.html', entries=entries)


# @app.route('/add', methods=['GET', 'POST'])
# def add_entry():
#     error = None
#     if request.method == 'POST':
# 		g.db.execute('insert into entries (title, text) values (?, ?)',[request.form['title'], request.form['text']])
# 		g.db.commit()
# 		flash('New entry was successfully posted')
# 		return redirect(url_for('show_entries'))
#     return render_template('add_entries.html', error=error)


@app.route('/about')
def about ():
	return render_template('about.html')

@app.route( '/labeler', methods=['GET', 'POST'])
def start_label ():

    if not session.get('logged_in'):
     return render_template('login.html')

    
    categories = g.mydb.getCategories ()
    query = g.mydb.getConsulta ( all=False )

    if request.method == 'POST':
        import ipdb ; ipdb.set_trace()
        g.mydb.setCategoria (request.form ['query_id'], dict(request.form)['CATEGORIA'])
        query = g.mydb.getConsulta ( all=False )
        if not (query):
            flash('No more data')
            return redirect(url_for('show_mainMenu'))
    else:
        if not(query):
            flash('No more data')
            return redirect(url_for('show_mainMenu'))

    return render_template('labeler.html', id=id, query=query, categories=categories)


@app.route( '/export')
def start_export ():
    if not session.get('logged_in'):
        return render_template('login.html')
    
    categories = g.mydb.getFinalCategories ()

    allQuerys = g.mydb.getConsulta ( all=True )
    strQuerys = ",".join([str(query['idconsulta']) + query['consulta'] for query in allQuerys])

    return render_template('export.html', categories=categories, querys=strQuerys)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        hashPwd = g.mydb.getUserPwd ( request.form['username'] )        

    	if not ( bcrypt.check_password_hash( hashPwd, request.form['password']) ):
    		error = 'Invalid password or Username'
    	else:
    	    session['logged_in'] = True
    	    return redirect(url_for('show_mainMenu'))
    return render_template('login.html', error=error)




@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_mainMenu'))









if __name__ == '__main__':
	app.run(host= '0.0.0.0')


