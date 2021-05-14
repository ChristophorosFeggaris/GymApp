from flask import Flask,render_template,url_for,redirect,flash,request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextField,IntegerField,SelectField
from wtforms.fields.html5 import DateField
from flask_bootstrap import Bootstrap
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import date
  

app = Flask(__name__)

app.config['SECRET_KEY']= 'Firsttimeinaction'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/user.KOROPI/Documents/flask/env/myproject/myclients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)


manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

# CLASSES
class User(db.Model, UserMixin):
    __tablename__='User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True,nullable=False)
    email = db.Column(db.String(30), unique=True,nullable=False)
    password = db.Column(db.String(30),nullable=False)
    confirmed = db.Column(db.Boolean,default=False,nullable=False)
    
    
    def __init__(self,username,email,password,confirmed=False,confirmed_at=None):
        self.username=username
        self.email=email
        self.password=generate_password_hash(password)
        self.confirmed=confirmed
    
    
    def get(self):
       return super().get_id()

class Client(db.Model):
    __tablename__='Client'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20) )
    email = db.Column(db.String(30), unique=True)
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(30))
    phone_number = db.Column(db.Integer(), unique=True)
    subscr = db.relationship('Subscribe', backref=db.backref("client", lazy='joined'), lazy='dynamic')
    enter = db.relationship('Entrance', backref=db.backref("enter", lazy='joined'), lazy='dynamic')
    
    def __init__(self,first_name,last_name,email,gender,date_of_birth,address,phone_number):
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.gender=gender
        self.date_of_birth=date_of_birth
        self.address=address 
        self.phone_number=phone_number  
        
         
    def get(self):
       return super().get_id()

class Subscribe(db.Model):
    __tablename__ = 'Subscribe'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'))
    sub = db.Column(db.Integer)
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())

    def __init__(self,sub,start_date,end_date,client_id):
        self.sub = sub
        self.start_date = start_date
        self.end_date = end_date
        self.client_id = client_id
    
    def get(self):
       return super().get_id()

class Entrance(db.Model):
    __tablename__ = 'Entrance'
    id = db.Column(db.Integer, primary_key=True, unique=True) 
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'))
    date_enter = db.Column(db.Date())

    def __init__(self, date_enter,client_id):
        self.date_enter = date_enter
        self.client_id = client_id
    
    def get(self):
        return super().get_id()

# FORMS
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(max=25), Email()])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20), EqualTo('confirm', message='Oups!Wrong password')])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=6, max=20)])

class NewclientForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=20)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(), Length(max=25), Email()])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth  = DateField('Date of Birth', format='%Y-%m-%d')
    address = TextField('Address', validators=[InputRequired(), Length(max=30)])
    phone_number = StringField('Phone number', validators=[InputRequired(), Length(10, message="That's not a phone number")])

class EditClient(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=20)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(), Length(max=25), Email()])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth  = DateField('Date of Birth', format='%Y-%m-%d')
    address = TextField('Address', validators=[InputRequired(), Length(max=30)])
    phone_number = StringField('Phone number', validators=[InputRequired(), Length(10, message="That's not a phone number")])
    submit = SubmitField('Submit')

class ReloadSub(FlaskForm):
    sub = IntegerField('New subscribe')
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')

class EntranceClient(FlaskForm):
    idClient = IntegerField('Id here')  

@app.route('/')
@login_required
def index():
    return render_template('home.html')

@login_manager.unauthorized_handler
def unauthorized():
    
    return redirect(url_for('login'))

# REGISTER USER
@app.route('/register', methods=['GET','POST'])
def register():

    form=RegisterForm()
    
    if form.validate_on_submit():
        new_usr = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_usr)
        db.session.commit()    
    return render_template('register.html',form=form)

        
    
# LOGIN USER
@app.route('/login', methods=['GET','POST'])
def login():

    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))  
        flash('Incorrect username or password.')
    return render_template('login.html',form=form)

# NEW CLIENT
@app.route('/new_client', methods=['GET', 'POST'])
@login_required
def new_client():

    form = NewclientForm()
    if form.validate_on_submit():
        new_client=Client(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, gender=form.gender.data, date_of_birth=form.date_of_birth.data, address=form.address.data, phone_number=form.phone_number.data )
        db.session.add(new_client)
        db.session.commit() 
        return redirect(url_for('list_clients'))                 
    return render_template('clientform.html', form=form)

# LIST OF CLIENTS
@app.route('/list_clients') 
@login_required
def list_clients():
    Clients = Client.query.all()
    return render_template('list_clients.html', rows=Clients)

# PROFILE CLIENT
@app.route('/profile/<id>')
@login_required
def profile_client(id):
    client=Client.query.filter_by(id=id).first_or_404()
    db.session.commit()
    return render_template('profile_client.html', client=client, id=id)

# RELOAD SUBSCRIBE
@app.route('/reload_subscribe/<id>', methods=['GET','POST'])
@login_required
def reload_sub(id):
    form = ReloadSub()
    if form.validate_on_submit():
        new_sub=Subscribe(sub=form.sub.data, start_date=form.start_date.data, end_date=form.end_date.data,client_id=id)
        db.session.add(new_sub)
        db.session.commit()
        return redirect(url_for('profile_client', id=id))
    return render_template('reload_sub.html', form=form, id=id)

# ENTRANCE CLIENT
@app.route('/entrance', methods=['GET','POST'])
@login_required
def entrance():
    form = EntranceClient()
    if form.validate_on_submit():
        new_enter = Entrance(client_id=form.idClient.data, date_enter=date.today())
        if Client.query.filter_by(id=form.idClient.data).first_or_404():
            db.session.add(new_enter)
            db.session.commit()
            mx= Subscribe.query.filter_by(client_id=new_enter.client_id).first()
            max_date=mx.end_date
            #cur.execute("Select max(end_date) from subscribe where id = ?", (new_enter.client_id,))
            #max_date=cur.fetchall()
            #max_date=' '.join(map(str,max_date))
            #print(max_date)
            now = date.today()
            if now<max_date:
                remain_days=max_date-now
                flash(f"You're ok.You almost have {remain_days}", 'success')
                return redirect(url_for('profile_client', id=new_enter.client_id))
            else:
                flash("Sorry cannot access", 'error')
                return redirect(url_for('profile_client', id=new_enter.client_id))
        flash('Not a valid client')
    return render_template('entrance.html', form=form)

# EDIT CLIENT
@app.route('/edit_client/<id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    client = Client.query.filter_by(id = id).first_or_404()
    form = EditClient(formdata = request.form , obj = client)

    if form.validate_on_submit():
        #client = Client()
        client.first_name = form.first_name.data 
        client.last_name  = form.last_name.data
        client.email = form.email.data
        client.gender = form.gender.data
        client.date_of_birth = form.date_of_birth.data
        client.address = form.address.data
        client.phone_number = form.phone_number.data
        db.session.commit() 
        return redirect(url_for('list_clients'))  
    elif request.method == 'GET':
        #form = EditClient()
        form.first_name.data = client.first_name
        form.last_name.data = client.last_name    
        form.email.data = client.email
        form.gender.data = client.gender
        form.date_of_birth.data = client.date_of_birth
        form.address.data = client.address
        form.phone_number.data = client.phone_number  

    return render_template('edit_client.html', form=form)

# EDIT USER


# DELETE CLIENT
@app.route('/delete_client/<id>', methods=['GET','POST'])
@login_required
def delete_client(id):
    delete = Client.query.filter_by(id=id).first_or_404()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for('list_clients'))
    

# LOGOUT USER
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# SHOW USER
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__=="__main__":
    app.run(debug=True)
    
    
    