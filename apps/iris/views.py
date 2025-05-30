from flask import Flask, request, render_template, jsonify, abort, current_app
from .authentication import require_api_key
import pickle
import os
from . import iris
# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
#TARGET_NAMES = ['setosa', 'versicolor', 'virginica']
from apps.config import Config
TARGET_NAMES = Config.LABELS   # 라벨 읽기
def check_api_key(request):
    key = (request.headers.get('x-api-key') or request.args.get('api_key') or request.form.get('api_key'))
    print('받은 API KEY:', key, '기대값:', current_app.config['API_KEY'])  # <--- 임시 디버깅용
    if key != current_app.config['API_KEY']:
        abort(401, 'Invalid or missing API Key')
@iris.route('/predict', methods=['GET', 'POST'])
def iris_predict():
    if request.method == 'POST':
        check_api_key(request)
        try:
            sl = float(request.form['sepal_length'])
            sw = float(request.form['sepal_width'])
            pl = float(request.form['petal_length'])
            pw = float(request.form['petal_width'])
        except Exception as e:
            return render_template('iris/index.html', error='입력 오류: '+str(e))
        pred = model.predict([[sl, sw, pl, pw]])[0]
        return render_template('iris/index.html',
                               result=TARGET_NAMES[pred],
                               sepal_length=sl, sepal_width=sw,
                               petal_length=pl, petal_width=pw,
                               api_key=request.form.get('api_key'))
    return render_template('iris/index.html')
@iris.route('/api/predict', methods=['POST'])
@require_api_key
def api_predict():
    data = request.get_json(force=True)
    try:
        X = [[
            float(data['sepal_length']),
            float(data['sepal_width']),
            float(data['petal_length']),
            float(data['petal_width'])
        ]]
    except Exception as e:
        return jsonify({'error': '입력 오류: '+str(e)}), 400
    pred = model.predict(X)[0]
    return jsonify({
        'class': TARGET_NAMES[pred]
    })
# curl -X POST http://localhost:5000/iris/api/predict -H "Content-Type: application/json" -H "x-api-key: your_strong_api_key_here" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
