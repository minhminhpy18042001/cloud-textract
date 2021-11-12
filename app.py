from flask import Flask, request, render_template
import json
import boto3

textractclient = boto3.client("textract", aws_access_key_id="ASIA47S4R7F2I2HLMCJH",
                              aws_secret_access_key="yuiNVay4P0+7WTsnBpMiRtUKgceiakCEEwt6+UZE", region_name="us-east-1")


app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html", jsonData=json.dumps({}))


@app.route("/extract", methods=["POST"])
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


app.run("0.0.0.0", port=5000, debug=True)
