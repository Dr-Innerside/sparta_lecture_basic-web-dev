from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.preboot

@app.route('/')
def home():
   return render_template('index.html')


# API
#
#  주문하기 POST : 정보 입력 후 '주문하기' 버튼 클릭 시 주문 목록에 추가
#  주문내역보기 GET : 페이지 로딩 후 하단 주문 목록이 자동으로 보이기

# POST API
@app.route('/list', methods=['POST'])
def list_post():
   # POST API 설계
   #
   #  사용자 요청
   #  사용자가 입력한 값을 받아옴(성함, 수량, 주소, 전화번호)
   #  받아온 값을 DB에 삽입
   #  데이터 응답
   #  'msg' : '주문목록에 추가되었습니다.'

   name_receive = request.form['name_give']
   count_receive = request.form['count_give']
   address_receive = request.form['address_give']
   number_receive = request.form['number_give']

   print(name_receive, count_receive, address_receive, number_receive)

   doc = {
      'name': name_receive,
      'count': count_receive,
      'address': address_receive,
      'number': number_receive
   }

   db.list.insert_one(doc)
   return jsonify({'result':'success', 'msg': '주문 목록에 추가되었습니다!'})

# GET API
@app.route('/list', methods=['GET'])
def list_get():
   # GET API 설계
   #
   #  사용자 요청
   #  없음
   #  응답 데이터
   #  DB에 존재하는 정보(성함, 수량, 주소, 전화번호) 데이터를 뿌려줌
   #  'all_list': 올 리스트

   all_list = list(db.list.find({},{'_id':False}))

   return jsonify({'msg': '이 요청은 GET'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)