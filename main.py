from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import re

app = Flask(__name__)

# --- SIMULASI DATABASE PENGETAHUAN ---
hiwar_db = {
    "assalamualaikum": "waalaikumussalam",
    "ma ismuka": "ismi khalid, wa anta?",
    "masmuka": "ismi khalid, wa anta?",
    "ma ismuki": "ismi aisyah, wa anti?",
    "masmuki": "ismi aisyah, wa anti?",
    "ismi ahmad": "ahlan ya ahmad",
    "ismi fatima": "ahlan ya fatima",
    "kaifa haluk": "bikhoir, walhamdulillah. wa kaifa haluk anta?",
    "kaifa haluki": "bikhoir, walhamdulillah. wa kaifa haluki anti?",
}

# --- SIMULASI DATABASE SUARA (TTS) ---
voice_db = {
    "male": {
        "waalaikumussalam": "https://www.islamcan.com/audio/dua/walykum-as-salam.mp3",
        "ismi khalid, wa anta?": "https://translate.google.com/translate_tts?ie=UTF-8&q=%D8%A7%D8%B3%D9%85%D9%8A%20%D8%AE%D8%A7%D9%84%D8%AF%20%D9%88%D8%A3%D9%86%D8%AA&tl=ar&client=tw-ob",
        "ahlan ya ahmad": "https://translate.google.com/translate_tts?ie=UTF-8&q=%D8%A3%D9%87%D9%84%D8%A7%20%D9%8A%D8%A7%20%D8%A3%D8%AD%D9%85%D8%AF&tl=ar&client=tw-ob",
        "bikhoir, walhamdulillah. wa kaifa haluk anta?": "https://translate.google.com/translate_tts?ie=UTF-8&q=%D8%A8%D8%AE%D9%8A%D8%B1%20%D9%88%D8%A7%D9%84%D8%AD%D9%85%D8%AF%20%D9%84%D9%84%D9%87%20%D9%88%D9%83%D9%8A%D9%81%20%D8%AD%D8%A7%D9%84%D9%83%20%D8%A3%D9%86%D8%AA&tl=ar&client=tw-ob",
        "default": "https://translate.google.com/translate_tts?ie=UTF-8&q=%D8%A7%D9%84%D8%B9%D9%81%D9%88%D8%8C%20%D9%84%D9%85%20%D8%A3%D9%81%D9%87%D9%85%20%D8%B0%D9%84%D9%83.%20%D9%8A%D8%B1%D8%AC%D9%89%20%D8%A7%D9%84%D9%85%D8%AD%D8%A7%D9%88%D9%84%D8%A9%20%D9%85%D8%B1%D8%A9%20%D8%A3%D8%AE%D8%B1%D9%89.&tl=ar&client=tw-ob"
    },
    "female": {
        "waalaikumussalam": "https://www.islamcan.com/audio/dua/walykum-as-salam.mp3",
        "ismi aisyah, wa anti?": "https://translate.google.com/translate_tts?ie=UTF-8&q=%D8%A7%D8%B3%D9%85%D9%8A%20%D8%B9%D8%A7%D8%A6%D8%B4%D8%A9%20%D9%88%D8%A3%D9%86%D8%AA&tl=ar&client=tw-ob",
        "ahlan ya fatima": "https://translate.google.com/translate_tts?ie=UTF-8&q=%D8%A3%D9%87%D9%84%D8%A7%20%D9%8A%D8%A7%20%D9%81%D8%A7%D8%B7%D9%85%D8%A9&tl=ar&client=tw-ob",
        "bikhoir, walhamdulillah. wa kaifa haluki anti?": "https://translate.google.com/translate_tts?ie=UTF-8&q=%D8%A8%D8%AE%D9%8A%D8%B1%20%D9%88%D8%A7%D9%84%D8%AD%D9%85%D8%AF%20%D9%84%D9%84%D9%87%20%D9%88%D9%83%D9%8A%D9%81%20%D8%AD%D8%A7%D9%84%D9%83%20%D8%A3%D9%86%D8%AA&tl=ar&client=tw-ob",
        "default": "https://translate.google.com/translate_tts?ie=UTF-8&q=%D8%A7%D9%84%D8%B9%D9%81%D9%88%D8%8C%20%D9%84%D9%85%20%D8%A3%D9%81%D9%87%D9%85%20%D8%B0%D9%84%D9%83.%20%D9%8A%D8%B1%D8%AC%D9%89%20%D8%A7%D9%84%D9%85%D8%AD%D8%A7%D9%88%D9%84%D8%A9%20%D9%85%D8%B1%D8%A9%20%D8%A3%D8%AE%D8%B1%D9%89.&tl=ar&client=tw-ob"
    }
}

# --- PENANGANAN CORS MANUAL ---
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = make_response()
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'POST'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return res

@app.after_request
def add_cors_headers(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
# --- AKHIR PENANGANAN CORS MANUAL ---


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower()
    user_message = re.sub(r'[^\w\s]', '', user_message)
    tutor_gender = data.get('tutor', 'male')
    
    response_text = ""
    
    if "siapa yang membuat kamu" in user_message or "siapa penciptamu" in user_message:
        response_text = "Saya dibuat oleh David Satria Kaunang, mahasiswa jurusan pendidikan bahasa arab, kampus IAIN Sultan Amai Gorontalo."
    elif user_message in hiwar_db:
        response_text = hiwar_db[user_message]
    else:
        response_text = "default_response"

    if response_text == "default_response":
        audio_url = voice_db[tutor_gender]['default']
        response_text = "Maaf, saya belum mengerti. Coba tanyakan dari Hiwar."
    else:
        # Untuk jawaban 'creator', kita gunakan suara default karena teksnya panjang
        audio_url = voice_db[tutor_gender].get(response_text, voice_db[tutor_gender]['default'])

    return jsonify({
        "text_response": response_text.capitalize(),
        "audio_url": audio_url
    })

if __name__ == '__main__':
    app.run(debug=True)