from flask import Flask, request, render_template
import json
import boto3

textractclient = boto3.client("textract", aws_access_key_id="ASIA47S4R7F2BFBS4PXP",
                              aws_secret_access_key="qvfJWGZ7YegyqdHvAO1OAKs1XZGoYsyqAzw/Tb/s",
                              aws_session_token="FwoGZXIvYXdzEBwaDCnzCUmxmBD3d7AqoSLPAR9nxk9iZMwjqL848WSAt7BgM+gu2Oi5pR37Qfmqsduh/Cr8mA37AUIrYGD5CYuKRNa+Zb/LEb2+HvF8b4C0gMn0HkxjaqltkSFLmUNSjTfM+aryezw/z4AdpqlRUOBFNFchE3QEuV5K3KgbnVRB1jNinDgex9nQzURSp3jcieRuFacTHp37EAVTk9g4D9Ap7P6mWzT712eTuh41QHnHt7qsLuJlWEFnbxdEpdS71bg66JoRS1LfgJQGE5X2DQFMj/sd5zhXNuhO3BAvU5uZ4SibtNqMBjItS+kSZsWhl+VbpDmttGT5lvpR+cek2DGv47lkydlVaVaGZHuLugBxFejhUOLV")


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
