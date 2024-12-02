from flask import render_template, url_for, redirect
from proj_flask_bot import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from proj_flask_bot.forms import FormLogin, FormCriarConta
from proj_flask_bot.models import Usuario
import os 
from werkzeug.utils import secure_filename


@app.route("/", methods = ["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email = form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("feed"))
    return render_template("homepage.html", form = form_login)



@app.route("/criarconta", methods = ["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username= form_criarconta.username.data,senha=senha,email=form_criarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form = form_criarconta)