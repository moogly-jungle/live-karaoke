#!/usr/bin/python3
import copy
import unicodedata
import os
import sys

source = "playlist.txt"

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
                elif l.startswith("paroles:"):
                    lyrics = True
    def __repr__(self):
        return f'{self.title} - {self.artist}'

    def html_file_name(self):
        return self.base_file_name + ".html"

    def html_link_line(self):
        return f'<li><a href="chansons/{self.html_file_name()}">{self.title}</a></li>'

# liste des chansons
songs = []
files = os.listdir('paroles')
files.sort()
for f in files:
    songs.append(Song('paroles/' + f))

print(f"{len(songs)} chansons au total")

# table des matières
os.system("rm -f chansons.html")
with open("resources/chansons.html.src", "r") as src:
    with open("chansons.html", "w") as dest:
        for line in src:
            if "<!--LIST_OF_SONGS-->" in line:
                dest.write(line)
                for song in songs:
                    dest.write(' '*4 + song.html_link_line() + '\n')
            else:
                dest.write(line)
os.system('mv chansons.html docs/chansons.html')

# Creation des fichiers de paroles
os.system("rm -f docs/chansons/*.html")
for s in songs:
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
                