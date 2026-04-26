import json
import os
from gtts import gTTS
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog

def select_folder():
    """彈出視窗讓使用者選擇下載路徑"""
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    folder_selected = filedialog.askdirectory(title="請選擇教材儲存路徑")
    root.destroy()
    return folder_selected

def run_ai_generator(sentences_list):
    # 1. 選擇路徑
    save_path = select_folder()
    if not save_path:
        print("❌ 未選擇路徑，程式結束")
        return

    lesson_name = input("請輸入課目名稱 (例如 lesson_01): ") or "lesson_01"
    
    combined_audio = AudioSegment.empty()
    timestamp_data = []
    current_pos = 0.0

    print(f"🚀 開始生成教學內容到: {save_path}")

    for i, text in enumerate(sentences_list):
        print(f"正在處理 [{i+1}/{len(sentences_list)}]: {text}")
        
        # 生成單句語音
        tts = gTTS(text=text, lang='ja')
        temp_mp3 = "temp_voice.mp3"
        tts.save(temp_mp3)

        # 讀取並計算長度
        seg = AudioSegment.from_mp3(temp_mp3)
        duration = len(seg) / 1000.0  # 秒

        # 紀錄時間區段
        timestamp_data.append({
            "id": i,
            "text": text,
            "start": round(current_pos, 2),
            "end": round(current_pos + duration, 2)
        })

        # 合併音軌，每句間隔 0.8 秒
        combined_audio += seg
        combined_audio += AudioSegment.silent(duration=800) 
        
        current_pos += (duration + 0.8)
        os.remove(temp_mp3)

    # 儲存輸出的檔案
    audio_filename = f"{lesson_name}.mp3"
    json_filename = f"{lesson_name}.json"
    
    combined_audio.export(os.path.join(save_path, audio_filename), format="mp3")
    
    with open(os.path.join(save_path, json_filename), 'w', encoding='utf-8') as f:
        json.dump({
            "audio_file": audio_filename,
            "sentences": timestamp_data
        }, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 生成成功！")
    print(f"🎵 音檔: {audio_filename}")
    print(f"📄 索引: {json_filename}")

# --- 測試內容 (這裡可以換成 Gemini 給你的內容) ---
if __name__ == "__main__":
    content = [
        "こんにちは、お元気ですか？",
        "今日はいい天気ですね。",
        "一緒に日本語を勉強しましょう。"
    ]
    run_ai_generator(content)
