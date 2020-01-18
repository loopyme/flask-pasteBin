from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
    # PasswordField,
)
from wtforms.validators import DataRequired, Length


# class VerifyForm(FlaskForm):
#     password = PasswordField(
#         u"Code: ", validators=[DataRequired(message=u"Code is not none")]
#     )
#     submit = SubmitField(u"Go")


class PasteForm(FlaskForm):
    record_title = StringField(
        u"Title  : ",
        validators=[DataRequired(message=u"Title should not be null"), Length(1, 10)],
        render_kw={"class": "text-body", "style": "width:100%;margin: auto;"},
    )
    record_type = SelectField(
        u"Type:",
        choices=[("text", "Text"), ("url", "URL")],
        render_kw={"style": "width:100%;margin: auto;"},
    )
    record_expire = SelectField(
        u"Expiration:",
        choices=[
            ("3600", "1 hour"),
            ("86400", "1 day"),
            ("604800", "7 days"),
            ("18144000", "30 days"),
            ("-2", "1 visit"),
            ("-6", "5 visits"),
            ("-11", "10 visits"),
            ("-101", "100 visits"),
            ("None", "permanent"),
        ],
        render_kw={"style": "width:100%;margin: auto;"},
    )
    record_content = TextAreaField(
        u"Content: ",
        validators=[
            DataRequired(message=u"Content should not be null"),
            Length(1, 2 ** 15),
        ],
        render_kw={
            "class": "text-body",
            "style": "height:100px;margin: auto;width:100%",
        },
    )

    record_submit = SubmitField(u"Paste!")
