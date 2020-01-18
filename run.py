from paste_bin.views import app

root = "http://0.0.0.0:8080"  # "http://paste.loopy.tech"

app.run(host="0.0.0.0", port=8080, debug=True)
