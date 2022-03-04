# Suas rotas aqui
from http.client import OK
from flask import Flask, request, jsonify
from csv import DictReader
from http import HTTPStatus
import os
from app.products import append_product, change_product


app = Flask(__name__)

FILEPATH = os.getenv("FILEPATH")



@app.get('/products')
def names():
    
    with open(FILEPATH, "r") as file_products:
        # 
        reader = DictReader(file_products, ["",""])
        
        
        value_1 = int(request.args.get("page", 1))
        value_2 = int(request.args.get("per_page", 3))
        page = []
        if (value_1 == 1) and (value_2 == 3):
            page = list(reader)[0:3]
        else:
            page = list(reader)[((value_1 + value_2)//2 + 1):((value_1 + value_2)//2 + 1)+4]
        output = []
        for item in page.copy():
            item["id"] = int(item["id"])
            item["price"] = float(item["price"])
            output.append(item)
        return jsonify(output), HTTPStatus.OK
    
@app.get('/products/<products_id>')
def names_id(products_id):
    with open(FILEPATH, "r") as file_products:
        reader = list(DictReader(file_products))
        output = {}
        for item in reader.copy():
            if int(item["id"]) == int(products_id):
                item["id"] = int(item["id"])
                item["price"] = float(item["price"])
                output = item
        return output, HTTPStatus.OK
        
@app.post('/products')
def add_products():
    #capturar o id do csv
    data = request.get_json()
    data_output = []
    data_keys_list = list(data.keys())
    last_id = ""

    with open(FILEPATH, "r") as file_products:
        reader = list(DictReader(file_products))
        last_id = list(reader)[-1]["id"]

    if (len(data) == 2) and (data_keys_list[0] == "name") and (data_keys_list[1] == "price"):
        new_id = int(last_id) + 1
        new_name = data.get('name')
        new_price = float(data.get('price'))
        data_output = [{"id": new_id, "name": new_name, "price": new_price}]
    else:
        return jsonify([{"error": "Requisição inválida!"},{"example": {"name": "batata", "price": "10.50"}}]), HTTPStatus.BAD_REQUEST

    append_product(data_output)
    
    return {"message": data_output}, HTTPStatus.ACCEPTED

@app.patch('/products/<product_id>')
def change_request_products(product_id):
    data = request.get_json()
    new_data_output = []
    data_output = []
    data_keys_list = list(data.keys())
    
    
    with open(FILEPATH, "r") as file_products:
            
        reader = (DictReader(file_products))

        if (len(data) == 2) and (data_keys_list[0] == "name") and (data_keys_list[1] == "price"):
            new_id = int(product_id)
            new_name = data.get('name')
            new_price = float(data.get('price'))
            new_data_output = {"id": new_id, "name": new_name, "price": new_price}
        else:
            return jsonify([{"error": "Requisição inválida!"},{"example": {"name": "batata", "price": "10.50"}}]), HTTPStatus.BAD_REQUEST            
        for dict in reader:
            if int(dict["id"]) == int(product_id):
                data_output.append(new_data_output)
            else:
                dict["id"] = int(dict["id"])
                dict["price"] = float(dict["price"])
                data_output.append(dict)                    

    change_product(data_output)
    return {"sucess": new_data_output}

@app.delete('/products/<product_id>')
def delete_products(product_id):
    data = request.get_json()
    delete_data_output = []
    data_output = []
    
    
    with open(FILEPATH, "r") as file_products:
            
        reader = (DictReader(file_products))
        
        for dict in reader:
            if int(dict["id"]) == int(product_id):
                delete_data_output.append(dict)
            else:
                dict["id"] = int(dict["id"])
                dict["price"] = float(dict["price"])
                data_output.append(dict)                    

    change_product(data_output)
    return {"deleted": delete_data_output}
