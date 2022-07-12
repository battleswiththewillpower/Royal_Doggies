from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.doggie import Doggie
from flask_app.models.contactform import Contactform
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/sign')
def log_reg ():
    if 'user_id' in session:
        return redirect('/success')
    return render_template('reg_login.html')


@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/')

 
    return render_template('dashboard.html', user=User.get_one({'id':session['user_id']}), doggies =Doggie.get_all(), users=User.get_all())


@app.route('/register', methods=['POST'])
def register():
    
    if not User.validate_user_login(request.form):
        return redirect('/')

    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])

    }
    id = User.create_user(data)
    session['user_id'] = id
    print(request.form)
    # user.User.create(request.form)

    return redirect("/success")

@app.route('/admin')
def log ():
    # FIX ADMIN LOGIN MAKE SURE IT REDIRECTS TO THE ADMIN
    # if admin
    if 'user_level' == 'admin' and 'user_id' in session:
        print('admin worked!')
        return redirect('/admin')
    # or if user
    if  'user_level' == 'normal' and 'user_id' in session:
        print('All users worked')
        return redirect('/success')
    return render_template('reg_login.html')



@app.route('/login', methods=['POST'])
def login():
    log_user = User.get_by_email(request.form)

    if not log_user:
        flash("Wrong Email")
        return redirect('/')
    if not bcrypt.check_password_hash(log_user.password, request.form['password']):
        flash("Wrong Password")
        return redirect('/')
    session['user_id'] = log_user.id
    
    return redirect('/success')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/sign')


# @app.route('/admin/<int:id>')
# def admin(id):

#     return render_template('admindashboard.html', user=User.get_one({'id':session['user_id']}), doggies =Doggie.get_all(), users=User.get_all())
@app.route('/admin')
def admin():

    return render_template('admindashboard.html',user=User.get_one({'id':session['user_id']}), doggies =Doggie.get_all(), users=User.get_all(), contact=Contactform.get_all_contact())


# ADD CRUD

# EDIT USER INFO
@app.route('/user/edit/<int:id>')
def edit_user(id):
    data ={
        "id":id
    }
    return render_template('editUser.html', user=User.get_one(data))

# UPDATE INFO
@app.route('/user/update/<int:id>', methods=['POST'])
def update(id):
    update_data={
            'id': id,
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'password':request.form['password'],
            'description':request.form['description']
            # 'user_id':session['user_id']
    }

    if 'user_id' not in session:
        return redirect('/')
        
        # this line of code needs to be refactered to fit the unique changes
    if not User.validate_user_login(request.form):   
        return redirect(f'/user/edit/{update_data["id"]}')

    User.update(update_data)
    return redirect('/success')

@app.route('/user/destroy/<int:id>')
def destroyUser(id):
    data ={
        "id":id
    }
    User.destroy(data)
    return redirect('/admin')

if __name__=="__main__":
    app.run(debug=True)