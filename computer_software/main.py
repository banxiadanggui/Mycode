import math
import json
import time
import GAv4 
import GAv3
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def receive_data():
    try:
        # 获取前端发送的 JSON 数据
        data = request.get_json()
        start_time = time.time()
        with open ('data.json','w',encoding='utf-8') as f:
            json.dump(data,f,indent = 4,ensure_ascii = False)
        # 在这里处理数据并执行相应的操作
        print("Received data")
        response_data = GAv4.processing(data)
        end_time = time.time()
        print(f"程序用时：{end_time - start_time}秒")
        # 将响应数据转换为 JSON 格式并返回
        return jsonify(response_data), 200
    except Exception as e:
        print(e,'failed')
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9111, debug=True)
