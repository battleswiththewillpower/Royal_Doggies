from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.doggie import Doggie
from flask_app.models.newsletter import Newsletter
from flask_app.models.contactform import Contactform


@app.route('/email/create', methods=['POST'])
def create_newsletter():
    print(request.form)

    # data={
    #         'email':request.form['email'],
    #         'doggies': Doggie.get_all()
    # }
    Newsletter.create_newsletter(request.form)

    if not Newsletter.validate_newsletter(request.form):       
        return redirect('/')
    # return redirect(f'/thankyou/{request.form["doggie_id"]}')

# FIX THE FORM SINCE ONCE THE BUTTON IS PRESSED IT AUTOMAICALLY CREATES IT IN THE DB
# CONTACT FROM ON BROOKLUNS PAGE
@app.route('/user/create', methods=['POST'])
def user_create():
    # print(request.form)
    
    # CHECK THIS OUT TO SEE IF THIS IS THE ISSUE
    Contactform.create_contact(request.form)
# Validation works
    if not Contactform.validate_contact_info(request.form):       
        return redirect('/brooklyn')

    
    return redirect(f'/thankyou/{request.form["doggie_id"]}')

# THANK YOU NOTE TO USER
@app.route('/thankyou/<int:id>')
def thankyou_page(id):
    context = {
        
        'doggie' : Doggie.get_one_user({'id':id})
        
    }
    # if 'user_id' not in session:
    #     return redirect('/')


    return render_template('thankyou.html', **context)

# CONTACT PAGE
@app.route('/new')
def new_contact():
    context = {
            # 'id': session['doggie_id'],
            'doggies': Doggie.get_all()
            
        }
    return render_template('contact-us.html', **context)

# FIX THE FORM SINCE ONCE THE BUTTON IS PRESSED IT AUTOMAICALLY CREATES IT IN THE DB
# for contact page
@app.route('/user/createcontact', methods=['POST'])
def user_create_contactform():
    # print(request.form)
    Contactform.create_contact(request.form)
# Validation works
    if not Contactform.validate_contact_info(request.form):       
        return redirect('/new')

    return redirect(f'/thankyou/{request.form["doggie_id"]}')