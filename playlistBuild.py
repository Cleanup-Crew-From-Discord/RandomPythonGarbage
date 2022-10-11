from asyncore import write
import sys
try:
    import mutagen
except:
    sys.exit('mutagen is required. run "pip install mutagen" and retry.')
from mutagen.easyid3 import EasyID3
import os
from datetime import datetime
cwd=os.getcwd()
mixedArtistReplace="Mixed Artist" #Change this to whatever string you want to denotate a mixed artist EG "(): Armageddon : The Album"
print("Running....")
#Crawl the current directory AND all subdirectories, proccess and pack each found mp3 file onto a list
def get_mp3_files(starter): #TODO: convert to os.walk loop, its much nicer than this nasty recursiveness
    songlist=[]
    alblist=[]
    for entry in os.scandir(starter):
            if entry.is_file() and entry.name.endswith(".mp3"):
                songlist.append(convert(entry))
                alblist.append(albums(entry))
            elif entry.is_dir():
                sl,al=(get_mp3_files(entry.path))
                songlist.extend(sl)
                alblist.extend(al)
            else:
                pass
    return songlist, alblist
#process mp3 files to produce a string of info
def convert(file):
    bitrate=("{bitraw}kbps".format(bitraw=(mutagen.File(file).info.bitrate//1000)))
    filesize=round(((os.path.getsize(file)/1024)/1024),1)
    audio = EasyID3(file)
    sec=round((mutagen.File(file).info.length)%60)
    if sec < 10:
        sec = '0' + str(sec)
    length = (f"{int((mutagen.File(file).info.length)//60)}:{sec}")
    return (f"{audio['artist']} : {audio['album']} : {audio['title']} || {bitrate}, {filesize}MB || {length}".replace("[",'').replace("]",'').replace("'",''))
#find and alphabetize all albums, mark if only rip quality
def albums(file):
    audio = EasyID3(file)
    alb=f"{audio['artist']} : {audio['album']}".replace("[",'').replace("]",'').replace("'",'')
    try:
        if (audio['albumartist'])==['Various']:
            cutlist=list(alb.split(":"))
            alb=mixedArtistReplace+":"+str(cutlist[1])+ " :"+str(cutlist[2])
    except:
        pass
    if mutagen.File(file).info.bitrate//1000 < 200:
        alb= '|RIP| ' + alb
    else:
        alb= '|CD|  ' + alb
    return str(alb)
songs,albs=get_mp3_files(cwd)
songs.sort()
albs=set(albs) #destroy duplicate albums
albs=list(albs) #convert back to a useable list
albs.sort()
with open("fullsonglist.txt", "w") as page:
    page.write("Artist : Album : Song || Bitrate, File Size || Length \n\n")
    for i in range(0, (len(songs))):
        page.write(f"{songs[i]}\n")
    page.write(f"\nLast Updated: {datetime.now()}")
    page.close()
    print("Song List Written")
with open("alblist.txt", "w") as page:
    for i in range(0, (len(albs))):
        page.write(f"{albs[i]}\n")
    page.write(f"\nLast Updated: {datetime.now()}")
    page.close()
    print("Album List Written")
print("Done")