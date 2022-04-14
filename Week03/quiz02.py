from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.preboot

# 코딩 시작

movie = db.movies.find_one({'title':'매트릭스'},{'_id':False})
print(movie['star'])

db.movies.update_one({'title':'매트릭스'},{'$set':{'star':0}})
