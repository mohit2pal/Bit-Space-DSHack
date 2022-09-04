from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators
from wtforms.fields.numeric import IntegerField
from wtforms.validators import Length, DataRequired





class SignUpForm(FlaskForm):
    name = StringField('Name*', validators=[DataRequired(), Length(max = 20)],render_kw={"placeholder": "Enter your full name"})
    age = StringField('Age*', validators=[DataRequired(), Length(max = 3)],render_kw={"placeholder": "Enter your age"})
    gender = StringField('Gender*',validators=[DataRequired(), Length(max = 8,min = 1)],render_kw={"placeholder": "Enter your Gender"})
    blood_group = StringField('Blood Group*', validators=[DataRequired(), Length(max = 2)] ,render_kw={"placeholder": "Enter your Blood Group"})
    height = StringField('Height*', validators=[DataRequired(), Length(max = 4)],render_kw={"placeholder": "Enter your Height in meters"})
    weight = StringField('Weight*',validators=[DataRequired(), Length(max = 3)],render_kw={"placeholder": "Enter your Weight in Kg"})
    contact = StringField('Contact info*', validators=[DataRequired(), Length(max = 10)] ,render_kw={"placeholder": "Enter your Mobile number"})
    submit = SubmitField('Submit form')