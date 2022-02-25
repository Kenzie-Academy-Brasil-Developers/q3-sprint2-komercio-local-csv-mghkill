# Suas rotas aqui
from flask import Flask, request, jsonify
from csv import DictReader

app = Flask(__name__)


@app.get('/products')
def todos_nomes():
    with open("data/products.csv", "r") as file_products:
        value_1 = int(request.args.get("page", 1))
        value_2 = int(request.args.get("per_page", 3))
        reader = DictReader(file_products)
        page = []
        if (value_1 == 1) and (value_2 == 3):
            page = list(reader)[0:3]
        else:
            page = list(reader)[((value_1 + value_2)//2 + 1):((value_1 + value_2)//2 + 1)+4]

        return jsonify(page)
    
@app.get('/products/<products_id>')
def nomes_id(products_id):
    with open("data/products.csv", "r") as file_products:
        reader = list(DictReader(file_products))
        output = {}
        print(reader)
        for item in reader.copy():
            if int(item["id"]) == int(products_id):
                output = item
        return output
        