from flask import Flask, request, render_template, send_file
import json
import boto3
import cgi
import textract_python_table_parser
account_id = ""
account_key = ""
account_token = ""


def client():
    global account_id
    global account_key
    global account_token
    print(account_id, account_key, account_token)
    client = boto3.client("textract", aws_access_key_id=account_id,
                          aws_secret_access_key=account_key,
                          aws_session_token=account_token,
                          region_name='us-east-1')
    return client


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
    global account_id
    global account_key
    global account_token
    global textractclient
    account_id = request.form.get("aws_id")
    account_key = request.form.get("aws_key")
    account_token = request.form.get("aws_token")
    #print(account_id, account_key, account_token)
    try:
        with open('test1.png', 'rb') as file:
            binaryFile = file.read()
        textractclient = client()
        response = textractclient.detect_document_text(
        Document={
            'Bytes': binaryFile
        }
    )
        return render_template("index.html", jsonData=json.dumps({}))
    except:
        print("Error key")
        return render_template("home.html")


@ app.route("/extracttext", methods=["POST"])
def extractImage():
    file = request.files.get("filename")
    binaryFile = file.read()
    textractclient = client()
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
    textractclient = client()
    file = request.files.get("filename")
    extractedText = textract_python_table_parser.use(file, textractclient)
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
