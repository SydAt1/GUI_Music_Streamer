# Music Stream

A feature-rich music player application built with Python and Pygame that provides both a command-line interface and an interactive graphical interface for managing and playing your music collection. This project demonstrates the use of various data structures including lists, dictionaries, linked lists, stacks, and queues.

## Features

### Music Library Management
- **Music Library Loading**: Automatically scans and loads music files from a specified directory
- **File Type Support**: Handles MP3, FLAC, WAV, M4A, and OGG files
- **Smart Parsing**: Intelligently extracts song information from various filename patterns
- **Artist Filtering**: Filter songs by specific artists
- **File Type Filtering**: Filter songs by audio format
- **Search**: Search for specific songs in your library
- **Comprehensive Reports**: Generate detailed reports organized by artist, file type, and statistics
- **Library Statistics**: View total song count, file sizes, and distribution information

### Playlist Management
- Create and manage multiple playlists
- Add songs to playlists from your library
- Insert songs at specific positions
- Remove songs from playlists
- Search within playlists
- Shuffle playlist songs

### Advanced Playback Features
- Play/pause, stop, and navigate between songs
- Volume control
- Progress tracking
- Play Next queue for on-the-fly song additions
- Party Mode queue with voting system

### History and Status
- View recently played songs
- Search playback history
- View application status and statistics

## File Structure

```
Music_Stream/
├── music/                          # Music files directory
│   ├── *.mp3                      # MP3 audio files
│   ├── *.flac                     # FLAC audio files
│   └── ...                        # Other audio formats
├── main.py                         # Command-line interface
├── main_gui.py                     # Graphical user interface
├── playlists/                      # Saved playlists directory
├── playlists.json                  # Playlist configuration
├── src/                            # Source code modules
│   ├── Lists_and_Tuples.py        # Basic music library management
│   ├── linked_list_playlist.py    # Playlist implementation using linked lists
│   ├── stacks_queues_music.py     # Play history and queues implementation
│   └── recursive_playlist_shuffle.py # Playlist shuffling algorithms
└── README.md                      # This file
```

## Requirements

- Python 3.6 or higher
- Pygame (for GUI version)
- Standard library modules

## Usage

### Command-line Interface

1. **Run the command-line application:**
   ```bash
   python main.py
   ```

2. **The application will automatically:**
   - Load all music files from the `music/` directory
   - Parse filenames to extract song information
   - Generate comprehensive reports
   - Display filtering examples

### Graphical User Interface

1. **Run the GUI application:**
   ```bash
   python main_gui.py
   ```

2. **Interface Navigation:**
   - **Library Tab**: Browse and search your music collection
   - **Playlists Tab**: Create and manage playlists
   - **Queues Tab**: Manage Play Next and Party Mode queues
   - **History Tab**: View and search playback history
   - **Status Tab**: View application statistics
   - **Now Playing Tab**: Control currently playing song

3. **Keyboard Shortcuts:**
   - Space: Play/Pause
   - Left/Right Arrow: Previous/Next song
   - Up/Down Arrow: Volume control

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

### Lists and Dictionaries
- **Song Library**: Main list containing all song information dictionaries
- **Artist Lists**: Lists of unique artists and their song counts
- **File Type Lists**: Lists of supported audio formats
- **Artist Report**: Dictionary mapping artists to lists of their songs
- **File Type Report**: Dictionary mapping file types to lists of songs
- **Statistics**: Dictionary containing comprehensive library metrics

### Linked Lists
- **Playlists**: Doubly linked lists for efficient playlist navigation and manipulation
- **Song Nodes**: Individual nodes containing song data and references to next/previous songs

### Stacks and Queues
- **Play History**: Stack implementation for tracking recently played songs
- **Play Next Queue**: Queue implementation for upcoming songs
- **Party Mode Queue**: Priority queue with voting system

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
