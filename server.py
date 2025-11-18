from flask import Flask, url_for, render_template, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import time

# set up the TinyDB (readonly)
db = TinyDB('sites.json', storage=CachingMiddleware(JSONStorage), sort_keys=True, indent=4, separators=(',', ': '))
Domain = Query()

# set up Flask
app = Flask(__name__)
# TODO handle reverse proxy
#app.wsgi_app = ProxyFix(
#    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
#)

@app.route("/")
def home():
    stylesheet=app.url_for('static', filename='style.css')
    return render_template("homepage.html", base_domain="https://example.com", stylesheet=stylesheet)
    #with open("homepage.html") as homepage:
    #    return homepage.read()

@app.route("/ublacklist")
def ublacklist():
    return as_raw(format_list("#"))

@app.route("/ublock")
def ublock():
    return as_raw(format_list("!"))

@app.route("/hosts")
def hosts():
    return as_raw(format_list("#", header=False))

def as_raw(text):
    response = make_response(text, 200)
    response.mimetype = "text/plain"
    return response

def format_list(comment_chr: str, header = True):
    access_time = time.asctime()
    utime = update_time()

    if utime is None:
        return f"{comment_chr} No updates have run yet or the database has been cleared. Contact the administrator."

    if header:
        comments = f"""Title: Grabify Domain List
Expires: 1 day
Description: Dynamically updated list of in-use Grabify domains, to block IP grabbers
Last modified: {utime}
Accessed at: {access_time}

Enjoy!
"""
    else:
        comments = f"Grabify Domain List"

    return ("\n".join((comment_chr+" "+i) for i in (comments.split("\n")))) + "\n\n" + filter_list()

def update_time():
    updateTable = db.table("lastUpdated").all()

    if len(updateTable) != 1:
        return None
    else:
        # return the list of domains
        return f"{updateTable[0]["lastUpdated"]}"

def filter_list():
    access_time = time.asctime()

    # format the domains as a newline-separated list, as a string
    sites: str = "\n".join(
        doc["Domain"] for doc in iter(db.table("sites"))
        )

    updateTable = db.table("lastUpdated").all()

    if len(updateTable) != 1:
        return "# No updates have run yet or the database has been cleared. Contact the administrator."
    else:
        # return the list of domains
        return sites

if __name__ == "__main__":
    print("This script should be run with Flask. Printing filter list for debugging purposes...")
    final_list=ublock()
    print("\nReturned page data:\n--------------")
    print(final_list)
