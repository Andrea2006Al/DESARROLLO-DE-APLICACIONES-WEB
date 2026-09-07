from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[DataRequired()]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired()]
    )

    estado = StringField(
        "Estado",
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")