#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Generate song lists and individual song pages from text files.
Requires jinja2 (pip install jinja2).
"""

import os
import jinja2

template_dir    = 'templates'
lyrics_link_dir = 'chansons'
score_link_dir  = 'partitions'

from songfilereader import SongFileReader    

def get_songs_from_dir(dir_path):
    """ Read all songs from a directory. Return a list of Song objects."""
    song_reader = SongFileReader()
    songs = []
    for file in os.listdir(dir_path):
        if file.endswith('.txt'):
            song = song_reader.read_from(os.path.join(dir_path, file))
            if not song is None:
                songs.append(song)
    return songs

songs = get_songs_from_dir('paroles')

# -------------------------------------------

def csv_escape(text):
    """ 
    Filter for jinja2. Escape text for CSV output.
    """
    if '"' in text or ',' in text:
        text = text.replace('"', '""')
        return f'"{text}"'
    return text

jinja2.filters.FILTERS['csv_escape'] = csv_escape

def latex_escape(text): 
    """
    Filter for jinja2. Escape text for LaTeX output.
    """
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('$', '\\$')
    return text

jinja2.filters.FILTERS['latex_escape'] = latex_escape


# tri des chansons par titre
songs.sort(key=lambda s: s.header.get('title').lower())

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
lyrics_template = jinja_env.get_template('lyrics.html.j2')

def generate_list(result_path, template_path, songs):
    """ Generate a list file from a template and a list of songs."""
    print(f'* generate list "{result_path}" from "{template_path}"')
    template = jinja_env.get_template(template_path)
    with open(result_path, 'w') as f:
        f.write(template.render(songs=songs,
                                lyrics_link_dir=lyrics_link_dir,
                                score_link_dir=score_link_dir))
    # print('- list done')
    
generate_list('docs/chansons.txt', 'liste.txt.j2', songs)
generate_list('docs/chansons.csv', 'simple.csv.j2', songs)
generate_list("docs/chansons.html", 'public-list.html.j2', songs)
generate_list('latex/liste.tex', 'liste.tex.j2', songs)

for song in songs:
    prefix = song.name.removesuffix('.txt')
    output_path = f"docs/{lyrics_link_dir}/{prefix}.html"
    with open(output_path, 'w') as f:
        # print(f'* generate lyrics "{output_path}"')  
        f.write(lyrics_template.render(song=song))
print(f'- all {len(songs)} lyrics done')


