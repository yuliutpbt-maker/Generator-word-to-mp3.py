import json
import os
from gtts import gTTS
from pydub import AudioSegment

# --- AI Generator 配置 ---
SAVE_FOLDER = "Japanese_Lessons"
LESSON_NAME = "ai_generated_lesson" # 你可以隨意改名

def run_ai_generator(sentences_list):
    """
    接收文字清單，產出：
    1. MP3 整體音檔
    2. JSON 時間戳記檔
    """
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    combined_audio = AudioSegment.empty()
    timestamp_data = []
    current_pos = 0.0

    print(f"🎬 AI Generator 分支啟動：正在處理 {len(sentences_list)} 個句子...")

    for i, text in enumerate(sentences_list):
        # 生成單句語音
        tts = gTTS(text=text, lang='ja')
        temp_mp3 = f"temp_{i}.mp3"
        tts.save(temp_mp3)

        # 讀取並計算長度
        seg = AudioSegment.from_mp3(temp_mp3)
        duration = len(seg) / 1000.0  # 秒

        # 紀錄精確的時間區段
        timestamp_data.append({
            "id": i,
            "text": text,
            "start": round(current_pos, 2),
            "end": round(current_pos + duration, 2)
        })

        # 合併音軌：每句中間空 0.8 秒方便 App 切換
        combined_audio += seg
        combined_audio += AudioSegment.silent(duration=800) 
        
        current_pos += (duration + 0.8)
        os.remove(temp_mp3)
        print(f"   [{i+1}/{len(sentences_list)}] 處理完成: {text[:10]}...")

    # 儲存輸出的檔案
    audio_path = os.path.join(SAVE_FOLDER, f"{LESSON_NAME}.mp3")
    json_path = os.path.join(SAVE_FOLDER, f"{LESSON_NAME}.json")

    combined_audio.export(audio_path, format="mp3")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            "audio_file": f"{LESSON_NAME}.mp3",
            "sentences": timestamp_data
        }, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 生成成功！")
    print(f"📁 位置：{SAVE_FOLDER}")
    print(f"📄 JSON：{LESSON_NAME}.json")
    print(f"🎵 MP3：{LESSON_NAME}.mp3")

# --- 這裡放入昨天 AI 幫你寫的文章 ---
if __name__ == "__main__":
    # 你可以把 Gemini 產出的 list 直接貼在這裡
    content = [
        "こんにちは、お元気ですか？",
        "今日はいい天気ですね。",
        "日本語を勉強するのは楽しいです。"
    ]
    run_ai_generator(content)
