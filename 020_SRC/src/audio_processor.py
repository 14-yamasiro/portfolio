
import google.generativeai as genai
from dotenv import load_dotenv
import os, re, subprocess
from typing import Tuple, Optional


venv_python = r'.\venv\Scripts\python.exe'





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
            # YouTube URLから動画の種類を判別
            video_format_match = re.search(r"youtube\.com/(watch|shorts)", url)
            video_format = video_format_match.group(1)
            if video_format == "watch":
                # YouTube URLから動画IDを抽出(横動画)
                video_id = re.search(r"v=([^&]+)", url).group(1)
                print(video_id)

            elif video_format == "shorts":
                # YouTube URLから動画IDを抽出(ショート動画)
                video_id = re.search(r"shorts/([^&]+)", url).group(1)
                print(video_id)

            else:
                print(video_format)
                return None, "urlの形式が正しくありません"
            
            # 以降、未実装----------------------------------------------------------------------------

            # 出力ファイルパスを指定
            output_dir = "./cache"
            output_path = os.path.join(output_dir, f"{video_id}.mp3")

            # 既にダウンロードしている動画の場合はダウンロードを飛ばす
            if os.path.exists(output_path):
                return output_path, None

            # FFmpegのパスを取得 
            ffmpeg_path = "./bin/ffmpeg.exe"


            # yt-dlpコマンドを作成
            cmd = [
                "./bin/yt-dlp.exe",
                "-x",  # 音声のみ抽出
                "--audio-format", "mp3",  # 出力フォーマットをmp3に設定
                "-o", output_path,  # 出力パスを指定
                "--ffmpeg-location", ffmpeg_path, # FFmpegのパスを指定
                url
            ]
            
            # サブプロセスでコマンドを実行
            subprocess.run(cmd, check=True)
            
            # ダウンロードされた音声ファイルのパスを返す
            if os.path.exists(output_path):
                return output_path, None
            else:
                return None, "音声ファイルの取得に失敗しました"
        
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
            # 以降、未実装----------------------------------------------------------------------------
            # 音声ファイルの内容をアップロードする
            audio_file = genai.upload_file(path=audio_path)
            # APIリクエストを送信して文字起こしを取得
            response = self.model.generate_content([prompt, audio_file])
            transcribed_text = response.text
            # genai.delete_file(audio_file.name)
            return transcribed_text, None

        except Exception as ex:
            return None, str(ex)



        


            
