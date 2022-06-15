from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, RadioField, FileField, BooleanField
from wtforms.validators import DataRequired


class ItemCreationForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])
    main_pic = FileField()
    is_available = BooleanField('is_available')
    is_automatic = BooleanField('is_automatic')


class ItemUpdateForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])
    main_pic = FileField()
    is_available = BooleanField('is_available')
    is_automatic = BooleanField('is_automatic')


class ItemImagesForm(FlaskForm):
    pictures = FileField()
    picture_id = FloatField('picture_id')

class ItemAddJournal(FlaskForm):
    car_id = FloatField('car_id')
    user_id = FloatField('user_id')