import login_form
import flask
import utils
from flask_login import login_required, login_user, logout_user
import globalss as gb
from globalss import app
import apsw
from apsw import Error


# This method is called whenever the login manager needs to get
# the User object for a given user id
@gb.login_manager.user_loader
def user_loader(user_id):
    if not utils.is_username_taken(user_id):
        print(f"Somebody tried to login a non existent user")
        return 

    user = utils.User()
    user.id = user_id
    return user



@app.route('/login', methods=['GET', 'POST'])
def login():
    message=""
    form = login_form.LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(flask.request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if not utils.is_username_valid(username): 
            message = "Username or password wrong"
        elif utils.check_user(username, password): 
            user = user_loader(username) 
            # automatically sets logged in session cookie
            login_user(user)
            flask.session['username'] = user.id
            gb.logging.info(f"User: {flask.session['username']} is logging IN")
            print(flask.session)

            flask.flash('Logged in successfully.')
            next = flask.request.args.get('next')

            if not utils.is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))
        else:
            message = "Username or password wrong"
    return flask.render_template('./login.html', form=form, message=message)


@app.route("/logout")
@login_required
def logout():
    gb.logging.info(f"User: {flask.session['username']} is logging OUT")
    logout_user()
    flask.flash('You have successfully logged yourself out.')
    return flask.redirect('/login')


@app.route("/register", methods=["GET", "POST"])
def register():
    message=""
    form = login_form.LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        #print(flask.request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        
        if not utils.is_username_valid(username):
            message = "Username not valid, should contains just letters, numbers and '.' or '_'"
        elif utils.is_username_taken(username):
            message = "Username already taken!"
        elif not utils.is_password_strong(password):
            message = """Passowrd not strong enough. 8 character, should include
             one upper case one lower case and a digit."""
        else:
            utils.register(username, password)
            gb.logging.info("Succesful registration for {username}")

            # login the just registered user
            user = user_loader(username) 
            login_user(user)
            flask.session['username'] = user.id
            gb.logging.info(f"User: {flask.session['username']} is logging IN")

            flask.flash('Logged in successfully.')
            
            next = flask.request.args.get('next')
            
            if not utils.is_safe_url(next):
                return flask.abort(400)
        
            return flask.redirect(next or flask.url_for('index'))
    
    return flask.render_template('./register.html', form=form, message=message)