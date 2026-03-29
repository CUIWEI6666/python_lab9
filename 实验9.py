# Импортируем необходимые модули
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Инициализируем Flask-приложение
app = Flask(__name__)

# Конфигурируем базу данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем лишние предупреждения

# Инициализируем SQLAlchemy
db = SQLAlchemy(app)


# Модель базы данных (Телефонная книга)
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный ID контакта
    name = db.Column(db.String(100), nullable=False)  # Имя (обязательное поле)
    phone = db.Column(db.String(20), nullable=False)  # Номер телефона (обязательное поле)

    def __repr__(self):
        return f'<Contact {self.name}>'


# Главная страница: показать все контакты + форма добавления
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из формы
        contact_name = request.form['name']
        contact_phone = request.form['phone']

        # Создаем новый контакт
        new_contact = Contact(name=contact_name, phone=contact_phone)

        # Сохраняем в базу данных
        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect(url_for('index'))  # Обновляем страницу
        except:
            return "Ошибка при добавлении контакта"
    else:
        # Получаем все контакты из БД
        contacts = Contact.query.all()
        return render_template('index.html', contacts=contacts)


# Запускаем приложение
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем таблицы в базе данных
    app.run(debug=True)