from flask import Flask, request, render_template, send_file
import json
import boto3
import cgi
import textract_python_table_parser


textractclient = textract_python_table_parser.get_key_AWS()


app = Flask(__name__)


@ app.route("/", methods=["GET"])
def main():
    extractedText = ""
    responseJson = {

        "text": extractedText
    }
    return render_template("home.html", jsonData=json.dumps(responseJson))


@ app.route("/login", methods=["POST"])
def login():
    aws_id = request.form.get("aws_id")
    aws_key = request.form.get("aws_key")
    aws_token = request.form.get("aws_token")
    print(aws_id, aws_key, aws_token)
    return render_template("index.html", jsonData=json.dumps({}))


@ app.route("/extracttext", methods=["POST"])
def extractImage():
    file = request.files.get("filename")
    binaryFile = file.read()
    response = textractclient.detect_document_text(
        Document={
            'Bytes': binaryFile
        }
    )
    extractedText = ""
    for block in response['Blocks']:
        if block["BlockType"] == "LINE":
            # print('\033[94m' + item["Text"] + '\033[0m')
            extractedText = extractedText+block["Text"]+" "

    responseJson = {

        "text": extractedText
    }
    print(responseJson)
    return render_template("index.html", jsonData=json.dumps(responseJson))


@ app.route("/extracttable", methods=["POST"])
def extractTable():
    file = request.files.get("filename")
    extractedText = textract_python_table_parser.use(file)
    responseJson = {

        "text": extractedText
    }
    print(responseJson)
    return render_template("index.html", jsonData=json.dumps(responseJson))


@app.route('/download')
def download_file():
    file = "output.csv"
    return send_file(file, as_attachment=True)


app.run("0.0.0.0", port=5000, debug=True)
