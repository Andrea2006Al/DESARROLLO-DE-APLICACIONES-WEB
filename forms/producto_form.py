from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[DataRequired()]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired()]
    )

    precio = FloatField(
        "Precio",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    submit = SubmitField("Guardar")