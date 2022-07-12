from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.doggie import Doggie


@app.route('/')
def home_dog_page():

    return render_template('index.html')
    # , doggie=doggie.Doggie.get_one({'id':session['doggie_id']}), users=user.User.get_all()



@app.route('/brooklyn')
def brooklyn():
    context = {
        'doggies': Doggie.get_all()
    }
    return render_template('dog-fostering.html', **context)


@app.route('/bella')
def success_story ():
    
    return render_template('bella.html')

@app.route('/doggie/new')
def new_doggie():
    name_data={
        'id': session['user_id']
    }
    return render_template("add_doggie.html", user=User.get_one(name_data))

@app.route('/doggie/create', methods=['POST'])
def doggie_create():
    # print("create user")
    data={
           'name':request.form['name'],
            'breed':request.form['breed'],
            'age':request.form['age'],
            'location':request.form['location'],
            'color':request.form['color'],
            'disability':request.form['disability'],
            'user_id':session['user_id']
    }
    if 'user_id' not in session:
        return redirect('/')
    if not Doggie.validate_doggie_info(request.form):
        return redirect('/doggie/new')
    # print(request.form)
    Doggie.create(data)
    return redirect('/success')


@app.route('/doggie/edit/<int:id>')
def edit_dog(id):

    
    return render_template('editdog.html',dog=Doggie.get_one({'id':id}),user=User.get_one({'id':session['user_id']})) 


@app.route('/doggie/update/<int:id>', methods=['POST'])
def update_dog(id):
    update_data={
            'id': id,
            'name':request.form['name'],
            'breed':request.form['breed'],
            'age':request.form['age'],
            'location':request.form['location'],
            'color':request.form['color'],
            'disability':request.form['disability'],
            'user_id':session['user_id']
            
            
    }
    if 'user_id' not in session:
        return redirect('/')
    if not Doggie.validate_doggie_info(request.form): 
        return redirect(f'/doggie/edit/{update_data["id"]}')

    Doggie.update(update_data)
    return redirect('/success')


@app.route('/admin')
def admin_page ():
    
    return render_template('admin-login.html')


@app.route('/success')
def successful_login():
    

    return render_template('admin-page.html',users=user.User.get_all_user(), doggies = doggie.Doggie.get_all())

@app.route('/doggies')
def allDoggies():
    
    return render_template('alldoggies.html', doggies = doggie.Doggie.get_all())


@app.route('/doggie/destroy/<int:id>')
def destroy(id):
    data ={
        "id":id,
    }
    Doggie.destroy(data)
    return redirect('/success')

@app.route('/doggie/select/<int:id>')
def display_dog(id):
    data ={
        "id":id,

    }

    user_data={
        'id':session['user_id']

    }
    return render_template('displaydog.html', dog=Doggie.get_one(data),user=User.get_one(user_data)) 

if __name__=="__main__":
    app.run(debug=True)