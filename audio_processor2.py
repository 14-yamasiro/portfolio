import google.generativeai as genai
from dotenv import load_dotenv
import os, re, subprocess
from typing import Tuple, Optional

class AudioProcessor:
    def __init__(self):
        """
        音声処理クラスの初期化
        """
        load_dotenv()
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')

    def download_youtube_audio(self, url: str, output_dir: str) -> Tuple[Optional[str], Optional[str]]:
        """
        YouTubeの動画から音声を抽出する
        Args:
            url: YouTube URL
            output_dir: 出力先ディレクトリパス
        Returns:
            Tuple[Optional[str], Optional[str]]: (音声ファイルパス, エラーメッセージ)
        """
        try:
            # video_idを取得
            video_id = re.search(r"v=([^&]+)", url).group(1)
            print(video_id)
            # 以降、未実装
        
        except Exception as ex:
            return None, str(ex)
    
    def get_audio_path(self, output_dir: str, video_id: str) -> Optional[str]:
        """
        音声ファイルのパスを取得する
        Args:
            output_dir: 出力先ディレクトリパス
            video_id: YouTube動画のID
        Returns:
            Optional[str]: 音声ファイルのパス
        """
        audio_files = [f for f in os.listdir(output_dir) if video_id in f]
        if not audio_files:
            return None
        return os.path.join(output_dir, audio_files[0])

    def transcribe_audio(self, audio_path: str, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        """
        音声ファイルを文字起こしする
        Args:
            audio_path: 音声ファイルのパス
            prompt: 文字起こしの指示プロンプト
        Returns:
            Tuple[Optional[str], Optional[str]]: (文字起こし結果, エラーメッセージ)
        """
        try:
            # 未実装
            with open(audio_path) as audio_file:
                audio_file=audio_file,
                prompt=prompt
                contents = [audio_file, prompt]
                transcription = self.model.generate_content(contents) 
            pass
        except Exception as ex:
            return None, str(ex)
        
        """ prompt=prompt
            audio_file = Part.from_uri(audio_path, mime_type="audio/mpeg")
            contents = [audio_file, prompt]
            transcription = self.model.generate_content(contents)
            return transcription.text, None
        except Exception as ex:
            return None, str(ex) """