# post functions
from flask import render_template, request, flash, url_for, redirect
from . import db
from . import models, forms
from flask_login import login_user, logout_user, login_required, current_user

from .models import Employee, User


def index():
    employee = models.Employee.query.all()
    return render_template("index.html", employee=employee)


@login_required
def employee_create():
    form = forms.EmployeeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_employee = models.Employee(
                fullname=request.form.get("fullname"),
                phone=request.form.get("phone"),
                short_info=request.form.get("short"),
                experience=request.form.get("experience"),
                preferred_position=request.form.get("preferred_position"),
                user_id=current_user.id)
            db.session.add(new_employee)
            db.session.commit()
            flash("Success")
            return redirect(url_for("index"))
        if form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category="danger")
        return render_template("employee_create.html", form=form)




def employee_detail(employee_id):
    employee = Employee.query.get(id=employee_id)
    return render_template("employee_detail.html", employee=employee)


@login_required
def employee_delete(employee_id):
    employee = Employee.query.get(id=employee_id)
    if employee.user_id == current_user.id:
        if request.method == "POST":
            db.session.delete(employee)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            form = forms.EmployeeForm()
            return render_template("employee_delete.html", employee=employee, form=form)
    else:
        flash("Сотрудник не найден", category="danger")
        return redirect(url_for("index"))


def employee_update(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first()
    if employee:
        if employee.user_id == current_user.id:
            form = forms.EmployeeForm(obj=employee)
            if request.method == "POST":
                if form.validate_on_submit():
                    employee.fullname = request.form.get("fullname")
                    employee.phone = request.form.get("phone")
                    employee.short_info = request.form.get("short_info")
                    employee.experience = request.form.get("experience")
                    employee.preferred_position = request.form.get("preferred_position")
                    db.session.commit()
                    flash('Данные сотрудник успешно обновлены', category='success')
                    return redirect(url_for("index"))
                if form.errors:
                    for errors in form.errors.values():
                        for error in errors:
                            flash(error, category="danger")
            return render_template("employee_update.html", form=form, employee=employee)
        else:
            flash("у вас недостаточно прав", category="danger")
            return redirect(url_for("index"))
    else:
        flash('Сотрудник не найден', category='danger')
        return redirect(url_for('index'))



# user functions

def register():
    user_form = forms.UserForm()
    if request.method == "POST":
        if user_form.validate_on_submit():
            username = request.form.get("username")
            password = request.form.get("password")
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Пользователь успешно зарегистрировался", category="success")
            return redirect(url_for("login"))
        if user_form.errors:
            for errors in user_form.errors.values():
                for error in errors:
                    flash(error, category="danger")
    return render_template("register.html", form=user_form)


def login():
    user_form = forms.UserForm()
    if request.method == "POST":
        if user_form.validate_on_submit():
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash("Вы успешно зашли в систему", category="success")
                return redirect(url_for("index"))
            else:
                flash("Неверный логин или пароль", category="danger")
                return render_template("login.html", form=user_form)
        if user_form.errors:
            for errors in user_form.errors.values():
                for error in errors:
                    flash(error, category="danger")
    return render_template("login.html", form=user_form)


def logout():
    logout_user()
    flash('Вы успешно вышли из системы', category='success')
    return redirect(url_for('login'))
