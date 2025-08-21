# Music Playlist Manager

A command-line Python application that simulates a music player with playlist management capabilities. This project demonstrates the use of lists and matrices (dictionaries) to organize and report on music collections.

## Features

- **Music Library Loading**: Automatically scans and loads music files from a specified directory
- **File Type Support**: Handles MP3, FLAC, WAV, M4A, and OGG files
- **Smart Parsing**: Intelligently extracts song information from various filename patterns
- **Artist Filtering**: Filter songs by specific artists
- **File Type Filtering**: Filter songs by audio format
- **Comprehensive Reports**: Generate detailed reports organized by artist, file type, and statistics
- **Library Statistics**: View total song count, file sizes, and distribution information

## File Structure

```
Music_Stream/
├── music/                          # Music files directory
│   ├── *.mp3                      # MP3 audio files
│   ├── *.flac                     # FLAC audio files
│   └── ...                        # Other audio formats
├── music_playlist_manager.py       # Main application file
├── requirements.txt                # Dependencies (none external)
└── README.md                      # This file
```

## Requirements

- Python 3.6 or higher
- No external packages required (uses only standard library)

## Usage

### Basic Usage

1. **Run the application:**
   ```bash
   python music_playlist_manager.py
   ```

2. **The application will automatically:**
   - Load all music files from the `music/` directory
   - Parse filenames to extract song information
   - Generate comprehensive reports
   - Display filtering examples

### Programmatic Usage

```python
from music_playlist_manager import MusicPlaylistManager

# Initialize with your music directory
manager = MusicPlaylistManager("path/to/your/music")

# Load the library
manager.load_music_library()

# Get all songs
all_songs = manager.get_song_library()

# Filter by artist
pantera_songs = manager.filter_songs_by_artist("Pantera")

# Filter by file type
mp3_songs = manager.filter_songs_by_file_type("mp3")

# Generate reports
artist_report = manager.generate_artist_report()
file_type_report = manager.generate_file_type_report()
statistics = manager.get_library_statistics()
```

## Data Structures Used

### Lists
- **Song Library**: Main list containing all song information dictionaries
- **Artist Lists**: Lists of unique artists and their song counts
- **File Type Lists**: Lists of supported audio formats

### Matrices (Dictionaries)
- **Artist Report**: Dictionary mapping artists to lists of their songs
- **File Type Report**: Dictionary mapping file types to lists of songs
- **Statistics**: Dictionary containing comprehensive library metrics

## Filename Parsing

The application intelligently parses various filename patterns:

- **Track - Title**: `01 - Highway Star`
- **Track. Title**: `01. I Don't Know`
- **Track Artist, Title**: `05 Pantera, Cemetary Gates`

## Output Examples

The application generates several types of reports:

1. **Complete Library**: All songs with metadata
2. **Artist Report**: Songs organized by artist
3. **File Type Report**: Songs organized by audio format
4. **Statistics**: Total counts, sizes, and distributions
5. **Filtering Examples**: Demonstrations of search functionality

## Extending the Application

The modular design makes it easy to add new features:

- **New File Formats**: Add extensions to `audio_extensions` set
- **Additional Filters**: Create new filtering methods
- **Enhanced Parsing**: Improve filename parsing logic
- **Metadata Support**: Integrate with audio metadata libraries
- **Playlist Management**: Add playlist creation and management features

## Future Enhancements

- Audio metadata extraction (ID3 tags, FLAC metadata)
- Playlist creation and management
- Audio playback capabilities
- Database storage for large libraries
- Web interface
- Music recommendation algorithms
