from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, session
from datetime import date, datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from functools import wraps
import mysql.connector
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret string here'
app.permanent_session_lifetime = timedelta(minutes=15)

userpass = 'mysql://root:@'
basedir = '127.0.0.1'
dbname = '/newest'
socket = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
dbname = dbname + socket
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.route('/')
@app.route('/index.html')
def hello_world():
    return render_template("index.html")


@app.route('/inner-page.html')
def blog3():
    today = date.today()
    now = datetime.now()
    day = today.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M")
    # print(day)
    # print(time)
    return render_template("inner-page.html", day=day, time=time)


@app.route('/update', methods=["GET", "POST"])
def update():
    print("aap k i")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="newest"
    )
    mycursor = mydb.cursor()
    if request.method == "POST":
        membership_id = request.form.get("membership_id")
        excercise_id = request.form.getlist("f_name")

        print(1)
        print(excercise_id)

        print(membership_id)
        for i in range(0, len(excercise_id)):
            temp = int(excercise_id[i])
            print(temp)

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="newest"
            )
            mycursor = mydb.cursor()
            mycursor.execute('insert into excercise_done (member_id,exe_id) values (%s,%s)',
                             (membership_id, temp,))
            mydb.commit()
            # mycursor.execute('insert into excercise_done(member_id, excercise_id) values(1, 1)')
            mycursor.execute('select * from excercise_done')
            account = mycursor.fetchall()
            print(account)

            print("added")
        print(1)

    return redirect('/home')


@app.route('/1', methods=["GET", "POST"])
def login_normal():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="newest"
    )
    mycursor = mydb.cursor()
    # print(request.form.get("member_id"))
    # print(request.form.get("time"))
    # print(request.form.get("day"))
    if request.method == "POST" and 'membership_id' in request.form and 'day' in request.form and 'time' in request.form:
        membership_id = request.form.get("membership_id")
        day = request.form.get("day")
        time = request.form.get("time")
        # print(request.form.get("member_id"))
        # print(request.form.get("time"))
        # print(request.form.get("day"))
        # mycursor.execute(
        #     "SELECT * FROM attandace NOT TIME (entry_time)")
        # ss = str([x[0] for x in mycursor.fetchall()])[15:-2]
        # print("===================================================")
        # print(ss)
        # print("===================================================")

        # payment_id = 1
        mycursor.execute('SELECT * FROM register WHERE member_id = %s ', (membership_id,))
        account = mycursor.fetchall()
        ###############################################3 attandance     #1
        print("hello")
        print(account)
        if account != []:
            mycursor.execute(
                "SELECT due_date FROM `payment` WHERE member_id =\'{0}\'ORDER by due_date DESC LIMIT 1".format(
                    membership_id))
            payment_id = str([x[0] for x in mycursor.fetchall()])[15:-2]
            session.permanent = True
            session["user"] = membership_id
            print(1)
            mycursor.execute(
                'SELECT entry_day FROM attandace WHERE member_id = %s ORDER By attandace.entry_day DESC LIMIT 1 ',
                (membership_id,))
            dieting = str([x[0] for x in mycursor.fetchall()])[2:-2]
            print("=====================================================")
            print(type(dieting))
            print(dieting)
            # if dieting==
            today = date.today()
            date1 = today.strftime("%d/%m/%Y")
            print(date1)
            print(type(date1))
            mycursor.execute(
                'SELECT exit_time FROM attandace WHERE member_id = %s ORDER By attandace.entry_day DESC LIMIT 1 ',
                (membership_id,))
            eating = str([x[0] for x in mycursor.fetchall()])[1:-1]
            print("##############")
            print(eating)
            print(type(eating))
            print("##############")
            print("=====================================================")
            if dieting == '':
                print("numm")
                mycursor.execute('insert into attandace (entry_day,entry_time,member_id) values (%s,%s,%s)',
                                 (day, time, membership_id,))
                mydb.commit()
            elif dieting == date1 and eating == 'None':
                print("asfdgfsbn")
                # "select * from users where userID='" + membership_id + "'"
                mycursor.execute(
                    "update attandace set exit_time='" + time + "' where member_id='" + membership_id + "'")
                mydb.commit()
            elif dieting == date1 and eating != 'None':
                return "=1"

            # tasks = Task.query.all()
            today = date.today()
            date1 = today.strftime("%d/%m/%Y")
            day = datetime.today().strftime('%A')
            # print(day)
            mycursor.execute('SELECT Name FROM register WHERE member_id = %s ', (membership_id,))
            name = str([x[0] for x in mycursor.fetchall()])[2:-2]
            # membership_left = mycursor.execute('SELECT due_date FROM payment WHERE member_id = %s ', (membership_id,))
            membership_left = payment_id
            membership_id = membership_id

            # day
            # chest , back
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="newest"
            )
            print("YHA tk to")
            mycursor = mydb.cursor()

            mycursor.execute(
                "SELECT * FROM `available`")

            data = mycursor.fetchall()
            print(data)
            # print(data[0][)
            lav = data
            print("1111111111111")
            print(lav)
            print("1111111111111")
            lav1 = []
            for i in range(0, len(lav)):
                lav1.append(data[i][1])
            print(lav1)
            return render_template("list.html", date=date1, day=day, name=name,
                                   membership_left=membership_left,
                                   data=data, membership_id=membership_id, lav=json.dumps(lav1))
        else:
            if "user" in session:
                return redirect('/home')
            else:
                flash('Check your member Id')
                return redirect(url_for('blog3'))
    elif request.method == "POST" and 'membership_id' in request.form:
        membership_id = request.form.get("membership_id")

        mycursor.execute('SELECT * FROM register WHERE member_id = %s ', (membership_id,))
        account = mycursor.fetchall()
        print("hello")
        print(account)

        ###############################################3 attandance
        if account != []:
            session.permanent = True
            session["user"] = membership_id
            print(1)
            mycursor.execute(
                "SELECT due_date FROM `payment` WHERE member_id =\'{0}\'ORDER by due_date DESC LIMIT 1".format(
                    membership_id))
            payment_id = str([x[0] for x in mycursor.fetchall()])[15:-2]
            print(payment_id)
            # tasks = Task.query.all()
            today = date.today()
            date1 = today.strftime("%d/%m/%Y")
            day = datetime.today().strftime('%A')
            # print(day)
            mycursor.execute('SELECT Name FROM register WHERE member_id = %s ', (membership_id,))
            name = str([x[0] for x in mycursor.fetchall()])[2:-2]
            # membership_left = mycursor.execute('SELECT due_date FROM payment WHERE member_id = %s ', (membership_id,))
            membership_left = payment_id
            membership_id = membership_id
            # day
            # chest , back
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="newest"
            )
            print("YHA tk to")
            mycursor = mydb.cursor()

            mycursor.execute(
                "SELECT * FROM `available`")

            data = mycursor.fetchall()
            print(data)
            print(data[1][0])
            lav = data
            lav1 = []
            for i in range(0, len(lav)):
                lav1.append(data[i][1])
            print(lav1)
            return redirect(url_for('home', membership_id=membership_id))
            # return render_template("list.html", date=date1, day=day, name=name,
            #                        membership_left=membership_left,
            #                        data=data, membership_id=membership_id,
            #                        lav=json.dumps(lav1))  ################################################# login
        else:
            if "user" in session:
                return redirect('/home')
            else:
                flash('Check your member Id')
                return redirect('/')

    else:
        return redirect('/500.html')


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


@app.route('/register2.html')
def html_page1():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="newest"
    )
    myd = mydb.cursor()
    myd.execute(
        'SELECT * from offers')
    offer = myd.fetchall()
    print(offer)
    return render_template('register2.html', offer=offer, o=json.dumps(offer))


@app.route('/home', methods=['get'])
def home():
    print("HERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
    if "user" in session:
        print("HERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
        usermemberid = session["user"]
        # m_id = membership_id
        print(usermemberid)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="newest"
        )
        ##################################################################
        #                   New
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT excercise_done.Date,SUM(available.Shoulder) AS shoulder_total,SUM(available.Chest) AS chest_total,SUM(available.Arms) AS arms_total,SUM(available.Legs) AS legs_total,SUM(available.Back_Abs) AS back_abs_total,available.Shoulder+available.Chest+available.Legs+available.Arms+available.Back_Abs as Total FROM `excercise_done`INNER JOIN available ON available.excercise_id = excercise_done.exe_id Where excercise_done.member_id='" + usermemberid + "'GROUP BY Date(excercise_done.Date)")

        fet = mycursor.fetchall()
        #                   member id  dalni h
        # mycursor.execute(
        #     "select * from userregistration where firstname='" + username + "' and password='" + password + "'"
        # ######################################################################
        tarik = []
        Shoulder = []
        chest = []
        Arms = []
        Legs = []
        Back_abs = []
        Total = []
        for i in range(0, len(fet)):
            tarik.append(str(fet[i][0]))
            # Shoulder.append(int(fet[i][1]))
            Shoulder.append(0 if fet[i][1] is None else int(fet[i][1]))
            chest.append(0 if fet[i][2] is None else int(fet[i][2]))
            Arms.append(0 if fet[i][3] is None else int(fet[i][3]))
            Legs.append(0 if fet[i][4] is None else int(fet[i][4]))
            Back_abs.append(0 if fet[i][5] is None else int(fet[i][5]))
            Total.append(0 if fet[i][6] is None else int(fet[i][6]))
        print("========================")
        print(tarik)
        print(Shoulder)
        print(chest)
        print(Arms)
        print(Legs)
        print(Back_abs)
        print(Total)
        all = []
        for i in range(0, len(fet)):
            z = dict({
                "Date": tarik[i],
                "Shoulder": Shoulder[i],
                "Chest": chest[i],
                "Arms": Arms[i],
                "Legs": Legs[i],
                "Back_abs": Back_abs[i],
                "sum": int(Shoulder[i]) + int(chest[i]) + int(Arms[i]) + int(Legs[i]) + int(Back_abs[i])
            })
            all.append(z)
        print(all)
        mycursor.close()
        ##################################################################################################
        myd = mydb.cursor()
        myd.execute(
            'SELECT Name from register where member_id=' + usermemberid)
        naam = myd.fetchall()
        naam = str(naam[0])[2:-3]
        print(str(naam[0])[2:-3])
        ##################################################################################################
        myd = mydb.cursor()
        myd.execute(
            'SELECT register.Name,SUM(available.Shoulder) AS shoulder_total,SUM(available.Chest) AS chest_total,'
            'SUM(available.Arms) AS arms_total,SUM(available.Legs) AS legs_total,SUM(available.Back_Abs)'
            ' AS back_abs_total,available.Shoulder+available.Chest+available.Legs+available.Arms+available.Back_Abs as Total FROM `excercise_done` '
            'INNER JOIN available ON available.excercise_id = excercise_done.exe_id  INNER JOIN register '
            'ON excercise_done.member_id = register.member_id GROUP BY excercise_done.member_id ORDER BY Total Desc LIMIT 3')
        get = myd.fetchall()
        print("9999999999999999999999999999999999999")
        print(get)
        print(type(get))
        print(type(get[0]))
        name = []
        Shoulder_n = []
        chest_n = []
        Arms_n = []
        Legs_n = []
        Back_abs_n = []
        Total_n = []
        for i in range(0, len(get)):
            name.append(str(get[i][0]))
            # Shoulder.append(int(fet[i][1]))
            Shoulder_n.append(0 if get[i][1] is None else int(get[i][1]))
            chest_n.append(0 if get[i][2] is None else int(get[i][2]))
            Arms_n.append(0 if get[i][3] is None else int(get[i][3]))
            Legs_n.append(0 if get[i][4] is None else int(get[i][4]))
            Back_abs_n.append(0 if get[i][5] is None else int(get[i][5]))
            Total_n.append(0 if get[i][6] is None else int(get[i][6]))
        myd.close()
        print(name)
        print(Shoulder_n)
        print(chest_n)
        print(Arms_n)
        print(Legs_n)
        print(Back_abs_n)
        print(Total_n)
        final = []
        for i in range(0, len(get)):
            # L=int(tarik[i]) + int(Shoulder[i]) + int(chest[i]) + int(Arms[i]) + int(Legs[i]) + int(Back_abs[i])
            z = tuple((name[i], Shoulder_n[i], chest_n[i], Arms_n[i], Legs_n[i], Back_abs_n[i], Total_n[i]))
            final.append(z)
        print(final)
        #################################################################################################
        myd = mydb.cursor()
        myd.execute(
            "SELECT excercise_done.member_id,SUM(available.Shoulder) AS shoulder_total,SUM(available.Chest) AS chest_total,SUM(available.Arms) AS arms_total,SUM(available.Legs) AS legs_total,SUM(available.Back_Abs) AS back_abs_total,SUM(available.Shoulder+available.Chest+available.Legs+available.Arms+available.Back_Abs) as Total FROM `excercise_done` INNER JOIN available ON available.excercise_id = excercise_done.exe_id Where excercise_done.member_id=" + usermemberid)
        pie = myd.fetchall()
        print("===============================")
        print(pie)
        print("===============================")
        pie_L = [{
            "country": "shoulder",
            "litres": (0 if pie[0][1] is None else int(pie[0][1]))
        }, {
            "country": "chest",
            "litres": (0 if pie[0][2] is None else int(pie[0][2]))
        }, {
            "country": "Arms",
            "litres": (0 if pie[0][3] is None else int(pie[0][3]))
        }, {
            "country": "Legs",
            "litres": (0 if pie[0][4] is None else int(pie[0][4]))
        }, {
            "country": "Back_abs",
            "litres": (0 if pie[0][5] is None else int(pie[0][5]))
        }]
        print(pie_L)
        mycursor.close()
        ################################################################################
        myd = mydb.cursor()
        myd.execute(
            "SELECT excercise_done.Date,SUM(available.Shoulder) AS shoulder_total,SUM(available.Chest) AS chest_total,SUM(available.Arms) AS arms_total,SUM(available.Legs) AS legs_total,SUM(available.Back_Abs) AS back_abs_total,available.Shoulder+available.Chest+available.Legs+available.Arms+available.Back_Abs as Total FROM `excercise_done` INNER JOIN available ON available.excercise_id = excercise_done.exe_id Where excercise_done.member_id='" + usermemberid + "' AND excercise_done.Date=CURDATE()")
        pie_to = myd.fetchall()
        print("===============================")
        print(pie_to)
        print("===============================")

        pie_T = [{
            "country": "shoulder",
            "litres": 0 if pie_to[0][1] is None else int(pie_to[0][1])
        }, {
            "country": "chest",
            "litres": 0 if pie_to[0][2] is None else int(pie_to[0][2])
        }, {
            "country": "Arms",
            "litres": 0 if pie_to[0][3] is None else int(pie_to[0][3])
        }, {
            "country": "Legs",
            "litres": 0 if pie_to[0][4] is None else int(pie_to[0][4])
        }, {
            "country": "Back_abs",
            "litres": 0 if pie_to[0][5] is None else int(pie_to[0][5])
        }]
        print(pie_T)
        myd.execute('Select * from offers')
        offer = myd.fetchall()
        print(offer)
        ###############################################################################
        return render_template('index3-horizontalmenu.html', all=json.dumps(all), date=json.dumps(tarik),
                               value=json.dumps(Shoulder),
                               chest=json.dumps(chest), Arms=json.dumps(Arms), Legs=json.dumps(Legs),
                               Back_abs=json.dumps(Back_abs), Total=json.dumps(Total), fet=fet, get=get,
                               pie_L=json.dumps(pie_L), pie_T=json.dumps(pie_T), name=naam, id=usermemberid,
                               offer=offer)
    else:
        return redirect(url_for("login_normal"))


######################################################## DEBUG HERE ####################################################
@app.route('/View_Detail', methods=['POST'])
def vire():
    print("herererererererererer")
    date = request.form['date']
    usermemberid = request.form['tokken']
    print(date)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="newest"
    )
    myd = mydb.cursor()
    myd.execute(
        "SELECT available.excercise_name,available.Shoulder,available.Chest,available.Legs,available.Arms,available.Back_Abs,available.Shoulder+available.Chest+available.Legs+available.Arms+available.Back_Abs as Total FROM `excercise_done` INNER JOIN available ON available.excercise_id = excercise_done.exe_id Where excercise_done.Date='" + date + "'AND excercise_done.member_id=" + usermemberid)
    d = myd.fetchall()
    print(d)
    return jsonify({'result': 'success'}, {'member_num': d})


@app.route('/pee', methods=['POST'])
def pee():
    print("herererererererererer")
    name = request.form['name']
    print(name)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="newest"
    )
    myd = mydb.cursor()
    myd.execute(
        'Select Name from register where member_id=' + name)
    d = [x[0] for x in myd.fetchall()]
    print(d)
    if d == []:
        print("YUP")
        # flash("Enter Valid Memebership Id")
        return jsonify({'result': 'failed'})
    print(type(d))
    print(d[0])
    print(type(d[0]))
    return jsonify({'result': 'success', 'name': d[0], 'mem_id': name})


@app.route('/peeling', methods=['POST'])
def peeling():
    print("herererererererererer")
    name = request.form['name']
    print(name)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="newest"
    )
    myd = mydb.cursor()
    myd.execute(
        'Select Amount from offers where offer_id=' + name)
    d = [x[0] for x in myd.fetchall()]
    print(d)
    print(d[0])
    print(type(d[0]))
    if d == []:
        print("YUP")
        flash("Enter Valid Memebership Id")
        return jsonify({'result': 'failed'})
    # return redirect(url_for(hurray, d=d[0]))
    return jsonify({'result': 'success', 'name': d[0]})


@app.route('/insert', methods=['POST'])
def insert():
    try:
        print("herererererererererer")
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']
        print(name)
        print(address)
        print(contact)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="newest"
        )
        mycursor = mydb.cursor()
        mycursor.execute('insert into register (Name,Contact,Address) values (%s,%s,%s)',
                         (name, str(contact), address,))
        mydb.commit()
        mycursor.execute('SELECT member_id FROM register WHERE name = %s and contact= %s and address = %s',
                         (name, contact, address))
        z = str(mycursor.fetchall())[2:-3]
        print("to kar na")
        print(z)
        zz = int(z)
        return jsonify({'result': 'success', 'mem_id': z, 'name': name})
    except mysql.connector.IntegrityError as err:
        print("Contact Number already Registered")
        return redirect('/register2.html')


################################################ INCOMPLETE ########################################################
@app.route('/payed', methods=['POST'])
def payed():
    try:
        mem_id = request.form['mem_id']
        pay_id = request.form['pay_id']
        offer_id = request.form['offer_id']
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="newest"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select No_of_days from offers where offer_id =  %s", (offer_id,))
        days = mycursor.fetchall()
        print(days)
        print(str(days[0])[1:-2])
        print(int(str(days[0])[1:-2]))
        print(type(int(str(days[0])[1:-2])))
        days = int(str(days[0])[1:-2])
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(mem_id)
        print(pay_id)
        print(offer_id)
        start = datetime.today().strftime('%Y-%m-%d')
        print(start)
        print(type(start))
        end = datetime.today() + timedelta(days=days)
        end = end.strftime('%Y-%m-%d')
        print(end)
        print(type(end))
        # [pay_id, mem_id, date, date2, offer_id]
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="newest"
        )
        mycursor = mydb.cursor()
        mycursor.execute('insert into payment (pay_id,member_id,payment_date,due_date,of_id) values (%s,%s,%s,%s,%s)',
                         (pay_id, str(mem_id), start, end, offer_id,))
        mydb.commit()
        # mycursor.execute('SELECT member_id FROM register WHERE name = %s and contact= %s and address = %s',
        #                  (name, contact, address))
        # z = [x[0] for x in mycursor.fetchall()]
        # print("to kar na")
        # print(z)
        print("yes")
        z = f'/success/' + mem_id
        print(z)
        return redirect(z)
        return jsonify({'result': 'success'})
    except mysql.connector.IntegrityError as err:
        print("Payment Id already Registered")
        return jsonify({'result': 'failed'})


@app.route('/checking', methods=['POST'])
def checking():
    print(checking)
    pay_id = request.form['pay_id']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="newest"
    )
    mycursor = mydb.cursor()
    mycursor.execute('Select * from payment where pay_id=%s', (pay_id,))
    z = mycursor.fetchall()
    print(z)
    if z == []:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failed'})


@app.route('/success/<d>', methods=['GET', 'POST'])
def hurray(d):
    return render_template('404.html', id=d)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect('/')


#######################################################################################################################
#                                                                                                                     #
#                                                                                                                     #
#                                                ADMIN                                                                #                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#######################################################################################################################
@app.route("/adminpage", methods=['GET', 'POST'])
def adminpafge():
    return render_template('login2.html')


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    username = request.form['username']
    password = request.form['password']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="newest"
    )
    mycursor = mydb.cursor()
    mycursor.execute("Select * from admin where username='" + username + "' and password='" + password + "'")
    account = mycursor.fetchall()
    print(account)
    if account:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="newest"
        )
        mycursor = mydb.cursor()
        mycursor.execute(
            'SELECT register.Name,register.Contact,register.Address,payment.pay_id,payment.payment_date FROM register INNER JOIN payment where register.member_id=payment.member_id;')
        usedata = mycursor.fetchall()
        print(usedata)
        name = []
        contact = []
        Address = []
        Pay_id = []
        date = []

        Final = []
        for i in range(0, len(usedata)):
            name.append(str(usedata[i][0]))
            # Shoulder.append(int(usedata[i][1]))
            contact.append(0 if usedata[i][1] is None else int(usedata[i][1]))
            Address.append(str(usedata[i][2]))
            Pay_id.append(str(usedata[i][3]))
            date.append(str(usedata[i][4]))

        print("========================")
        print(name)
        print(contact)
        print(Address)
        print(Pay_id)
        print(date)

        for i in range(0, len(usedata)):
            z = tuple((name[i], contact[i], Address[i], Pay_id[i], date[i]))
            Final.append(z)
        print(Final)
        # for i in range(0, len(usedata)):
        #     z = dict({
        #         "Date": tarik[i],
        #         "Shoulder": Shoulder[i],
        #         "Chest": chest[i],
        #         "Arms": Arms[i],
        #         "Legs": Legs[i],
        #         "Back_abs": Back_abs[i],
        #     #         "sum": int(Shoulder[i]) + int(chest[i]) + int(Arms[i]) + int(Legs[i]) + int(Back_abs[i])
        #     #     })
        #     #     all.append(z)
        #     # print(all)
        mycursor.execute('Select * from offers')
        offer = mycursor.fetchall()
        print(offer)
        mycursor.execute('Select * from available')
        exe = mycursor.fetchall()
        print(exe)
        return render_template('datatable.html', userdata=json.dumps(Final), offer=offer, exe=exe)
    else:
        render_template('login2.html')


#
#
# @app.route('/sort', methods=['POST'])
# def sort():
#     sorting = request.form['date']
#     count = int(request.form['count'])
#     print(count)
#     count = count + 1
#     print(count)
#     print(sorting)
#     '''SELECT register.Name AS Name,register.Contact AS Contact,register.Address AS Address,payment.pay_id AS pay_id ,payment.payment_date AS payment_date ,payment.amount AS amount FROM register INNER JOIN payment where register.member_id=payment.member_id ORDER By Contact;'''
#     return jsonify({'result': 'success'})

@app.route('/updateexe', methods=['POST'])
def updateexe():
    try:
        name = request.form['name']
        shoulder = request.form['shoulder']
        chest = request.form['chest']
        legs = request.form['legs']
        arms = request.form['arms']
        back_abs = request.form['back_abs']
        print(name)
        print(shoulder)
        print(chest)
        print(legs)
        print(arms)
        print(back_abs)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="newest"
        )
        mycursor = mydb.cursor()
        mycursor.execute(
            'INSERT INTO available (excercise_name, Shoulder, Chest, Legs, Arms, Back_Abs) VALUES ( %s,  %s,  %s,  %s,  %s,  %s)',
            (name, shoulder, chest, legs, arms, back_abs))
        mydb.commit()
        # usedata = mycursor.fetchall()
        # print(usedata)
        # INSERT INTO `available` (`excercise_id`, `excercise_name`, `Shoulder`, `Chest`, `Legs`, `Arms`, `Back_Abs`) VALUES ('37', 'rr', '0', '0', '0', '0', '0');
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'failed'})


@app.route('/updateoffer', methods=['POST'])
def updateoffer():
    try:
        name = request.form['name']
        price = request.form['price']
        nod = request.form['nod']

        print(name)
        print(price)
        print(nod)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="newest"
        )
        mycursor = mydb.cursor()
        mycursor.execute(
            'INSERT INTO offers (offer_name, Amount, No_of_days) VALUES ( %s,  %s,  %s)',
            (name, price, nod))
        mydb.commit()
        # usedata = mycursor.fetchall()
        # print(usedata)
        # INSERT INTO `available` (`excercise_id`, `excercise_name`, `Shoulder`, `Chest`, `Legs`, `Arms`, `Back_Abs`) VALUES ('37', 'rr', '0', '0', '0', '0', '0');
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'failed'})


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/test', methods=['GET', 'POST'])
# def indextest():
#     form = Form()
#     form.city.choices = [(city.id, city.name) for city in City1.query.filter_by(state='CA').all()]
#
#     if request.method == 'POST':
#         city = City1.query.filter_by(id=form.city.data).first()
#         return '<h1>State: {}, City: {}</h1>'.format(form.state.data, city.name)
#
#     return render_template('test.html', form=form)

# @app.route('/city/<state>')
# def citytest(state):
#     cities = City1.query.filter_by(state=state).all()
#
#     cityArray = []
#
#     for city in cities:
#         cityObj = {}
#         cityObj['id'] = city.id
#         cityObj['name'] = city.name
#         cityArray.append(cityObj)
#
#     return jsonify({'cities': cityArray})

# @app.route('/1')
# # @login_required
# def tasks_list():
#     tasks = Task.query.all()
#     today = date.today()
#     date1 = today.strftime("%d/%m/%Y")
#     day = datetime.today().strftime('%A')
#     # print(day)
#     name = "N A M E"
#     membership_left = "membership left"
#     membership_id = 55
#     # day
#     # chest , back
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="ecommerce1"
#     )
#
#     mycursor = mydb.cursor()
#
#     mycursor.execute("select * from city1")
#
#     data = mycursor.fetchall()
#     # print(data)
#     form = Form()
#     form.city.choices = [(city.id, city.name) for city in City1.query.filter_by(state='CA').all()]
#
#     if request.method == 'POST':
#         city = City1.query.filter_by(id=form.city.data).first()
#         return '<h1>State: {}, City: {}</h1>'.format(form.state.data, city.name)
#
#     return render_template("list.html", tasks=tasks, date=date1, day=day, name=name, membership_left=membership_left,
#                            form=form, data=data, membership_id=membership_id)

# @app.route('/task', methods=['POST'])
# def add_task():
#     member = request.form['content']
#     content = request.form['content']
#     if not content:
#         return "ERROR"
#     task = Task(content, member)
#     db.session.add(task)
#     db.session.commit()
#
#     return redirect('/1')

#
# @app.route('/delete/<int:task_id>')
# def delete_task(task_id):
#     task = Task.query.get(task_id)
#     if not task:
#         return redirect('/')
#
#     db.session.delete(task)
#     db.session.commit()
#     return redirect('/1')

# @app.route('/done/<int:task_id>')
# def resolve_task(task_id):
#     task = Task.query.get(task_id)
#
#     if not task:
#         return redirect('/')
#     if task.done:
#         task.done = False
#     else:
#         task.done = True
#
#     db.session.commit()
#     return redirect('/1')

# @app.route('/chomu', methods=["GET", "POST"])
# def chomu():
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="newest"
#     )
#     mycursor = mydb.cursor()
#     if request.method == "POST":
#         membership_id = request.form.get("membership_id")
#         # mycursor.execute("select * from users where userID ="+ membership_id")
#         mycursor.execute(
#             "select * from users where userID='" + membership_id + "'")
#         print(1)
#         return "bye"
#     else:
#         return "hello"

# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash("You need to login first")
#             return redirect(url_for('login_normal'))
#
#     return wrap
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root@localhost'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'ecommerce1'
#
# mysql = MySQL(app)
# ===============================================================================
#                                   EXAMPLE
# ===============================================================================
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="ecommerce1"
# )
# mycursor = mydb.cursor()
# # Executing SQL Statements
# mycursor.execute("select * from orders")
# # Saving the Actions performed on the DB
# data = mycursor.fetchall()
# print(data)
# =================================================================================
# Closing the cursor
# =================================================================================
# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text)
#     member = db.Column(db.Integer)
#     done = db.Column(db.Boolean, default=False)

#
#     def __init__(self, content, member):
#         self.content = content
#         self.member = member
#         self.done = False
#
#     def __repr__(self):
#         return '<Content %s>' % self.content
#
#
# class City1(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     state = db.Column(db.Text)
#     name = db.Column(db.Text)
#
#
# class Form(FlaskForm):
#     state = StringField()
#     # 'state', choices = [('CA', 'California'), ('NV', 'Nevada'), ('LG', 'Legs'), ('sh', 'Shoulder'),
#     #                     ('st', 'Stomach'), ('hd', 'hands'), ('ct', 'chest')]
#     city = SelectField('city', choices=[])
# @app.route('/new', methods=['GET', 'POST'])
# def new():
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="newest"
#     )
#     mycursor = mydb.cursor()
#     if request.method == "POST":
#         name = request.form.get("name")
#         number = request.form.get("number")
#         address = request.form.get("address")
#
#         print(1)
#         print(name)
#         print(address)
#         print(number)
#         mycursor.execute('insert into register (Name,Contact,Address) values (%s,%s,%s)',
#                          (name, str(number), address,))
#         mycursor.execute('SELECT member_id FROM register WHERE name = %s and contact= %s and address = %s',
#                          (name, number, address))
#         z = [x[0] for x in mycursor.fetchall()]
#         print("to kar na")
#         print(z)
#
