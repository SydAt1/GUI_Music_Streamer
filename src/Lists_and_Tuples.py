import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class MusicPlaylistManager:
    def __init__(self, music_directory: str):
        """Initialize the Music Playlist Manager with a music directory."""
        self.music_directory = Path(music_directory)
        self.song_library = []
        self.artists = set()
        self.file_types = set()
        
        # Load the music library on startup
        self.load_music_library()
        
    def load_music_library(self) -> None:
        """Load all music files from the music directory into the library."""
        if not self.music_directory.exists():
            print(f"Error: Music directory '{self.music_directory}' does not exist.")
            return
            
        # Supported audio file extensions
        audio_extensions = {'.mp3', '.flac', '.wav', '.m4a', '.ogg'}
        
        print("Loading music library...")
        
        for file_path in self.music_directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
                song_info = self._extract_song_info(file_path)
                if song_info:
                    self.song_library.append(song_info)
                    self.artists.add(song_info['artist'])
                    self.file_types.add(song_info['file_type'])
                    
        print(f"Loaded {len(self.song_library)} songs from the music library.")
        
    def _extract_song_info(self, file_path: Path) -> Dict:
        """Extract song information from filename with format 'Artist Name - Song Name'."""
        filename = file_path.stem
        file_type = file_path.suffix.lower()
        
        # Parse filename with format "Artist Name - Song Name"
        if ' - ' in filename:
            parts = filename.split(' - ', 1)
            if len(parts) == 2:
                artist = parts[0].strip()
                title = parts[1].strip()
            else:
                artist = "Unknown Artist"
                title = filename
        else:
            # If no separator found, treat entire filename as title
            artist = "Unknown Artist"
            title = filename
            
        return {
            'filename': filename,
            'title': title,
            'artist': artist,
            'file_type': file_type,
            'file_path': str(file_path),
            'file_size': file_path.stat().st_size
        }
            
    def get_song_library(self) -> List[Dict]:
        """Return the complete song library."""
        return self.song_library
        
    def filter_songs_by_artist(self, artist: str) -> List[Dict]:
        """Filter songs by a specific artist."""
        return [song for song in self.song_library if song['artist'].lower() == artist.lower()]
        
    def filter_songs_by_file_type(self, file_type: str) -> List[Dict]:
        """Filter songs by file type."""
        return [song for song in self.song_library if song['file_type'] == file_type.lower()]
    
    def search_songs(self, query: str) -> List[Dict]:
        """Search songs by title or artist."""
        query_lower = query.lower()
        results = []
        for song in self.song_library:
            if (query_lower in song['title'].lower() or 
                query_lower in song['artist'].lower()):
                results.append(song)
        return results
        
    def get_artists_list(self) -> List[str]:
        """Get a list of all artists in the library."""
        return sorted(list(self.artists))
        
    def get_file_types_list(self) -> List[str]:
        """Get a list of all file types in the library."""
        return sorted(list(self.file_types))
        
    def generate_artist_report(self) -> Dict[str, List[Dict]]:
        """Generate a report organized by artist."""
        report = {}
        for artist in self.artists:
            report[artist] = self.filter_songs_by_artist(artist)
        return report
        
    def generate_file_type_report(self) -> Dict[str, List[Dict]]:
        """Generate a report organized by file type."""
        report = {}
        for file_type in self.file_types:
            report[file_type] = self.filter_songs_by_file_type(file_type)
        return report
        
    def get_library_statistics(self) -> Dict:
        """Get comprehensive statistics about the music library."""
        total_songs = len(self.song_library)
        total_size = sum(song['file_size'] for song in self.song_library)
        
        # Count by artist
        artist_counts = {}
        for song in self.song_library:
            artist = song['artist']
            artist_counts[artist] = artist_counts.get(artist, 0) + 1
            
        # Count by file type
        file_type_counts = {}
        for song in self.song_library:
            file_type = song['file_type']
            file_type_counts[file_type] = file_type_counts.get(file_type, 0) + 1
            
        return {
            'total_songs': total_songs,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'total_size_gb': round(total_size / (1024 * 1024 * 1024), 2),
            'unique_artists': len(self.artists),
            'artist_counts': dict(sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)),
            'file_type_counts': file_type_counts
        }
        
    def display_song_library(self) -> None:
        """Display the complete song library in a formatted way."""
        print("\n" + "="*90)
        print("MUSIC LIBRARY")
        print("="*90)
        print(f"{'#':<3} {'Title':<40} {'Artist':<25} {'Type':<6} {'Size (MB)':<10}")
        print("-"*90)
        
        for i, song in enumerate(self.song_library, 1):
            size_mb = round(song['file_size'] / (1024 * 1024), 2)
            print(f"{i:<3} {song['title'][:39]:<40} {song['artist'][:24]:<25} "
                  f"{song['file_type']:<6} {size_mb:<10}")
            
    def display_artist_report(self) -> None:
        """Display a report organized by artist."""
        print("\n" + "="*80)
        print("ARTIST REPORT")
        print("="*80)
        
        artist_report = self.generate_artist_report()
        for artist, songs in sorted(artist_report.items()):
            print(f"\n{artist.upper()} ({len(songs)} songs):")
            for song in sorted(songs, key=lambda x: x['title']):
                print(f"  • {song['title']} ({song['file_type']})")
                
    def display_file_type_report(self) -> None:
        """Display a report organized by file type."""
        print("\n" + "="*80)
        print("FILE TYPE REPORT")
        print("="*80)
        
        file_type_report = self.generate_file_type_report()
        for file_type, songs in sorted(file_type_report.items()):
            print(f"\n{file_type.upper()} ({len(songs)} files):")
            for song in sorted(songs, key=lambda x: x['artist']):
                print(f"  • {song['title']} - {song['artist']}")
                
    def display_statistics(self) -> None:
        """Display comprehensive library statistics."""
        stats = self.get_library_statistics()
        
        print("\n" + "="*80)
        print("LIBRARY STATISTICS")
        print("="*80)
        print(f"Total Songs: {stats['total_songs']:,}")
        print(f"Total Size: {stats['total_size_gb']:.2f} GB ({stats['total_size_mb']:.1f} MB)")
        print(f"Unique Artists: {stats['unique_artists']}")
        
        print(f"\nTop Artists by Song Count:")
        for artist, count in list(stats['artist_counts'].items())[:10]:
            print(f"  {artist}: {count} songs")
            
        print(f"\nFile Types:")
        for file_type, count in sorted(stats['file_type_counts'].items()):
            print(f"  {file_type.upper()}: {count} songs")

def main():
    """Main function to demonstrate the Music Playlist Manager."""
    # Initialize the manager with the music directory
    music_dir = input("Enter the path to your music directory: ").strip()
    if not music_dir:
        music_dir = r"D:\projects\Music_Stream\music"  # Default path
        
    manager = MusicPlaylistManager(music_dir)
    
    # Load the music library
    manager.load_music_library()
    
    if not manager.song_library:
        print("No music files found in the specified directory.")
        return
    
    # Display various reports and information
    manager.display_song_library()
    manager.display_artist_report()
    manager.display_file_type_report()
    manager.display_statistics()
    
    # Demonstrate filtering functionality
    print("\n" + "="*80)
    print("FILTERING EXAMPLES")
    print("="*80)
    
    # Search functionality
    search_query = input("\nEnter a search term (artist or song): ").strip()
    if search_query:
        print(f"\nSearching for '{search_query}':")
        search_results = manager.search_songs(search_query)
        if search_results:
            for song in search_results[:10]:  # Show first 10 results
                print(f"  • {song['title']} - {song['artist']} ({song['file_type']})")
        else:
            print("  No results found.")
    
    # Show available artists for filtering
    artists = manager.get_artists_list()
    if artists and len(artists) > 0:
        print(f"\nAll Artists ({len(artists)} total):")
        for artist in artists[:15]:  # Show first 15 artists
            songs_count = len(manager.filter_songs_by_artist(artist))
            print(f"  • {artist} ({songs_count} songs)")
        
        if len(artists) > 15:
            print(f"  ... and {len(artists) - 15} more artists")
    
    # Filter by file type examples
    print("\nFile Type Examples:")
    file_types = manager.get_file_types_list()
    for file_type in file_types:
        type_songs = manager.filter_songs_by_file_type(file_type)
        print(f"\n{file_type.upper()} files ({len(type_songs)} total) - First 5:")
        for song in type_songs[:5]:
            print(f"  • {song['title']} - {song['artist']}")

if __name__ == "__main__":
    main()