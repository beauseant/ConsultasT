
# all the imports
import sqlite3
from flask import Flask, request, session, make_response, g, redirect, url_for, \
     abort, render_template, flash

from contextlib import closing

import sys
sys.path.append('../lib/')
from DBConsultas import DB

#sudo /opt/anaconda/bin/pip install flask-bcrypt
from flask.ext.bcrypt import Bcrypt

import ConfigParser
import argparse



DEBUG = True
SECRET_KEY = 'c9d883d5-634b-477a-ab87-2fecba340e0d'

# create our little application :)
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(__name__)




@app.before_request
def before_request():

    config = ConfigParser.ConfigParser()
    config.read('consultas.cfg')


    g.mydb = DB (dbName=config.get('DB','dbname'), host=config.get('DB','host'), user=config.get('DB','user'), pwd=config.get('DB','pwd'))


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

    numquerys = g.mydb.getNumQuerys ( etiquetadas = False)
    etiquetadas = g.mydb.getNumQuerys ( etiquetadas = True )

    return render_template('show_mainMenu.html', etiquetadas=etiquetadas, numquerys=numquerys)


@app.route('/about')
def about ():
	return render_template('about.html')

@app.route( '/labeler', methods=['GET', 'POST'])
def start_label ():

    if not session.get('logged_in'):
     return render_template('login.html')

    
    categories = g.mydb.getCategories ()
    sortedList = sorted(categories)
    query = g.mydb.getConsulta ( all=False )
    numquerys = g.mydb.getNumQuerys ( etiquetadas = False)
    etiquetadas = g.mydb.getNumQuerys ( etiquetadas = True )

    if request.method == 'POST':

        dictOptions = dict(request.form)

        queryid =  dictOptions.pop ('query_id')[0]

        cats = [v for k,v in dictOptions.iteritems() ]

        g.mydb.setCategoria ( queryid, cats)
        query = g.mydb.getConsulta ( all=False )
        etiquetadas = g.mydb.getNumQuerys ( etiquetadas = True )
        if not (query):
            flash('No more data, all queries done')
            return redirect(url_for('show_mainMenu'))
    else:
        if not(query):
            flash('No more data, all queries done')
            return redirect(url_for('show_mainMenu'))

    return render_template('labeler.html', id=id, query=query, categories=categories, sortedList=sortedList, numquerys=numquerys, etiquetadas=etiquetadas)



@app.route( '/export')
def start_export ():
    if not session.get('logged_in'):
        return render_template('login.html')
    
    categories = g.mydb.getFinalCategories ()

    allQuerys = g.mydb.getConsulta ( all=True )
    strCategories = "," +",".join([str(query['catid']) + '_' +query['categoria'] for query in categories])

    csv = 'no, hay, suficientes, datos'

    numCats = g.mydb.getNumCats ()
    cad = ''
    for query in allQuerys:
        cad = cad +  str(query['idconsulta']) + '_' + query['consulta'] + ','
        listzeros=[0] * numCats        
        #en caso de no tener categorias da un error, lo ignoramos 
        #y no ponemos 1 en ninguna:
        for cat in query['categorias']:            
            listzeros[int(cat[0])] = 1

        cad = cad + ','.join(str(e) for e in listzeros)
        cad = cad + '\n'

        csv = strCategories + '\n' + cad


    # We need to modify the response, so the first thing we 
    # need to do is create a response out of the CSV string
    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=Output.csv"
    return response    


@app.route( '/show', methods=['GET', 'POST'])
def start_show ():
    if not session.get('logged_in'):
        return render_template('login.html')

    if request.method == 'POST':
        dictOptions = dict(request.form)
        g.mydb.delConsultas ( dictOptions['borrar'] )
        flash(str(len(dictOptions['borrar'])) + ' entradas borradas...'  )


    entries  = g.mydb.getConsulta ( all=True )
    dictCats = g.mydb.getDictCats ()

    return render_template('show_entries.html', entries=entries, dictCats=dictCats)    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        hashPwd = g.mydb.getUserPwd ( request.form['username'] )        

    	if (not hashPwd) or (not ( bcrypt.check_password_hash( hashPwd, request.form['password']) )):
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

    parser = argparse.ArgumentParser(description='consultas')
    parser.add_argument('--addUser', help='add user to the App', action='store_true')
    parser.add_argument('--name', help='the user name to add if --addUser')
    parser.add_argument('--pwd', help='the user name to add if --addUser')

    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.read('consultas.cfg')


    if args.addUser:
        consultas =  DB (dbName=config.get('DB','dbname'), host=config.get('DB','host'), user=config.get('DB','user'), pwd=config.get('DB','pwd'))
        pw_hash = bcrypt.generate_password_hash( args.pwd )
        consultas.createUser (args.name, pw_hash )
        print 'usuario creado o actualizado'
    else:

        app.run(host= config.get('APP','host'), port= int(config.get('APP','port')))