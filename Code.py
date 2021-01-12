#importing the module
from pytube import YouTube
import moviepy.editor as mp
import time # time module
import string
import os

class YouTubeDownloader:
    def __init__(self):
        pass
    def ClearName(self, name):
        new_name = ""
        for i in range(0,len(name)):
            if(name[i] in string.punctuation):
                new_name=new_name+"-"
            else:
                new_name=new_name+name[i]
        return new_name

    def ExtractingTheInteger(self,string):
        value = ""
        for i in range(0,len(string)):
            if(string[i]>='0' and string[i] <= '9'):
                value = value +string[i]
        return int(value)

    def DownloadInitiate(self, video_url, type='video'):
        try:
            try:
                #object creation using YouTube which was imported in the beginning
                yt = YouTube(video_url)
                self.thumbnail_url = yt.thumbnail_url
                list = yt.streams.filter(type=type)
                print(list)
                default_index = 0
                max_resolution = 0
                resolutions = []
                parse_type = ""
                if(type == 'video'):
                    parse_type = 'res='
                elif(type == 'audio'):
                    parse_type = 'abr='
                for i in range(0,len(list)):
                    string = str(list[i])
                    string = string.split(" ")
                    for j in range(0,len(string)):
                        if(parse_type in string[j]):
                            resolution = string[j].split('"')
                            print(resolution)
                            resolution = resolution[1].split('p')
                            print(resolution)
                            try:
                                print(resolution[0])
                                resolution = self.ExtractingTheInteger(resolution[0])
                                print("resul = ",resolution)
                                if(resolution not in resolutions):
                                    resolutions.append(resolution)
                            except Exception as e:
                                continue
                resolutions.sort()
                print("resolutions ",resolutions)
                default_index = 0
                files = os.listdir('./')
                ct = 0
                video_updated_title = self.ClearName(yt.title)
                f = video_updated_title
                while True:
                    if(f not in files):
                        break
                    f = video_updated_title+str(ct)
                    ct = ct + 1
                video_updated_title = f
                return True,video_updated_title,list,default_index,resolutions
            except Exception as e:
                print(e)
                print("Connection Error") #to handle exception
                return False,""
        except Exception as e:
            print(e)
            return False,""
    def GettingVideoFileActualName(self, video_file_directory):
        files = os.listdir(video_file_directory+'/')
        video_file_name = files[0]
        audio_file_name = video_file_name.strip().split('.mp4')[0]
        return audio_file_name, video_file_name
    def VideoToAudio(self,video_file_directory):
        audio_file_name, video_file_name = self.GettingVideoFileActualName(video_file_directory)
        print("audio,video = ",audio_file_name, video_file_name)
        try:
            # Insert Local Video File Path
            clip = mp.VideoFileClip(video_file_directory+'/'+video_file_name)
            # Insert Local Audio File Path
            clip.audio.write_audiofile(video_file_directory+'/'+audio_file_name+'.mp3')
            clip.close()
            print("came here")
            return True, audio_file_name, video_file_name
        except Exception as e:
            print(e)
            return False, None, video_file_name
    def PerformDownload(self, video_updated_title, list_of_streams, index):
        stream = list_of_streams[index]
        try:
            stream.download(video_updated_title)
            print("video download completed.")
            return True
        except Exception as e:
            print(e)
            return False
            
    def ChooseResolution(self,resolutions):
        if(len(resolutions) == 1):
            return 0
        else:
            while True:
                print(resolutions)
                try:
                    index = int(input('Choose the resolution index (1 based indexing): '))
                except Exception as e:
                    print("Give properly (1 based indexing)")
                    continue
                index = index-1
                if(index>=0 and index<=len(resolutions)-1):
                    return index

    def DownloadBase(self,video_url, type):
        for i in range(0,10):
            verdict,video_updated_title,list_of_streams,default_index,resolutions  = self.DownloadInitiate(video_url,type)
            if(verdict == True):
                verdict = self.PerformDownload(video_updated_title, list_of_streams, default_index)
                if(verdict == True):
                    return True,video_updated_title
            else:
                time.sleep(.500)
                print("Again Trying")
        return False,None

    def Main(self,type,link):
        if(type == 'video' or type == 'audio'):
            verdict,video_updated_title = self.DownloadBase(video_url=link, type=type)
            return verdict,video_updated_title,"",""

#link of the video to be downloaded
link="https://www.youtube.com/watch?v=Cb6wuzOurPc"
type = 'video'
main = YouTubeDownloader()
verdict, video_updated_title,video_file_name,audio_file_name = main.Main(type,link)
del main
