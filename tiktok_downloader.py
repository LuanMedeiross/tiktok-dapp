from TikTokAPI import TikTokAPI
from os import system
import requests
import concurrent.futures
import time

class Tiktok(object):
    
    def __init__(self, vid_id):
        self.vid_id = vid_id

    def video_exists(self):
        try:
            self.api = TikTokAPI()
            self.video = self.api.getVideoById(self.vid_id)['itemInfo']['itemStruct']
            return True
        except Exception as e:
            print(e)
            return False

    def get_msc_title(self):
        return self.video['music']['title']

    def get_msc_link(self):
        return self.video['music']['playUrl']

    def get_author_name(self):
        return self.video['author']['nickname']

    def get_author_avatar(self):
        return self.video['author']['avatarThumb']

    def get_desc(self):
        return self.video['desc']

    def download_video_without_watermark(self):

        print('downloading video without watermark')

        r = requests.get( 
            'https://toolav.herokuapp.com/id/?video_id=' + self.vid_id, 
            headers = {'user-agent': 'okhttp'} 
        )

        link = r.json().get('item').get('video').get('playAddr')[0]
        
        command = f'curl "{link}" --output ./static/download/video_without_watermark.mp4 --silent'

        system(command)
    
    def download_video_with_watermark(self):
        print('downloading video with watermark')
        return self.api.downloadVideoById(self.vid_id, './static/download/video_with_watermark.mp4')

    def download_video_thumb(self):
        
        thumb = self.video['video']['cover']

        command = f'curl "{thumb}" --output ./static/download/video_thumb.jpeg --silent'

        print('downloading video thumb')

        system(command)

    def download_msc(self):

        msc_link = self.get_msc_link()

        command = f'curl {msc_link} --output ./static/download/audio.mp3 --silent'

        print('downloading audio')

        system(command)

    def download_author_avatar(self):

        author_avatar_link = self.get_author_avatar()

        command = f'curl "{author_avatar_link}" --output ./static/download/author_avatar.jpeg --silent'

        print('downloading author avatar')

        system(command)

    def download_all(self):
        
        start = time.perf_counter()

        with concurrent.futures.ThreadPoolExecutor() as executor:

            executor.submit(self.download_msc)
            executor.submit(self.download_author_avatar)
            executor.submit(self.download_video_thumb)
            executor.submit(self.download_video_with_watermark)
            executor.submit(self.download_video_without_watermark)

        print(f'Download time: {round(time.perf_counter() - start, 2)}s')

    def wipe(self):
        system('rm ./download/*')

    def id_from_shortened_link(self):

        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

        try:    
            r = requests.get('https://vm.tiktok.com/' + self.vid_id, headers=headers, timeout=10)
            id_v = r.url.split('/video/')[1].split('?_d=')[0]
            self.vid_id = id_v
        except:
            pass

if __name__ == '__main__':
    vid_id = '7057934623619239173'
    ttk = Tiktok(vid_id)
