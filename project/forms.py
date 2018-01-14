from project import app
from wtforms import Form, StringField, TextAreaField, IntegerField, validators, SelectField
from wtforms.fields.html5 import EmailField

class ContactForm(Form):
	naam = StringField('Naam', [validators.Length(min=5, max=35), validators.required()])
	straat = StringField('Straat', [validators.Length(min=3, max=35), validators.required()])
	stad = StringField('Stad', [validators.Length(min=3, max=35), validators.required()])
	postcode = IntegerField('Postcode', [validators.required()])
	phone = IntegerField('Telefoonnummer', [validators.required()])
	msg = TextAreaField('Bericht', [validators.Length(min=10, max=500), validators.required()])


class CreateRichtingenForm(Form):
	naam = StringField('Naam', [validators.Length(min=5, max=35), validators.required()])
	description = TextAreaField('Beschrijving', [validators.Length(min=10, max=500), validators.required()])

class CreateKlasForm(Form):
	jaar = SelectField(u'Jaar', choices=[('1', '1e jaars'), ('2', '2e jaars'), ('3', '3e jaars'), ('3', '3e jaars'), ('4', '4e jaars'), ('5', '5e jaars'), ('6', '6e jaars')])
	richting = SelectField(u'Richting', choices=[], coerce=int)

class CreateLeraarForm(Form):
	voornaam = StringField('Voornaam', [validators.Length(min=3, max=35), validators.required()])
	achternaam = StringField('Achternaam', [validators.Length(min=3, max=35), validators.required()])
	email = EmailField('Email addres', [validators.Email(), validators.DataRequired()])
	vakken = StringField('Vakken', [validators.Length(min=3, max=35), validators.required()])


class UpdateForm(Form):
	update_id = SelectField(u'Richting', choices=[], coerce=int)