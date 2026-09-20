from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del servicio",
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
        "Stock",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    submit = SubmitField("Guardar")