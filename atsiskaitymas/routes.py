from datetime import datetime
from flask import redirect, request, render_template, flash, url_for
from flask_bcrypt import Bcrypt
from flask_login import logout_user, login_user, login_required, current_user

from atsiskaitymas.models import User, Car, Admin, Repair
from atsiskaitymas import forms
from atsiskaitymas import app, db, admin

admin.add_view(Admin(User, db.session))
admin.add_view(Admin(Car, db.session))
admin.add_view(Admin(Repair, db.session))

bcrypt = Bcrypt(app)


@app.route("/admin")
@login_required
def admin():
    return redirect(url_for(admin))

@app.route('/')
def home():
    flash('Hello', 'info')
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Log out to register a new user.')
        return redirect(url_for('home'))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        coded_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        is_first_user = not User.query.first()
        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = coded_password,
            is_admin = is_first_user,
            is_staff = is_first_user
        )
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered! You can log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')
    if current_user.is_authenticated:
        flash('User is already logged in. Please log out and try again.')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed, incorrect email or password.', 'danger')
    return render_template('login.html', form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home')) 

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = forms.ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', current_user=current_user, form=form)    

@app.route('/car_register', methods=['GET', 'POST'])
@login_required
def car_register():
    form = forms.CarRegisterForm()
    if form.validate_on_submit():
        new_car = Car(
            car_brand = form.car_brand.data,
            model = form.model.data,
            years = form.years.data,
            engine = form.engine.data,
            plate = form.plate.data,
            vin = form.vin.data,
            user_id = current_user.id
        )
        db.session.add(new_car)
        db.session.commit()
        flash('Successful registration', 'succes')
        return redirect(url_for('home'))
    return render_template('car_register.html', form=form, current_user=current_user)

@app.route('/repair/<int:car_id>', methods=['GET', 'POST'])
@login_required
def repair(car_id):
    form = forms.RepairForm()
    if form.validate_on_submit():
        new_repair = Repair(
            description = form.description.data,
            car_id = car_id
        )
        db.session.add(new_repair)
        db.session.commit()
        flash('Successful registration', 'succes')
        return redirect(url_for('home'))
    return render_template('repair.html', form=form, current_user=current_user, car_id=car_id)  

@app.route('/all_cars')
@login_required
def all_cars():
    page = request.args.get('page', 1, type=int)
    visi_automobiliai = Car.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=5)
    return render_template("all_cars.html", visi_automobiliai=visi_automobiliai, datetime=datetime)

@app.route('/all_repairs')
@login_required
def all_repairs():
    try:
        all_defects= Repair.query.all()
    except:
        all_defects = []
    return render_template('all_repairs.html', all_defects=all_defects)

@app.route('/edit_defect/<int:id>', methods=['GET', 'POST'])
def edit_defect(id):
    form = forms.RepairForm()
    try:
        defect_obj = Repair.query.get(id)
    except:
        return redirect(url_for('all_repairs'))
    else:  
        if form.validate_on_submit():
            defect_obj.status = form.status.data
            defect_obj.price = form.price.data
            db.session.commit()
            return redirect(url_for('all_repairs'))
        return render_template("edit_defect.html", form=form, defect_obj=defect_obj) 

@app.route('/orders_history/<int:car_id>')
@login_required
def orders_history(car_id):
    cars_history = Repair.query.filter_by(car_id=car_id).all()
    return render_template("orders_history.html", cars_history=cars_history, datetime=datetime)