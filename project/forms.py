from project import app
from wtforms import Form, StringField, TextAreaField, IntegerField, validators

class MyForm(Form):
	naam = StringField('Naam', [validators.Length(min=3, max=35), validators.required()])
	straat = StringField('Straat', [validators.Length(min=3, max=35), validators.required()])
	stad = StringField('Stad', [validators.Length(min=3, max=35), validators.required()])
	postcode = IntegerField('Postcode', [validators.required()])
	phone = IntegerField('Telefoonnummer', [validators.required()])
	msg = TextAreaField('Bericht', [validators.Length(min=20, max=500), validators.required()])
