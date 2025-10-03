
from dataclasses import dataclass
import os


class SongReaderError(Exception):
    pass

@dataclass
class Song:
    """ A song with its metadata (header) and lyrics."""
    name: str        # filename, with .txt suffix 
    header: dict[str]
    lyrics: list[str]


allowed_tags  = ['title', 'artist', 'score',
                 'youtube', 'tabs', 'lyrics', 'notes']
required_tags = ['title', 'artist', 'score' ]

tag_aliases = {
    'titre': 'title',
    'artiste': 'artist',
    'partition': 'score',
    'paroles': 'lyrics'
}

class SongFileReader:  
    
    """ Read songs from files."""
    
    def read_from(self, file_path):
        """ Read a song from a file. Return a Song object or None if error."""
        with open(file_path, 'r') as f:
            # get attributes from header
            try:
                header = self.get_header(f)   
                lyrics = self.get_body(f) 
                return Song(os.path.basename(file_path), header, lyrics)
            except SongReaderError as e:
                print(f'Error reading "{file_path}": {e}')
        return None

    def get_header(self, file):
        """ Read the header part (metadata) of the song file."""
        header = {}
        line_no = 0
        for line in file:
            line_no += 1
            if line.strip() == '':
                break
            try:
                tag, value = [ x.strip() for x in line.split(':', 1)]
                tag = tag_aliases.get(tag, tag)
                if tag not in allowed_tags:
                   raise SongReaderError(f'unknown tag "{tag}" line {line_no}\n---')
                if tag == "lyrics":
                   break
                # allow repeated tags
                if tag in header:
                    header[tag] = f'{header[tag]}\n{value}'
                else:
                    header[tag] = value
            except ValueError:
                raise SongReaderError(f'tag error line {line_no}\n---')
        for tag in required_tags:
            if tag not in header:
                raise SongReaderError(f'missing required tag "{tag}"\n---')
        return header
 
    def get_body(self, file):
        """ Read the remaining lines, body part (lyrics) of the song file."""
        return [ line for line in file ]
        
