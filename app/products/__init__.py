from csv import DictWriter
import os

FILEPATH = os.getenv("FILEPATH")

def append_product(value: list):
       
    with open(FILEPATH, "a") as file:
        
        writer = DictWriter(file, ["id","name","price"])
        
        writer.writerows(value)

def change_product(value: list):
    
    with open(FILEPATH, "w") as file:
        
        writer = DictWriter(file, ["id","name","price"])
        writer.writeheader()
        writer.writerows(value)
