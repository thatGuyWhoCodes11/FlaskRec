from flask import Flask, jsonify, send_file, redirect
import flask as fl
import imageRec as IMGR
from serve_pil_image import serve_pil_image
app = Flask("__name__")
app.config['UPLOAD_FOLDER'] = "./static/images"


@app.route("/", methods=['GET', 'POST'])
def welcome():
    if (fl.request.method == "POST"):
        img = fl.request.files["image"]
        drawnImage = IMGR.drawRectangle(img)
        drawnImage.save("./static/images/drawnImage.jpg")
        return redirect("/registerFaces")
    fl.url_for('static', filename='welcome.js')
    return fl.render_template("welcome.html")


@app.route("/registerFaces", methods=['GET', 'POST'])
def registerFaces():
    if (fl.request.method == "POST"):
        if(not fl.request.files):
           data=fl.request.get_json(force=True)
           print(data)
           IMGR.editFacesInfo(data["faceInfos"])
           return jsonify({"message":"success!"})
        image = fl.request.files["image"]
        faceIds = IMGR.addFaces(image)
        drawnImage = IMGR.drawRectangle(image)
        drawnImage.save("./static/images/drawnImage.jpg")
        return fl.jsonify({"faceIds":faceIds})
    return fl.render_template("registerFaces.html")


@app.route("/recognizeFaces", methods=["GET", "POST"])
def recognizeFaces():
    if (fl.request.method == "POST"):
        img = fl.request.files["image"]
        drawnImage = IMGR.drawRectangle(img)
        drawnImage.save("./static/images/drawnImage.jpg")
        results = IMGR.recognizeFaces(img)
        return fl.jsonify({"results":results})
    return fl.render_template("recognizeFaces.html")


app.run(port=9000)
