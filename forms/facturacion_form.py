from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        "N.º Factura",
        validators=[DataRequired()]
    )

    cliente = StringField(
        "Cliente",
        validators=[DataRequired()]
    )

    servicio = StringField(
        "Servicio",
        validators=[DataRequired()]
    )

    valor = FloatField(
        "Valor",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    submit = SubmitField("Guardar")