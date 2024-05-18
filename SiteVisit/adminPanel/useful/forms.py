from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField, RadioField
from wtforms.fields.simple import TelField, TextAreaField, URLField, FileField
from wtforms.validators import Length, Regexp


class ProfileForm(FlaskForm):
    logos = [("None", "Выберите лого"),
             ("vk", "vk"),
             ("twitter", "twitter"),
             ("instagram", "instagram"),
             ("facebook", "facebook"),
             ("youtube", "youtube"),
             ("linkedin", "linkedin"),
             ("behance", "behance"),
             ("dribbble", "dribbble"),
             ("whatsapp", "whatsapp"),
             ("wechat", "wechat"),
             ("wordpress", "wordpress"),
             ("twitch", "twitch"),
             ("yahoo", "yahoo"),
             ]
    name = StringField("Имя",
                       validators=[Length(min=2, max=25, message="Имя должно содержать от 2 до 25 символов"),
                                   Regexp('^[a-zA-Zа-яА-яёЁ]+$', message='Имя должно состоять только из букв '
                                                                         'русского и латинского алфавита')],
                       description="Ваше имя")
    surname = StringField("Фамилия",
                          validators=[Length(min=2, max=40, message="Фамилия должна содержать от 2 до 25 символов"),
                                      Regexp('^[a-zA-Zа-яА-яёЁ]+$', message='Фамилия должно состоять только из букв '
                                                                            'русского и латинского алфавита')],
                          description="Ваша фамилия")
    avatar = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    phone = TelField("Мобильный номер", validators=[Length(min=10, max=10, message="Номер телефона содержит 10 цифр"),
                                                    Regexp('^\\d+$', message='only digits')],
                     description="Введите номер телефона")
    profession = StringField("Профессия", validators=[Length(min=4, max=40, message="Профессия должна содержать от 4 "
                                                                                    "до 25 символов")],
                             description="Ваша профессия")
    about = TextAreaField("О себе", validators=[Length(min=0, max=200, message="Поле 'О себе' должно содержать "
                                                                               "до 200 символов")],
                          description="Здесь Вы можете написать о себе, своих скиллам, хобби, достижениях")
    type_profile = RadioField("Вид Вашей визитки", choices=[(0, "1"), (1, "2"), (2, "3")], default=0)
    logo1 = SelectField("Logo 1", choices=logos, default=None)
    logo2 = SelectField("Logo 2", choices=logos, default=None)
    logo3 = SelectField("Logo 3", choices=logos, default=None)
    logo4 = SelectField("Logo 4", choices=logos, default=None)
    logo5 = SelectField("Logo 5", choices=logos, default=None)
    logo6 = SelectField("Logo 6", choices=logos, default=None)
    url1 = URLField("URL 1",
                    description="Введите ссылку на Вашу страницу")
    url2 = URLField("URL 2",
                    description="Введите ссылку на Вашу страницу")
    url3 = URLField("URL 3",
                    description="Введите ссылку на Вашу страницу")
    url4 = URLField("URL 4",
                    description="Введите ссылку на Вашу страницу")
    url5 = URLField("URL 5",
                    description="Введите ссылку на Вашу страницу")
    url6 = URLField("URL 6",
                    description="Введите ссылку на Вашу страницу")
    submit = SubmitField("Сохранить")

# validators=[URL(message="Enter Valid URL Please.")],
