from flask import Flask, request, render_template
import json
import boto3

textractclient = boto3.client("textract", aws_access_key_id="ASIA47S4R7F2GVZ4C7FT",
                              aws_secret_access_key="9rfoYItgVrCaFXKlfi524Z+lWcYHW5MYgGF6xhHg",
                              aws_session_token="FwoGZXIvYXdzEKn//////////wEaDLtXOu5PTV15kz9dxyLPAfEnLe/Hvl+q2Wgs5BdoZrDe/Kc3rNbJKxB0tIffa7EPzBHlEF0DSPrFeMfaY4BEAgbh29sV6bpSYxjVxcVTjoAAvE7/al9MeGl6weAFq1bx2KOXCrZnCWl6vSS0xd6MZ84Ql+1GP5+b3g0zKbQLkQm8bVktT+LKm9GjyjVYCTPhB5QW+Lx3zFqI44YICjfv9w63tcPEww1qwhyAOToPwcUO8XviMOYnQbD7qN8se5/bOjXDhiF/WdEw8SNYISJCeknJaTNcWoZ2V4IMsXXM9CiCtvmMBjItHltksAfBKbRS6J+huENVkij3Bm539zasvkiDcnqJIu8/2H61GUbbAfihtAvp")


app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    extractedText = ""
    responseJson = {

        "text": extractedText
    }
    return render_template("index.html", jsonData=json.dumps(responseJson))


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
