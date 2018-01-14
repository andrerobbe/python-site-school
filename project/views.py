from project import app
from flask import render_template, request, flash, redirect, g, url_for, session

import sqlite3
from forms import MyForm


"""
	ROUTES
"""
@app.route('/home')
@app.route('/')
def home():
	get_cookie()
	session_add_page('home')
	return set_cookie(render_template('home.html'))


@app.route('/aanbod')
def aanbod():
	session_add_page('aanbod')
	aanbodArray = get_aanbod()
	return set_cookie(render_template('aanbod.html', aanbodArray=aanbodArray))


@app.route('/wie-is-wie')
def wie():
	session_add_page('wie-is-wie')
	leraarArray = get_leraren()
	return set_cookie(render_template('wie.html', leraarArray=leraarArray))



@app.route('/contact', methods=['GET', 'POST'])
def contact():
	session_add_page('contact')
	try:
		form = MyForm(request.form)
		if request.method == 'POST' and form.validate():
			form.value = 	[request.form.get('naam'), 
							request.form.get('straat'), 
							request.form.get('stad'), 
							request.form.get('postcode'), 
							request.form.get('phone'), 
							request.form.get('msg')]
			add_post = "INSERT INTO contact (naam,straat,stad,zip,phone,msg) VALUES (?, ?, ?, ?, ?, ? )"

			db = get_db()
			db.execute(add_post, (form.value));
			db.commit()
			flash('Bedankt voor het bericht!')
	except KeyError:
		return 'error'
	return set_cookie(render_template('contact.html', form=form))



@app.route('/intranet', methods=['GET', 'POST'])
@app.route('/intranet/<option>', methods=['GET', 'POST'])
def intranet(option='Richtingen'):
	session_add_page('intranet')
	leraarArray = get_leraren()
	aanbodArray = get_aanbod()
	klasArray = get_klassen()

	try:
		form = MyForm(request.form)
		if request.method == 'POST': #AND FORM.VALIDATE() IS EEN PROBLEEEM?????
			whichForm = request.form.get('button')

			to_do = ""
			note = ""
			form.value = []

			if whichForm == 'Aanmaken':
				form.value =	[request.form.get('naam'), 
								request.form.get('description')]
				to_do = "INSERT INTO richtingen (name,description) VALUES (?, ?)"
				note = "Richting aangemaakt!"

			if whichForm == 'Delete':
				form.value = [request.form.get('delete-id')]
				to_do = "DELETE FROM richtingen WHERE richting_id = ?"
				note = "Richting gedelete!"
				print form.value

			if whichForm == 'Update':
				print "update"
				return

			db = get_db()
			db.execute(to_do, (form.value));
			db.commit()
			flash(note)
	except KeyError:
		return 'error'

	return set_cookie(render_template('intranet.html', option=option, leraarArray=leraarArray, aanbodArray=aanbodArray, klasArray=klasArray, form=form))



"""
	DATABASE
"""
def connect_db():
	db = sqlite3.connect('school.db')
	return db

def get_db():
    #Opens a new database connection if there is none yet for the current application context.
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db



"""
	COOKIES & SESSIONS
"""
def set_cookie(link=None):
	url = link
	response = app.make_response(url)
	response.set_cookie('Atheneum Antwerpen', value='visited')
	return response

def get_cookie():
	if(request.cookies.get('Atheneum Antwerpen')):
		flash('Leuk om u weer terug te zien!')
	return

@app.route('/delete_cookie')
def delete_cookie():
	response = app.make_response(redirect(url_for('home')))
	response.set_cookie('Atheneum Antwerpen', value='visited', expires=0)
	return response



def session_add_page(currentPage=None):
	if 'page' in session.keys():
		page_list = session['page']
		page_list.append(currentPage)
		session['page'] = page_list
	else:	
		session['page'] = [currentPage]
	return

@app.route('/session_reset')
def session_reset():
    session.pop('page', None)
    flash("Uw sessie is gereset")
    return redirect('/delete_cookie')

@app.route('/session_show')
def session_show():
	flash("Uw laatst bekenen pagina's zijn: ")
	flash(str(session['page']))
	return redirect(url_for('home'))


"""
	GET DB INFO
"""
def get_leraren():
	db = get_db()
	leraren = db.execute('SELECT * FROM leraren')
	db.commit()
	leraarArray = []
	for row in leraren:
		leraarArray.append( row )
	return leraarArray

def get_aanbod():
	db = get_db()
	aanbod = db.execute('SELECT * FROM richtingen')
	db.commit()
	aanbodArray = []
	for row in aanbod:
		aanbodArray.append( row )
	return aanbodArray

def get_klassen():
	db = get_db()
	klassen = db.execute('SELECT klassen.jaar, richtingen.name FROM klassen INNER JOIN richtingen ON klassen.richting_id = richtingen.richting_id')
	db.commit()
	klasArray = []
	for row in klassen:
		klasArray.append( row )
	return klasArray