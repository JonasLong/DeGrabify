from flask import Flask, Response, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.wrappers import response
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import time
from argparse import ArgumentParser

# set up Flask
app = Flask(__name__)

# Parse command line args
parser = ArgumentParser(description="Flask server for DeGrabify")
parser.add_argument("-d", "--database", dest="database",
                    help="path to the database", metavar="FILE", default="sites.json")
parser.add_argument("-p", "--proxy-lvl", dest="proxy_lvl",
                    help="level of reverse proxies for Flask ProxyFix middleware", metavar="NUM", default="0")
args = parser.parse_args()
app.config["db"]=args.database
proxy_lvl = args.proxy_lvl

# TODO handle reverse proxy
#app.wsgi_app = ProxyFix(
#    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
#)

# set up the TinyDB (readonly)
db = TinyDB(app.config["db"], storage=CachingMiddleware(JSONStorage), sort_keys=True, indent=4, separators=(',', ': '))
Domain = Query()


@app.route("/")
def home():
    stylesheet=app.url_for('static', filename='style.css')
    return render_template("homepage.html", base_domain="http://127.0.0.1:5000", stylesheet=stylesheet)

@app.route("/ublacklist")
def ublacklist():
    return as_raw(format_list(get_filter_list(), "#", "*://*.{site}/*"))

@app.route("/ublock")
def ublock():
    return as_raw(format_list(get_filter_list(), "!", "||{site}^$document\nduckduckgo.com,bing.com##a[href*=\"{site}\"]:upward(li):remove()\ngoogle.com##a[href*=\"{site}\"]:upward(2):remove()\n"))

@app.route("/hosts")
def hosts():
    return as_raw(format_list(get_filter_list(), "#", "0.0.0.0 {site}"))


    """Formats the provided text as plaintext Flask response
    """
def as_raw(text: str) -> Response:
    response = app.make_response(text)
    response.status_code = 200
    response.mimetype = "text/plain"
    return response

    """Returns a formatted list of domains along with a commented header

    @param site_list: List of fully-qualified domain names
    @param comment_chr: the comment character for this format type
    @prama fmtstr: a format string for domain in the list, using the substitution {site}
    """
def format_list(site_list: list[str], comment_chr: str, fmtstr: str, full_header=True) -> str:
    access_time = time.asctime()
    utime = update_time()

    if utime is None:
        return f"{comment_chr} No updates have run yet or the database has been cleared. Contact the administrator.\n{comment_chr} DB path: {app.config["db"]}"

    if full_header:
        comments = f"""Title: Grabify Domain List
Expires: 1 day
Description: Dynamically updated list of in-use Grabify domains, to block IP grabbers
Last modified: {utime}
Accessed at: {access_time}

Enjoy!
"""
    else:
        comments = f"Grabify Domain List"

    commented_header=("\n".join((comment_chr+" "+i) for i in (comments.split("\n"))))    

    site_str = "\n".join(fmtstr.format(site=i) for i in site_list)

    return commented_header+ "\n\n" + site_str

    """Retrieves the last updated time from the database

    @returns An asctime formatted last update time, or None if not found
    """
def update_time() -> str|None:
    updateTable = db.table("lastUpdated").all()

    if len(updateTable) != 1:
        return None
    else:
        return f"{updateTable[0]["lastUpdated"]}"

def get_filter_list() -> list[str]:
    access_time = time.asctime()

    # format the domains as a newline-separated list, as a string
    sites: list[str] = [
        doc["Domain"] for doc in iter(db.table("sites"))
    ]
    # return the list of domains
    return sites


if __name__ == "__main__":
    #print("This script should be run with Flask. Printing filter list for debugging purposes...")
    #response=ublacklist()
    #print("\nReturned page data:\n--------------")
    #print(bytes.decode(response.data))
    #print("--------------")
    app.run(host="0.0.0.0")
 