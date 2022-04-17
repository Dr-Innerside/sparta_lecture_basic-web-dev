from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.preboot


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분

# 영화인 조회: 영화인 정보 전체를 조회
@app.route('/api/list', methods=['GET'])
def show_stars():
    # API 설계
    #
    #   사용자 요청
    #   없음
    #   응답 데이터
    #   정보 전체 리턴
    #   'all_moviestar': 올 무비스타
    all_moviestar = list(db.mystar.find({},{'_id':False}).sort('like',-1))
    # print(all_moviestar)
    return jsonify({'msg': 'GET 연결!','all_moviestar':all_moviestar})

# 좋아요 기능: 클라이언트에서 받은이름(name_give)으로 찾아 좋아요(like) 증
@app.route('/api/like', methods=['POST'])
def like_star():
    # API 설계
    #
    #   사용자 요청
    #   이름 요청(name_give)
    #   DB에서 해당 영화인 데이터를 찾아 좋아요 값 1증가
    #   응답 데이터
    #   msg : 좋아요!
    name_receive = request.form['name_give']
    # print(name_receive)
    find_star = db.mystar.find_one({'name': name_receive})
    print(find_star)
    find_like = find_star['like']
    new_like = find_like + 1
    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})

    return jsonify({'result': 'success','msg': '좋아요!'})

# 삭제 기능: 클라이언트에서 받은이름(name_give)으로 찾아 영화인데이터 삭제
@app.route('/api/delete', methods=['POST'])
def delete_star():
    # API 설계
    #   사용자 요청
    #   사용자 이름 요청(name_give)
    #   사용자 이름으로 데이터베이스 find_one
    #   해당 데이터 삭제
    #   응답 데이터
    #   msg : 삭제 완료 되었습니다.
    name_receive = request.form['name_give']
    print(name_receive)
    db.mystar.delete_one({'name': name_receive})
    return jsonify({'result': 'success','msg': '삭제 완료 되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)