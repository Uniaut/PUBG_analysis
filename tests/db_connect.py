from pymongo import MongoClient
from pymongo.cursor import CursorType
import json

with open('58d82aa4-f206-4dc6-82d1-6db8fba29905Desert_Main.json') as file:
    file_data = json.load(file)

client = MongoClient("mongodb://localhost:27017")
db = client['PUBG_Analysis']

db.landing_recommendation.insert_one(file_data)
for i in db['landing_recommendation'].find():
    print(i)










# db.landing_reommendataion.find({'land_x','land_y','end_x','end_y','circle_x','circle_y'}){
#     item.
# }




# db.getCollection('recipe').find({ data_value: { $type: 2 } }).forEach(function(obj){
# try {
# 	obj.data_value = parseInt(obj.data_value);
# 	db.getCollection('recipe').save(obj);
#     } catch(e) {
    
#     }
# });
# 출처: https://hwanschoi.tistory.com/142 [신세계에 발을 담그다:티스토리]

# db = client.PUBG_Analysis
# collection = client.landing_recommendataion





# def insert_item_one(mongo, data, db_name=None, collection_name=None):
#     result = mongo[db_name][collection_name].insert_one(data).inserted_id
#     return result

# def insert_data(data):
#     keys = list(data.keys())
#     for i in range(len(keys)):
#         key = keys[i]
#         value = data.get(str(keys[i]))

#         insert_item_one(client,"{key} : {value}", "PUBG_Analysis", "landing_recommendataion")


# def temp(data):
#     keys = list(data.keys())
#     for i in range(len(keys)):
#         print(keys[i]," : ",data.get(str(keys[i])))





# temp(file_data)
#collection = db['landing_recommendation']

# print("get collection", db.get_collection('landing_recommendation'))
# print("db.list_collection_name", db.list_collection_names())

#C:\Program Files\MongoDB\Server\5.0\bin>mongod --dbpath "C:\Users\juhon\PUBG_DB"




