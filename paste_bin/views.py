import random
import string

from flask import Flask, render_template, redirect, session

from .PasteBin import PasteBin
from .forms import PasteForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "".join(
    random.sample(string.ascii_letters + string.digits, 16)
)
app.config['SESSION_PERMANENT'] = False
root = "http://0.0.0.0:8080"  # "http://paste.loopy.tech"


def is_robot():
    if 'count' in session:
        session['count'] += 1
    else:
        session['count'] = 0
    return session['count'] > 20


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect("/paste")


@app.route("/paste", methods=["GET", "POST"])
def set():
    form = PasteForm()
    if is_robot():
        return render_template("pastebin.html", msg="Due to frequent operations, you are currently banned from server.")

    if form.validate_on_submit():
        if PasteBin.set_record(**form.data):  # succeed
            return redirect("/info/{}".format(form.data["record_title"]))
        else:  # title taken
            return render_template(
                "pastebin.html",
                form=form,
                msg="Failed: Title [{}] has been taken, try another one!".format(
                    (form.data["record_title"])
                ),
            )
    else:
        return render_template("pastebin.html", form=form)


@app.route("/<title>", methods=["GET", "POST"])
def get(title):
    if is_robot():
        return render_template("pastebin.html", msg="Due to frequent operations, you are currently banned from server.")

    record = PasteBin.get_record(title)
    if record is None:
        return render_template("record.html", msg="Failed! No record has been found!")
    elif record.type == "url":
        return redirect(record.content)
    else:
        return render_template(
            "record.html", content=record.content, expire=record.expire_info
        )


@app.route("/info/<title>", methods=["GET", "POST"])
def info(title):
    if is_robot():
        return render_template("pastebin.html", msg="Due to frequent operations, you are currently banned from server.")

    record = PasteBin.get_record(title)
    if record is None:
        return render_template("record.html", msg="Failed! No record has been found!")
    elif record.type == "url":
        return render_template(
            "record.html",
            url="{}/{}".format(root, title),
            content=record.content,
            expire=record.expire_info,
        )
    else:
        return render_template(
            "record.html",
            url="{}/{}".format(root, title),
            content=record.content,
            expire=record.expire_info,
        )
