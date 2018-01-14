from project import app
from flask import render_template, request, flash, redirect, g, url_for, session

import sqlite3
import datetime

from forms import ContactForm, CreateRichtingenForm, CreateKlasForm, CreateLeraarForm, UpdateForm


"""
	ROUTES
"""
@app.route('/home')
@app.route('/')
def home():
	get_cookie()
	session_add_page('home')
	msg = get_time()
	return set_cookie(render_template('home.html', msg=msg))


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
		contactForm = ContactForm(request.form)
		if request.method == 'POST' and contactForm.validate():
			contactForm.value = [request.form.get('naam'), 
								request.form.get('straat'), 
								request.form.get('stad'), 
								request.form.get('postcode'), 
								request.form.get('phone'), 
								request.form.get('msg')]
			add_post = "INSERT INTO contact (naam,straat,stad,zip,phone,msg) VALUES (?, ?, ?, ?, ?, ? )"

			db = get_db()
			db.execute(add_post, (contactForm.value));
			db.commit()
			flash('Bedankt voor het bericht!')
	except KeyError:
		return 'error'
	return set_cookie(render_template('contact.html', form=contactForm))



@app.route('/intranet', methods=['GET', 'POST'])
@app.route('/intranet/<option>', methods=['GET', 'POST'])
def intranet(option='richtingen'):
	session_add_page('intranet')
	aanbodArray = ''
	klasArray = ''
	leraarArray = ''
	richtingForm = CreateRichtingenForm(request.form)
	klasForm = CreateKlasForm(request.form)
	leraarForm = CreateLeraarForm(request.form)
	updateForm = UpdateForm(request.form)


	#get info + set update choices
	if option == "richtingen":
		aanbodArray = get_aanbod()

		richting_ids = get_richting_id()
		updateForm.update_id.choices = richting_ids

	elif option == "klassen":
		klasArray = get_klassen()

		richting_ids = get_richting_id()
		klasForm.richting.choices = richting_ids

	elif option == "leraren":
		leraarArray = get_leraren()




	try:
		if request.method == 'POST':
			whichForm = request.form.get('button')
			formValue = []
			to_do = ""
			note = ""
			url = ""
			refresh = 0

#CRUD RICHTINGEN
			if whichForm == 'Richting Aanmaken':
				url = '/richtingen'
				if richtingForm.validate():
					formValue =	[request.form.get('naam'), 
								request.form.get('description')]
					to_do = "INSERT INTO richtingen (name,description) VALUES (?, ?)"
					note = "Richting aangemaakt!"
					refresh = 1;
					url = '/richtingen'
				else:
					note = "Not valid! Try again"

			elif whichForm == 'Update Richting':
				if richtingForm.validate():
					formValue =	[request.form.get('naam'), 
								request.form.get('description'),
								request.form.get('update_id')]
					to_do = "UPDATE richtingen SET name = ?, description = ? where richting_id = ?"
					note = "Richting geupdate!"
					refresh = 1;
					url = '/richtingen'
				else:
					note = "Not valid! Try again"

			elif whichForm == 'Delete Richting':
				formValue = [request.form.get('delete-id')]
				to_do = "DELETE FROM richtingen WHERE richting_id = ?"
				note = "Richting gedelete!"
				refresh = 1;
				url = '/richtingen'

#CRUD KLASSEN
			elif whichForm == 'Klas Aanmaken':
					formValue =	[request.form.get('jaar'), 
								request.form.get('richting')]
					to_do = "INSERT INTO klassen (jaar,richting_id) VALUES (?, ?)"
					note = "Klas aangemaakt!"
					refresh = 1;
					url = '/klassen'
			elif whichForm == 'Update Klas': 
				formValue = []
				to_do = ""
				note = "Klas geupdate!"
				refresh = 1;
				url = '/klassen'

			elif whichForm == 'Delete Klas':
				formValue = [request.form.get('delete-id')]
				to_do = "DELETE FROM klassen WHERE klas_id = ?"
				note = "Klas gedelete!"
				refresh = 1;
				url = '/klassen'

#CRUD LERAAR
			if whichForm == 'Leraar Aanmaken':
				url = '/leraren'
				if leraarForm.validate():
					formValue =	[request.form.get('voornaam'), 
								request.form.get('achternaam'),
								request.form.get('email'),
								request.form.get('vakken')]
					to_do = "INSERT INTO leraren (voornaam,naam,email,vakken) VALUES (?, ?, ?, ?)"
					note = "Leraar aangemaakt!"
					refresh = 1;					
				else:
					note = "Not valid! Try again"

			elif whichForm == 'Update Leraar':
				formValue = []
				to_do = ""
				note = "Leraar geupdate!"
				refresh = 1;
				url = '/leraren'

			elif whichForm == 'Delete Leraar':
				formValue = [request.form.get('delete-id')]
				to_do = "DELETE FROM leraren WHERE leraar_id = ?"
				note = "Leraar gedelete!"
				refresh = 1;
				url = '/leraren'


#COMMIT TO DB
			db = get_db()
			db.execute(to_do, (formValue));
			db.commit()
			flash(note)

			#fix this: only refresh if succesfully through validator, otherwise validate errors aren't shown
			return redirect(url_for('intranet') + url)
	except KeyError:
		return 'error'

	return set_cookie(render_template('intranet.html', option=option, leraarArray=leraarArray, aanbodArray=aanbodArray, klasArray=klasArray, leraarForm=leraarForm, richtingForm=richtingForm, klasForm=klasForm, updateForm=updateForm))



"""
	DATABASE CONNECTION
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
		page_list = page_list[-10:] # only last 10 pages into session, : to avoid error if empty
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
	pages = ""
	for page in session['page']:
		pages += page + ", "
	flash("Uw 10 laatst bekenen pagina's zijn: ")
	flash(pages)
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
	klassen = db.execute('SELECT klassen.klas_id, klassen.jaar, richtingen.name FROM klassen INNER JOIN richtingen ON klassen.richting_id = richtingen.richting_id')
	db.commit()
	klasArray = []
	for row in klassen:
		klasArray.append( row )
	return klasArray

def get_richting_id():
	db = get_db()
	id_ = db.execute('SELECT richting_id, name FROM richtingen')
	db.commit()
	ids = []
	for row in id_:
		ids.append( row )
	return ids

def get_klas_id():
	db = get_db()
	id_ = db.execute('SELECT klas_id, name FROM klassen')
	db.commit()
	ids = []
	for row in id_:
		ids.append( row )
	return ids

def get_leraar_id():
	db = get_db()
	id_ = db.execute('SELECT leraren_id, name FROM leraren')
	db.commit()
	ids = []
	for row in id_:
		ids.append( row )
	return ids




"""
	OTHER FUNCTIONS
"""
def get_time():
	now = datetime.datetime.now()
	msg = ""
	if now.hour > 0:
		msg = "goede nacht"
	if now.hour > 6:
		msg = "goede morgen"
	if now.hour > 12:
		msg = "goede middag"
	if now.hour > 18:
		msg = "goede avond"
	return msg