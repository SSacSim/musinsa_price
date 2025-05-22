from flask import Flask, render_template, abort , request, jsonify
from flask_cors import CORS

import csv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.DButils as dbu

app = Flask(__name__)
CORS(app)
# CSV 파일을 읽어서 딕셔너리로 저장
# 램에 올리는건 말도 안됨 
#

# DB에서 읽어오도록 변경 
# -> DB 객체 생성 

db_ = dbu.DBOBJ()

date, cost , sale = None, None ,None 
def load_products(item_index):
    
    cost,sale, date , products, rows= db_.search_items(item_index)
    return products, cost, sale, date


@app.route('/')
def show_main():
    return render_template('main.html')

@app.route('/product/<product_id>')
def show_product(product_id):
    global cost , sale, date
    product ,cost , sale ,date  = load_products(product_id)
    if product:
        return render_template('product.html', product=product)
    else:
        abort(404)


@app.route('/validate_product', methods=['GET'])
def validate_product():
    '''
        상품번호 유효 확인 
        return : jsonify 
    '''

    # 상품번호 / 상풍명 들어왔을때 처리하도록 변경 .
    product = request.args.get('product')
    print(product)
    product_number = db_.valid_item(product)
    if product_number is None:
        return jsonify({"valid": False, "message": "상품번호가 존재하지 않습니다."})
    else:
        return jsonify({"valid": True, "url": f"/product/{product_number}"})


@app.route('/get_product_data')
def get_product_data():
    product_data = {
        'date' : date,
        'price': cost,  # 가격 (숫자형)
        'discountRate': sale   # 할인율
    }
    return jsonify(product_data)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify(results=[])
    try:
        db_.cur.execute("SELECT 상품명 FROM products WHERE 상품명 LIKE %s LIMIT 5", ('%' + query + '%',))
        
        results = [row for row in db_.cur.fetchall()]
        print(results)
        # conn.close()
        return jsonify({'results': results})
    except Exception as e:
        # 트랜잭션 롤백
        db_.conn.rollback()
        print("DB 오류:", e)
        return jsonify(results=[])

if __name__ == '__main__':
    app.run(debug=True)