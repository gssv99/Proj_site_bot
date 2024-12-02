from proj_flask_bot import database, app
from proj_flask_bot.models import Usuario


with app.app_context():
    database.create_all()