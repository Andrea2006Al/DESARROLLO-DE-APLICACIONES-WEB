from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[DataRequired()]
    )

    telefono = StringField(
        "Teléfono",
        validators=[DataRequired()]
    )

    correo = StringField(
        "Correo",
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")