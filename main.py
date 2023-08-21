from flask import Flask, request
from flask_restful import Api, Resource, reqparse

import pandas as pd
import numpy as np

import os

app = Flask(__name__)
api = Api(app)

files = []

subfolder_name = "files/"

class File(Resource):
    def get(self, filename=''):
        parser = reqparse.RequestParser()
        parser.add_argument("filter", location='args', type=str)
        parser.add_argument("sort", location='args', type=str)
        params = parser.parse_args()
        subfolder_fullpath = os.path.join(os.getcwd(), subfolder_name)
        if filename == '':
            #return list of all files with columns info
            return_list = []
            for file in os.listdir(subfolder_fullpath):
                try:
                    # print(os.path.join(subfolder_fullpath, file))
                    df = pd.read_csv(os.path.join(subfolder_fullpath, file))
                    
                except FileNotFoundError:
                    return 'No such file found', 400
                res = df.describe(include='all').loc[['count', 'unique', 'top']]
                current_dict = {
                    'filename': file,
                    'columns': []
                }
                for title in res:
                    tmp_dict = {
                        'name': title,
                        'count': str(res.loc['count', title]),
                        'unique': str(res.loc['unique', title]),
                        'top': str(res.loc['top', title])
                    }
                    current_dict["columns"].append(tmp_dict)
                return_list.append(current_dict)
            return return_list, 200
        else:
            #give info about certain file
            found = False
            return_dict = {}
            for file in os.listdir(subfolder_fullpath):
                if file != filename:
                    continue
                found = True
                df = pd.read_csv(os.path.join(subfolder_fullpath, file))
                if params["filter"] != None:
                    filter_parameters = params["filter"].split(',')
                    res = df[[str for str in df if str in filter_parameters]]
                    if params["sort"] != None:
                        sort = params["sort"].split(',')
                        res = res.sort_values(sort)
                    return_dict = res.to_json(orient='index')

            if found:
                return return_dict, 200
            return 'File not found', 400


    def post(self, filename):
        f = request.files['file']
        current_path = os.getcwd()
        subfolder_path = os.path.join(current_path, subfolder_name)
        try:
            os.mkdir(subfolder_path)
        except FileExistsError:
            pass
        # df = pd.read_csv(f)
        file = open(os.path.join(subfolder_path, filename), 'wb')
        # file.write(*f)
        f.save(file)
        file.close()
        return 'File has been uploaded', 200

    def delete(self, filename):
        subfolder_fullpath = os.path.join(os.getcwd(), subfolder_name)
        was_deleted = False
        for file in os.listdir(subfolder_fullpath):
            if file == filename:
                os.remove(os.path.join(subfolder_fullpath, file))
                was_deleted = True
                break
        if was_deleted:
            return f'File {filename} was successfully deleted', 200
        return f'File {filename} not found', 400


api.add_resource(File, "/file/<string:filename>", "/file", "/file/")
if __name__ == '__main__':
    app.run(debug=True)