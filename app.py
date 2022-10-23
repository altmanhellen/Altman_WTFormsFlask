# Возьмите предыдущий проект с пользователями. Замените форму на wtforms. Нужны следующие валидаторы:
# 	•	Имя — непустое, максимум 30 символов, состоит только из символов кириллицы или латиницы
# 	•	Фамилия — непустая, максимум 30 символов, состоит только из символов кириллицы или латиницы
# 	•	Возраст — непустое поле, содержит число от 14 до 100
# 	•	Пароль: Минимум 8 символов, должен содержать буквы латиницы и цифры.
# 	•	Email — непустое поле, должен быть введен правильный email.
# Сделать сортировку по емейлу, по имени, по фамилии, по возрасту


from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, InputRequired, ValidationError
from operator import itemgetter, attrgetter, methodcaller

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Your secret key'

counter = 0

file = open("list_of_users.csv")
data = file.readlines()
mas = []

for i in data:
    mas.append(tuple(i.split()))

class Sortirovka:

    def __int__(self, mas):
        self.mas = mas

    @staticmethod
    def sortNumber(mas):
        return sorted(mas, key=itemgetter(0))

    @staticmethod
    def sortName(mas):
        return sorted(mas, key=itemgetter(1))

    @staticmethod
    def sortSurname(mas):
        return sorted(mas, key=itemgetter(2))

    @staticmethod
    def sortEmail(mas):
        return sorted(mas, key=itemgetter(5))

print(Sortirovka.sortNumber(mas))
print(Sortirovka.sortName(mas))
print(Sortirovka.sortSurname(mas))
print(Sortirovka.sortEmail(mas))

class MessageForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired(), Length(min=1, max=30)])
    surname = StringField("Surname: ", validators=[DataRequired(), Length(min=1, max=30)])
    age = StringField("Age: ", validators=[DataRequired()])
    psw = PasswordField("Password", validators=[Length(min=8)])
    email = StringField("Email: ", validators=[Email()])
    submit = SubmitField("Submit")

    def validate_name(form, field):
        slovar = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
        for letter in field.data:
            if letter.lower() not in slovar:
                raise ValidationError('Имя должно содержать только буквы')

    def validate_surname(form, field):
        slovar = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
        for letter in field.data:
            if letter.lower() not in slovar:
                raise ValidationError('Имя должно содержать только буквы')

    def validate_age(form, field):
        if field.data.isdigit():
            if int(field.data) < 14 or int(field.data) > 100:
                raise ValidationError('Для работы на нашем сайте вы должны быть старше 14 лет')
        else:
            raise ValidationError('Введите количество полных лет цифрами')

    def validate_psw(form, field):
        slovar = 'abcdefghijklmnopqrstuvwxyz'
        digits = '0123456789'
        count_letter = 0
        count_digit = 0
        for symbol in field.data:
            if symbol.lower() in slovar:
                count_letter += 1
            elif symbol in digits:
                count_digit += 1
        if count_letter == 0 or count_digit == 0:
            raise ValidationError('Пароль должен содержать латинские буквы и цифры')


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/message", methods=['get', 'post'])
def message():
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        age = form.age.data
        psw = form.psw.data
        email = form.email.data
        # print(f'{name}, {surname}, {age}, {psw}, {email}')
        global counter
        counter += 1
        with open('list_of_users.csv', 'a') as f:
            f.write(f'{len(mas)+1}. {name}, {surname}, {age}, {psw}, {email}\n')

        return redirect(url_for('message'))

    return render_template('message.html', form=form)


if __name__ == '__main__':
    app.run()
