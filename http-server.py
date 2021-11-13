from flask import Flask, render_template, make_response, request, send_from_directory
import hashlib
import uuid
import time
import random
from cryptography.fernet import Fernet

app = Flask(__name__, static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

private_key = "Q@!NF0T3CH"
enkey = "Rq6jreLf2EmkllCuzg1DNC7FLnyytt6Q2f4tweo3sDo="
fernet = Fernet(enkey)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
def splash():
    return send_from_directory("static", "index.html")

@app.route("/intro")
def home():
    return render_template('landing.html', bct={})

@app.route("/c/<cid>")
def landing(cid):
    zs = request.cookies.get("_zZs")
    cid_in_request = zs.split(".")[2]
    p = int(zs.split(".")[1])%10
    b = bct(cid)
    if not validate_request(cid):
        error_response = make_response(render_template('validation-error.html', checkpoint_page_id=cid_in_request, bct={}))
        error_response.status_code = 400
        return error_response
    return make_response(render_template(cid+".html", cookie=zs, bct=b, p=p))

@app.route("/start")
def start():
    return launch_response("c1")

@app.route("/l/<cid>")
def launcher(cid):
    return launch_response(cid)

@app.route("/r/<cid>", methods=['POST'])
def responder(cid):
    zs = request.cookies.get("_zZs")
    cid_in_request = zs.split(".")[2]
    if not validate_request(cid):
        error_response = make_response(render_template('validation-error.html', checkpoint_page_id=cid_in_request, bct={}))
        error_response.status_code = 400
        return error_response
    # validate challenge response
    if(globals()["response_" + cid]()):
    # if response success
        return launch_response(next_cid())
        
    error_response = make_response(render_template('validation-error.html', checkpoint_page_id=cid_in_request, bct={}))
    error_response.status_code = 400
    return error_response
    # error page

@app.route("/j/not_a_bot.js")
def not_a_bot_js():
    words = "Lorem ipsum dolor sitamet consectetur adipiscing elita seddo eiusmod tempor incididunt labore etdolore magna aliqua Utenim adminim veniam quisn osrud exerci tation ullamco laboris nisiut aliquip exear commodo consequat Duist autez irure dolorin repreh enderit invol uptate velit essecillum dolore eufugiat nulla pariatur Excepteur sintoc caecat cupidatat nonpr oident suntin culpaqui officia deserunt mollit animid estla borum zaaze eatna itasx".split(" ")
    word = words[random.randint(0,59)][0:5].lower()
    response = make_response(render_template('not_a_bot.js', word=word))
    response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    return response

def bct(cid):
    return {"map": len(route), "curr": route.index(cid)}

# challenge handlers
def validate_request(cid):
    zs = request.cookies.get("_zZs")
    cid_in_request = zs.split(".")[2]
    timestamp_in_request = zs.split(".")[1]
    public_key_in_request = zs.split(".")[3]
    if(cid != cid_in_request):
        return False
    # if(current_timestamp - int(timestamp_in_request) < 60):
    #    return False
    if(zs != signature(cid, timestamp_in_request, public_key_in_request)):
        return False
    return True

def signature(cid, timestamp, public_key):
    #timestamp = str(round(time.time()))
    sig = private_key + timestamp + public_key + cid
    sig = hashlib.sha256(bytes(sig, 'utf-8')).hexdigest()
    return sig+"." + timestamp+"."+cid+"."+public_key

def launch_response(cid):
    # set target page state
    res = make_response()
    public_key = str(uuid.uuid4())
    zs = signature(cid, str(round(time.time())), public_key)
    res.set_cookie("_zZs", value=zs)
    # redirect to target page
    res.headers['location'] = "/c/" + cid
    res.status_code = 301
    res.autocorrect_location_header = False
    return res

def next_cid():
    cid_in_request = request.cookies.get("_zZs").split(".")[2]
    return route[route.index(cid_in_request) + 1]

route = [
        "c1",
        "a_video",
        "crystal_maze",
        "maps",
        "not_a_bot",
        "socket_gate",
        "treasure"
        ]

def response_c1():
    return True

def response_maps():
    dot_coords = [float(num_string) for num_string in request.form["mapsChallengePath"].split(",")]
    
    india_coords = [388, 80, 355, 116] #[coords arranged as top right then bottom left]
    us_coords = [164, 58, 79, 93]
    
    isIndia = (dot_coords[0] > india_coords[2] and dot_coords[0] < india_coords[0] \
            and dot_coords[1] < india_coords[3] and dot_coords[1] > india_coords[1])

    isUSA =  (dot_coords[0] > us_coords[2] and dot_coords[0] < us_coords[0] \
            and dot_coords[1] < us_coords[3] and dot_coords[1] > us_coords[1])
    return (isIndia or isUSA)
    
def response_not_a_bot():
    return request.form["notABotCaptchaResponse"] == request.form["notABotCaptchaWord"][::-1]

def response_a_video():
    mute = request.form["aVideoStatus"].split(",")[0]
    played = request.form["aVideoStatus"].split(",")[1]
    status = request.form["aVideoStatus"].split(",")[2]
    if(mute != "true"):
        return False
    if(float(played) < 8):
        return False
    if(status != "1"):
        return False
    return True

def response_socket_gate():
    try:
        zs = request.cookies.get("_zZs")
        ezs = fernet.decrypt(request.form["socketGateMessage"].encode()).decode()
        if(zs == ezs):
            return True
    except Exception as e:
        print(e)
    return False

def response_crystal_maze():
    direction = request.form["crystalMazePath"]
    if not direction.startswith("r"):
        return False
    if not direction.endswith("r"):
        return False
    if(len(direction)<30):
        return False
    return True

if __name__ == "__main__":
    app.run(host="0.0.0.0")
