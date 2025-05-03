from flask import Flask, render_template, abort , request, jsonify
import csv

app = Flask(__name__)

# CSV 파일을 읽어서 딕셔너리로 저장
# 램에 올리는건 말도 안됨 

def load_products():
    products = {}
    with open(r'C:\Users\sim\Desktop\musinsa\datas\2025-04-28.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products[row['상품번호']] = row
    # print(products)
    return products

# 상품 데이터 로드
product_data = load_products()


@app.route('/')
def show_main():
    return render_template('main.html')

@app.route('/product/<product_id>')
def show_product(product_id):
    product = product_data.get(product_id)
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
    product_id = request.args.get('product_id')

    if product_id in product_data:
        # 유효한 상품번호라면 해당 상품 페이지로 리디렉션
        return jsonify({"valid": True, "url": f"/product/{product_id}"})
    else:
        # 유효하지 않으면 오류 메시지 반환
        return jsonify({"valid": False, "message": "상품번호가 존재하지 않습니다."})



@app.route('/get_product_data')
def get_product_data():
    # print("ddddd")
    product_data = {
        'price': [10000, 50000, 3000, 2000, 40000],  # 가격 (숫자형)
        'discountRate': [30, 50, 20, 30, 50]   # 할인율
    }
    return jsonify(product_data)


if __name__ == '__main__':
    app.run(debug=True)