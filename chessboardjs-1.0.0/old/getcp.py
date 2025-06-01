import subprocess
import os
import time
import re
#w15:2460
#w16:2250
#b15:2571
#b16:2164

#stockfishの実行ファイルへのパス
stockfish_path = "stockfish/src/stockfish"
#ファイルのパス
path_input = "testmatch2.txt" #試合の棋譜へのパス
path_output = "testmatchout2.txt"
error_num = 0
num = 0
kyokumen = 0
k=1
for i in range(0, 1):
    line = 0
    fenpath = path_input
    #outputファイルへのパス
    evalout = path_output
    #stockfishを起動
    stockfish = subprocess.Popen(
        [stockfish_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1,  #行単位でバッファリング
        universal_newlines=True
    )
    #fen形式の棋譜を一行ずつ送信して評価値を取得
    try:
        with open(fenpath, 'r') as f, open(evalout, 'a') as outf:
            for fenline in f:
                line += 1
                if '"' not in fenline and '{' not in fenline: #対戦情報の箇所はスキップ
                    fenline = fenline.rstrip('[')
                    fenline = fenline.rstrip(']')
                    fenline = fenline.rstrip(')')
                    outf.write(fenline.strip())
                    parts = fenline.split()
                    fenline = ' '.join(parts[:4])
                    stockfish.stdout.flush()
                    print(str(line) + " " + str(fenline.strip()))
                    #outf.write(fenline.strip() + '\n')
                    stockfish.stdin.write(f'position fen {fenline.strip()}\n')  #改行削除
                    stockfish.stdin.flush()
                    stockfish.stdin.write('go depth 20\n')
                    stockfish.stdin.flush()
                    start_time = time.time()
                    while True:
                        output = stockfish.stdout.readline().strip()
                        elapsed_time = time.time() - start_time
                        if 'info depth 20' in output:
                            print(output)
                            match = re.search(r'score cp (-?\d+)', output)
                            if match:
                                kyokumen += 1
                                cp = match.group(1)
                                outf.write(f" cp {cp}")
                                outf.flush()
                                outf.write('\n')
                            break
                        if "bestmove (none)" in output:
                            outf.write(" checkmate")
                            break
        print(kyokumen)
        print(error_num)
    except Exception as e:
        print(f"error: {e}\n")
    finally:
        #stockfishを終了
        stockfish.terminate()
