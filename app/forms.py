# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length, Email, NumberRange


class RegisterForm(Form):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=4, max=40)])
    passord = PasswordField('Passord', validators=[InputRequired(), Length(min=6, max=40)])
    passord_igjen = PasswordField('Passord igjen', validators=[InputRequired(),
                                                               EqualTo('passord', message='Passord felten må være lik.')])
    fornavn = StringField('Fornavn', description='Fornavn', validators=[InputRequired(), Length(min=2, max=40)])
    etternavn = StringField('Etternavn', validators=[InputRequired(), Length(min=2, max=40)])
    telefon = StringField('Telefon', validators=[InputRequired(), NumberRange(8)])


class EditForm(Form):
    email = StringField('Email')
    passord = PasswordField('Passord', validators=[InputRequired(), Length(min=6, max=40)])
    passord_igjen = PasswordField('Gjenta passord', validators=[InputRequired(),
                                                               EqualTo('passord', message='Passord felten må være lik.')])
    fornavn = StringField('Fornavn')
    etternavn = StringField('Etternavn')
    telefon = StringField('Telefon', validators=[InputRequired(), NumberRange(8)])


class LoginForm(Form):
    email = StringField('Email', validators=[Email()])
    passord = PasswordField('Passord', validators=[InputRequired()])
