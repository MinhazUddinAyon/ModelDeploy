from flask import Flask, render_template, request,redirect,session, jsonify
from db import Database
#import requests
import helper

app = Flask(__name__)
dbo = Database()
app.secret_key = '1234'

@app.route('/')
def home():
    return render_template('main.html')
@app.route('/register')
def register():
    return render_template('Registration.html')

@app.route('/register/input', methods=['post'])
def registerInput():
    Name = request.form.get('personName')
    Email = request.form.get('personEmail')
    Pass = request.form.get('personPassword')
    response = dbo.insert(Name, Email, Pass)
    if response:
        return render_template('Login.html', message="Registration Successful. Kindly login to proceed")
    else:
        return render_template('Registration.html', message="Email Already Exists. Kindly Register again to proceed")
@app.route('/login')
def login():
    if 'counter' not in session:
        session['counter'] = 0
    session['counter'] += 1  # Increment counter on every access

    return render_template('Login.html', counter=session['counter'])

@app.route("/login/input", methods=['post'])
def loginInput():
    Email = request.form.get('personEmail')
    Pass = request.form.get('personPassword')
    response = dbo.search(Email, Pass)
    if response:
        session['logged_in'] = 1
        return render_template('perform.html', message='Login Successful!')
    else:
        return render_template('Login.html', message='Incorrect Email/Password!')

@app.route('/action')
def action():
    return render_template('perform.html')

@app.route('/nextpage')
def next_page():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect('/login')

    return render_template('nextpage.html')


#pipeline.pkl filter=lfs diff=lfs merge=lfs -text
@app.route('/usedcar')
def used_car():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect('/login')

    return render_template('usedcar.html')

@app.route('/makers')
def makers():
    maker = helper.maker_name('Maker')
    genmodel = helper.maker_name('Genmodel')
    bodytype = helper.maker_name('Bodytype')
    gearbox = helper.maker_name('Gearbox')
    fuel_type = helper.maker_name('Fuel_type')
    average_mpg = helper.maker_name('Average_mpg')
    cars_old = helper.maker_name('Cars_old')
    return render_template('usedcar.html',
                           maker = sorted(maker),
                           genmodel=sorted(genmodel),
                           bodytype=sorted(bodytype),
                           gearbox=sorted(gearbox),
                           fuel_type=sorted(fuel_type),
                           average_mpg=sorted(average_mpg),
                           cars_old=sorted(cars_old)
                           )
@app.route('/predict_car_price')
def predict_car_price():
    Maker = request.args.get('maker')
    Genmodel = request.args.get('genmodel')
    Bodytype = request.args.get('bodytype')
    Gearbox = request.args.get('gearbox')
    Fuel_type = request.args.get('fuel_type')
    Runned_Miles = float(request.args.get('runned_miles'))
    Engine_size = float(request.args.get('engine_size'))
    Engine_power = float(request.args.get('engine_power'))
    Average_mpg = request.args.get('average_mpg')
    Top_speed = float(request.args.get('top_speed'))
    Wheelbase = float(request.args.get('wheelbase'))
    Height = float(request.args.get('height'))
    Width = float(request.args.get('width'))
    Length = float(request.args.get('length'))
    Seat_num = float(request.args.get('seat_num'))
    Door_num = float(request.args.get('door_num'))
    Cars_old = request.args.get('cars_old')

    prediction = helper.make_prediction(Maker, Genmodel, Bodytype, Gearbox, Fuel_type, Runned_Miles,Engine_size, Engine_power, Average_mpg, Top_speed, Wheelbase,
                    Height, Width, Length, Seat_num, Door_num, Cars_old)
    return render_template('usedcar.html',prediction = prediction)

#if __name__ == "__main__":
    #app.run(debug=True,port=9000)
