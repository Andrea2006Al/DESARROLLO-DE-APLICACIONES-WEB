from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[DataRequired()]
    )

    telefono = StringField(
        "Teléfono",
        validators=[DataRequired()]
    )

    comunidad = StringField(
        "Comunidad",
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")