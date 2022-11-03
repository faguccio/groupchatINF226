from globalss import app
import globalss as gb
import flask
import utils
from json import dumps, loads
import apsw
from apsw import Error
import datetime
import markupsafe

@app.route('/favicon.ico')
def favicon_ico():
    return flask.send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/favicon.png')
def favicon_png():
    return flask.send_from_directory(app.root_path, 'favicon.png', mimetype='image/png')



@app.route('/')
@app.route('/index')
@app.route('/index.html')
@gb.login_required
def index():
    return flask.send_from_directory(app.root_path,
                        'index.html', mimetype='text/html')



@app.get("/messages/myids")
@gb.login_required
def get_my_ids():
    user = flask.session['username']
    ids = utils.fetch_myids(user)
    return ids

@app.get("/messages")
@gb.login_required
def get_messages():
    user = flask.session['username']
    messages = utils.fetch_messages(user)
    if messages == []:
        return utils.format_messages_html([[f"Empty", f"No body is texting you..."]])
    
    output = []

    for mess in messages:
        print(mess)
        output.append(utils.format_message(mess))

    return utils.format_messages_html(output)


@app.get("/messages/ID")
@gb.login_required
def get_message_from_id():
    query = flask.request.args.get('q') or flask.request.form.get('q')
    try:
        query = int(query)
    except:
        return f"!Error, invalid message ID"
    
    user = flask.session['username']
    message = utils.fetch_message_id(query, user)
    if message == []:
        return f"!I don't think you can see that message..."
    if len(message) > 1:
        return f"!Something really bad happend"
    
    print(message[0])
    return utils.format_messages_html([utils.format_message(message[0])])
    

@app.route('/new', methods=['POST', 'GET'])
@gb.login_required
def new_message():
    # I wish I could use the UNIX epoch as a timestamp but it's probably too hardcore
    timestamp = datetime.datetime.now().__str__()
    print(flask.session)
    username = flask.session['username']
    # test if it works removing the form.get (javascript should do a fetch but i dunno)
    message = flask.request.args.get('message') or flask.request.form.get('message')
    message = markupsafe.escape(message)

    replyId = flask.request.args.get('replyId') or flask.request.form.get('replyId')
    if replyId == None:
        replyId = -1
    else:
        try:
            replyId = int(replyId)
        except:
            return f"Invalid reply ID"

    recipients = flask.request.args.get('recipients') or flask.request.form.get('recipients')
    # recipients can by either a username or #all (which is not a valid username)
    if recipients != gb.ALL_address and ( not utils.is_username_valid(recipients) or not utils.is_username_taken(recipients)):
            return f"Invalid recivier (it doesn't exists)"
    
    if not username or not message or not recipients:
        return f"Error, missing a field"
    
    return utils.insert_message(username, timestamp, message, replyId, recipients)


@app.get('/highlight.css')
def highlightStyle():
    resp = flask.make_response(gb.cssData)
    resp.content_type = 'text/css'
    return resp