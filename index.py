from flask import Flask, jsonify
from flask_cors import CORS  # <-- Nayi Library
import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)  # <-- Yeh line sabhi websites ko data access karne ki permission degi

@app.route('/', methods=['GET'])
def home():
    return "API is Live! Banners dekhne ke liye URL ke aage region lagayein, e.g., /get-leaks/ind ya /get-leaks/bd"

@app.route('/get-leaks/<region>', methods=['GET'])
def get_banners(region):
    region = region.lower()
    
    api_url = f"https://client.{region}.freefiremobile.com/LoginGetSplash"
    hex_payload = "9223AF2EAB91B7A150D528F657731074"
    data_bytes = bytes.fromhex(hex_payload)
    
    headers = {
        "Host": f"client.{region}.freefiremobile.com",
        "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInN2ciI6IjMiLCJ0eXAiOiJKV1QifQ.eyJhY2NvdW50X2lkIjoxNDU0OTI1OTk0MCwibmlja25hbWUiOiIwT3FuMjd5Y2d0ZmkyK0hDcmNiYXQ1V3NwWUhod1lDTXROdXlrdG5XbGhvPSIsIm5vdGlfcmVnaW9uIjoiSU5EIiwibG9ja19yZWdpb24iOiJJTkQiLCJleHRlcm5hbF9pZCI6IjkxZThhOTZiZWJhOWM2YThkMTYxY2JkNTgzODQ4MGVjIiwiZXh0ZXJuYWxfdHlwZSI6OCwicGxhdF9pZCI6MSwiY2xpZW50X3ZlcnNpb24iOiIyLjEyNy4xOCIsImVtdWxhdG9yX3Njb3JlIjowLCJpc19lbXVsYXRvciI6ZmFsc2UsImNvdW50cnlfY29kZSI6IklOIiwiZXh0ZXJuYWxfdWlkIjoxNDQ0MDAxNTk0OTE0LCJyZWdfYXZhdGFyIjoxMDIwMDAwMDcsInNvdXJjZSI6MCwibG9ja19yZWdpb25fdGltZSI6MTc2OTQyOTIyNiwiY2xpZW50X3R5cGUiOjIsInNpZ25hdHVyZV9tZDUiOiIxYWM0YjgwZWNmMDQ3OGE0NDIwM2JmOGZhYzYxMjBmNSIsInVzaW5nX3ZlcnNpb24iOjIsInJlbGVhc2VfY2hhbm5lbCI6ImFuZHJvaWRfbWF4IiwicmVsZWFzZV92ZXJzaW9uIjoiT0I1NCIsImV4cCI6MTc4NjUxMDEyNX0.7Wmk9UKhy6shfSKAXzFeWHFTd72DXHpoo8oLaUhZ12w",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB54",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2022.3.47f1"
    }

    try:
        response = requests.post(api_url, headers=headers, data=data_bytes, verify=False)
        
        if response.status_code == 200:
            decoded_data = response.content.decode('utf-8', errors='ignore')
            url_pattern = r'https?://[^\s<>*]+\.(?:jpg|jpeg|png)'
            extracted_urls = list(set(re.findall(url_pattern, decoded_data)))
            
            language_grouped_data = {}
            
            for url in extracted_urls:
                lang_match = re.search(r'_([a-zA-Z]{2,3})\.(?:jpg|jpeg|png)$', url, re.IGNORECASE)
                
                if lang_match:
                    lang_code = lang_match.group(1).upper()
                else:
                    lang_code = "DEFAULT_LANG"
                
                if lang_code not in language_grouped_data:
                    language_grouped_data[lang_code] = []
                
                language_grouped_data[lang_code].append(url)
                
            return jsonify({
                "success": True,
                "server_region": region.upper(),
                "total_leaks": len(extracted_urls),
                "leaks_by_language": language_grouped_data
            })
        else:
            return jsonify({"success": False, "error": f"Server Error {response.status_code}"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
