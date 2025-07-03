#!/usr/bin/python3
import copy
import unicodedata
import os
import sys

form_link = 'https://forms.gle/nma55N8XSGRkphcC8'

def sans_accents(texte):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texte)
        if unicodedata.category(c) != 'Mn'
    )

class Song:
    def __init__(self, file):
        self.base_file_name = file.split('/')[-1].split('.')[0]
        self.title = None
        self.artist = None
        self.youtube = None
        self.partition = None
        self.lyrics = ''
        lyrics = False
        with open(file, "r") as f:
            for l in f:
                if lyrics:
                    self.lyrics += l.strip() + '\n'
                if l.startswith("titre:"):
                    self.title = l.split(':')[1].strip()
                elif l.startswith("artist:"):
                    self.artist = l.split(':')[1].strip()
                elif l.startswith("youtube:"):
                    self.youtube = l[8:].strip()
                elif l.startswith("partition:"):
                    self.partition = 'partitions/'+l[10:].strip()
                elif l.startswith("paroles:"):
                    lyrics = True
    def __repr__(self):
        return f'{self.title} - {self.artist}'

    def html_file_name(self):
        return self.base_file_name + ".html"

    def html_link_line(self):
        return f'<a href="chansons/{self.html_file_name()}">{self.title}</a> - <i>{self.artist}</i>'

# liste des chansons
songs = []
todo = []
dirs = [['paroles', songs], ['todo', todo]]
for d, l in dirs:
    files = os.listdir(d)
    files.sort()
    for f in files:
        l.append(Song(d + '/' + f))

print(f"- {len(songs)} chansons")
print(f"- {len(todo)} todo")

# table des matières
# keys = [["<!--LIST_OF_SONGS-->", songs], ["<!--LIST_OF_TODO-->", todo]]
keys = [["<!--LIST_OF_SONGS-->", songs] ]

os.system("rm -f docs/chansons.html")
with open("resources/chansons.html.src", "r") as src:
    with open("chansons.html", "w") as dest:
        for line in src:
            for k, song_list in keys:
                if k in line:
                    dest.write(line)
                    for n, song in enumerate(song_list):
                        if song.youtube is not None:
                            youtube_link = f'- <a href="{song.youtube}">YouTube</a>'
                        if song.partition is not None:
                            partition_link = f'- <a href="{song.partition}">Partition</a>'
                        else: partition_link = ''    
                        dest.write(f'     <li>{n+1}. {song.html_link_line()} {youtube_link} {partition_link}</li>\n')
            dest.write(line)
os.system('mv chansons.html docs/chansons.html')

# Creation des fichiers de paroles
os.system("rm -f docs/chansons/*.html")
for s in songs + todo:
    html_file = 'docs/chansons/' + s.html_file_name()
    with open(html_file, "w") as dest:
        with open('resources/parole.html.src', "r") as src:
            for line in src:
                line = line.replace('TITLE', s.title)
                line = line.replace('ARTIST', s.artist)
                dest.write(line)
                if  '<!--LYRICS-->' in line:
                    lyr = s.lyrics.split('\n')
                    for l in lyr:
                            dest.write(' '*4 + l.strip() + '\n')
                if  '<!--YOUTUBE_LINK-->' in line:
                    if s.youtube is not None:
                        dest.write('&nbsp;'*4 + f'<a href="{s.youtube}">[youtube]</a>\n')
                