from flask import Flask, render_template, request, url_for, send_file, redirect
from os import listdir
from tiktok_downloader import *
import re
import os

import nest_asyncio
nest_asyncio.apply()

app = Flask(__name__)

@app.route('/', methods = ["POST", "GET"])
async def index(err=None, desc=None, nick_author=None):
    if request.method == "POST":

        link = request.form['link']

        if 'https' in link and 'tiktok' in link:

            id_v = link.split('/')[-1]

            if bool(re.match('^[A-Za-z0-9]*$', id_v)):

                ttk = Tiktok(id_v)
                
                ttk.id_from_shortened_link() if 'vm.' in link else False
                
                if ttk.video_exists():            

                    if len(listdir('./static/download')) == 0:
                        ttk.download_all()

                    desc = ttk.get_desc()
                    nick_author = ttk.get_author_name()

                    return render_template('download.html', desc=desc, nick_author=nick_author)
                
                else: return render_template('index.html', err='Video não encontrado!')

            else: return render_template('index.html', err="Não use caracteres especiais!")
        
        else: return render_template('index.html', err='Insira o link corretamente!')

    else:
        os.system('rm ./static/download/*') 
        return render_template('index.html')

@app.route('/download/<mode>')
def download(mode):
    
    if mode == 'without_watermark':
        return send_file('./static/download/video_without_watermark.mp4', as_attachment=True)
    elif mode == 'with_watermark':
        return send_file('./static/download/video_with_watermark.mp4', as_attachment=True)
    elif mode == 'video_audio':
        return send_file('./static/download/audio.mp3', as_attachment=True)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run()
