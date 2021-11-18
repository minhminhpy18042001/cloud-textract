from flask import Flask, request, render_template
import json
import boto3

textractclient = boto3.client("textract", aws_access_key_id="ASIA47S4R7F2CGREHWLH",
                              aws_secret_access_key="Mp4q2akqvnzcy0C5vAKMZpu4gdhyeymUiYa1tRC3",
                              aws_session_token="FwoGZXIvYXdzEBgaDKypzSMJapZPYx/5IyLPAUviEsK/TuLM52HFqIWijZO9oG5/6eqZ4vscIleBJjFEno2o4ax6xYhP4KSjpqn2acbGpNdr8GI39OGIFoMeKpreETD0iw6JEpyAIpIq0ol98OnDf5hqVaZzzmh1OF4+hc51n1bsxiYUFXAfafVOfKnEQ2rtRcVxu6efuslJvsqa5+5rERKbn1XAyCJvrUdPfwmwmHvQBDc54YL5qu3xO4d1AIl5kUWZasZ75VBwRAfFmyjExTzW0MbBuw3B0Tz2MhyFK23Z4/Ws54stp8sIjyju0tmMBjItlr2O8qP2m8iLgnAiA9+Wbm1flCSLA9M2fMjYedtIq+4cV8YkSuP94pKwGJZg")


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
