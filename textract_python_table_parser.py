import webbrowser
import os
import json
import boto3
import io
from io import BytesIO
import sys
from pprint import pprint
import pandas as pd
import html_to_json
from trp import Document


def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}

                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '
    return text


def get_key_AWS():
    client = boto3.client("textract", aws_access_key_id="ASIA47S4R7F2PFDRBFTN",
                          aws_secret_access_key="iToFXECvjXOPRWwAKMwCzqBkW8Lu1iKEBkELQCRI",
                          aws_session_token="FwoGZXIvYXdzEPv//////////wEaDOxZMKTwYnHsws2mhyLPAeG9W4ruHIYRCIg0u0MXyXLVRlX/d2dD/xGUVgiZyoD+QV71mYeHxvYvj9WMwY9zgsZgisZuooxh/4SIeU9ZE741Y2cwy+EkJ5QNC8EkAbokbJ6JVzk0kdisIimKYEOO74X2/6lKawpJYKszL/APhZRo7OyiLpN1jvAPPYmQ/HXqldhvvB3lgVVXT+t4+wBxD1Zr3JZfLA82GLzdZ9q1h6ePTIfEZ9Z1XesSnOVqq56CNuU/5Bi7SUQUApbIICzWhoHQJen/Pq3URfPAj8Q3IijdwIuNBjIt7OF5Ve/h22Cd4RHdmHQgx9J70XD91+64piU3t9mnA1XznLIFB8ftLAZAtsaL")
    return client


def get_table_csv_results(file_name):

    img_test = file_name.read()
    bytes_test = bytearray(img_test)
    print('Image loaded', file_name)

    client = get_key_AWS()

    response = client.analyze_document(
        Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])

    # Get the text blocks
    blocks = response['Blocks']
    # pprint(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "NO Table FOUND "

    csv = ''
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv(table, blocks_map, index + 1)
        csv += '\n\n'

    return csv


def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)

    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():

        for col_index, text in cols.items():
            txt = '{}'.format(text)
            txt = txt.replace(",", ".")
            csv += txt + ","
        csv += '\n'

    csv += '\n\n\n'
    return csv


def main(file_name):
    table_csv = get_table_csv_results(file_name)
    print(table_csv)
    output_file = 'output.csv'
    # replace content
    with open(output_file, "wt") as fout:
        fout.write(table_csv)
    # show the results
    table_html = pd.read_csv('output.csv')
    print(table_html)


def use(file_name):
    table_csv = get_table_csv_results(file_name)
    # print(table_csv)
    output_file = 'output.csv'
    # replace content
    with open(output_file, "wt") as fout:
        fout.write(table_csv)
    # show the results
    table = pd.read_csv('output.csv', encoding='latin-1',
                        error_bad_lines=False)
    output_json = html_to_json.convert(table.to_html())
    return table.to_html()


if __name__ == "__main__":
    file_name = sys.argv[1]
    main(file_name)
