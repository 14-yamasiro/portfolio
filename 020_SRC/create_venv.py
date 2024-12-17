import asyncio, os
import platform

# Python実行ファイルのバージョンと場所を指定
PYTHON_VERSION = '312'
PYTHON_PATH = rf'%USERPROFILE%\AppData\Local\Programs\Python\Python{PYTHON_VERSION}\python.exe'

async def create_subprocess(cmd):
    # サブプロセスを作成し、標準出力と標準エラー出力をパイプで接続
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    
    # 出力を逐次的に読み取って表示
    while True:
        # cp65001(UTF-8)でデコードし、右側の空白を削除
        stdout = (await proc.stdout.readline()).decode('cp65001', 'ignore').rstrip()
        if len(stdout):
            # 出力がある場合は表示（flush=Trueでバッファリングせずに即時出力）
            print(stdout, end='\n', flush=True)
        else:
            break

async def main():
    # OSに応じてactivateスクリプトのパスを設定
    if platform.system() == 'Windows':
        activate = r'.\venv\Scripts\activate.bat'
    elif platform.system() == 'Darwin':  # macOS
        activate = r'./venv/bin/activate'
    else:
        raise Exception('Unsupported OS')

    # 仮想環境を作成
    await create_subprocess(f'{PYTHON_PATH} -m venv venv')
    
    # 仮想環境をアクティベートし、pipをアップグレードして必要なパッケージをインストール
    await create_subprocess(f'{activate} && python -m pip install --upgrade pip && pip install -r requirements.txt')
    
    # 実行終了後にコンソールを一時停止
    os.system('PAUSE')

try:
    # メイン処理を非同期で実行
    asyncio.run(main())
except Exception as e:
    # エラーが発生した場合は表示して一時停止
    print(e)
    os.system('PAUSE')