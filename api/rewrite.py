from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/api/rewrite', methods=['POST'])
def rewrite_text():
    try:
        # 获取请求数据
        data = request.get_json()
        original_text = data.get('text', '')
        
        if not original_text:
            return jsonify({"error": "请提供要改写的文章内容"}), 400
        
        # 豆包API配置（你需要替换成真实的API地址和密钥）
        api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"  # 这是示例地址，请替换
        headers = {
            "Authorization": f"Bearer {os.environ.get('DOUBAO_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        # 精心设计的提示词
        prompt = f"""请你作为一个经验丰富的写作专家，将下面的文章进行深度改写。改写要求：

1. 保持原文的核心观点和主要信息
2. 完全改变表达方式，使用更自然、更人性化的语言
3. 增加一些个人见解和情感色彩
4. 调整句式结构，避免AI写作的规整模式
5. 适当添加细节描述和例子
6. 让文章读起来像是人类原创作品

原文内容：
{original_text}

请输出改写后的文章："""

        # 调用豆包API
        payload = {
            "model": "ep-20241201111649-vdxkx",  # 这是示例模型名，请替换成你的
            "messages": [
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.8,
            "max_tokens": 4000
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            rewritten_text = result['choices'][0]['message']['content']
            return jsonify({
                "success": True,
                "rewritten_text": rewritten_text,
                "original_length": len(original_text),
                "rewritten_length": len(rewritten_text)
            })
        else:
            return jsonify({
                "error": f"API调用失败: {response.status_code}",
                "message": response.text
            }), 500
            
    except Exception as e:
        return jsonify({"error": f"处理失败: {str(e)}"}), 500

# Vercel需要这个
if __name__ == '__main__':
    app.run(debug=True)
