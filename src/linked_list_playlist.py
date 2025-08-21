#!/usr/bin/env python3
"""
Linked List Playlist Implementation
Week 4: Linked Lists where nodes are songs
"""

from typing import Optional, List, Dict
from Lists_and_Tuples import MusicPlaylistManager

class SongNode:
    """Node class representing a song in the linked list playlist."""
    
    def __init__(self, song_data: Dict):
        self.song_data = song_data
        self.next: Optional[SongNode] = None
        self.previous: Optional[SongNode] = None
    
    def __str__(self) -> str:
        return f"{self.song_data['title']} - {self.song_data['artist']}"

class LinkedListPlaylist:
    """Doubly linked list implementation for a music playlist."""
    
    def __init__(self):
        self.head: Optional[SongNode] = None
        self.tail: Optional[SongNode] = None
        self.current_node: Optional[SongNode] = None
        self.size = 0
    
    def is_empty(self) -> bool:
        """Check if the playlist is empty."""
        return self.head is None
    
    def get_size(self) -> int:
        """Get the number of songs in the playlist."""
        return self.size
    
    def add_song_at_end(self, song_data: Dict) -> None:
        """Add a song at the end of the playlist."""
        new_node = SongNode(song_data)
        
        if self.is_empty():
            # First song in playlist
            self.head = new_node
            self.tail = new_node
            self.current_node = new_node
        else:
            # Add to end
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
        print(f"Added: {new_node}")
    
    def add_song_at_beginning(self, song_data: Dict) -> None:
        """Add a song at the beginning of the playlist."""
        new_node = SongNode(song_data)
        
        if self.is_empty():
            # First song in playlist
            self.head = new_node
            self.tail = new_node
            self.current_node = new_node
        else:
            # Add to beginning
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
        
        self.size += 1
        print(f"Added at beginning: {new_node}")
    
    def insert_song_after(self, target_song_title: str, song_data: Dict) -> bool:
        """Insert a song after a specific song in the playlist."""
        if self.is_empty():
            print("Playlist is empty. Cannot insert after specific song.")
            return False
        
        current = self.head
        while current:
            if current.song_data['title'].lower() == target_song_title.lower():
                new_node = SongNode(song_data)
                
                # Insert after current node
                new_node.next = current.next
                new_node.previous = current
                
                if current.next:
                    current.next.previous = new_node
                else:
                    # Inserting at end
                    self.tail = new_node
                
                current.next = new_node
                self.size += 1
                print(f"Inserted after '{target_song_title}': {new_node}")
                return True
            
            current = current.next
        
        print(f"Song '{target_song_title}' not found in playlist.")
        return False
    
    def insert_song_before(self, target_song_title: str, song_data: Dict) -> bool:
        """Insert a song before a specific song in the playlist."""
        if self.is_empty():
            print("Playlist is empty. Cannot insert before specific song.")
            return False
        
        current = self.head
        while current:
            if current.song_data['title'].lower() == target_song_title.lower():
                new_node = SongNode(song_data)
                
                # Insert before current node
                new_node.next = current
                new_node.previous = current.previous
                
                if current.previous:
                    current.previous.next = new_node
                else:
                    # Inserting at beginning
                    self.head = new_node
                
                current.previous = new_node
                self.size += 1
                print(f"Inserted before '{target_song_title}': {new_node}")
                return True
            
            current = current.next
        
        print(f"Song '{target_song_title}' not found in playlist.")
        return False
    
    def remove_song(self, song_title: str) -> bool:
        """Remove a song from the playlist by title."""
        if self.is_empty():
            print("Playlist is empty. Nothing to remove.")
            return False
        
        current = self.head
        while current:
            if current.song_data['title'].lower() == song_title.lower():
                # Update current_node if we're removing it
                if self.current_node == current:
                    if current.next:
                        self.current_node = current.next
                    elif current.previous:
                        self.current_node = current.previous
                    else:
                        self.current_node = None
                
                # Remove the node
                if current.previous:
                    current.previous.next = current.next
                else:
                    # Removing head
                    self.head = current.next
                
                if current.next:
                    current.next.previous = current.previous
                else:
                    # Removing tail
                    self.tail = current.previous
                
                self.size -= 1
                print(f"Removed: {current}")
                return True
            
            current = current.next
        
        print(f"Song '{song_title}' not found in playlist.")
        return False
    
    def next_song(self) -> Optional[Dict]:
        """Move to the next song and return its data."""
        if not self.current_node or not self.current_node.next:
            print("No next song available.")
            return None
        
        self.current_node = self.current_node.next
        print(f"Now playing: {self.current_node}")
        return self.current_node.song_data
    
    def previous_song(self) -> Optional[Dict]:
        """Move to the previous song and return its data."""
        if not self.current_node or not self.current_node.previous:
            print("No previous song available.")
            return None
        
        self.current_node = self.current_node.previous
        print(f"Now playing: {self.current_node}")
        return self.current_node.song_data
    
    def get_current_song(self) -> Optional[Dict]:
        """Get the current song data."""
        if not self.current_node:
            print("No song is currently selected.")
            return None
        
        return self.current_node.song_data
    
    def go_to_first_song(self) -> Optional[Dict]:
        """Go to the first song in the playlist."""
        if self.is_empty():
            print("Playlist is empty.")
            return None
        
        self.current_node = self.head
        print(f"Now at first song: {self.current_node}")
        return self.current_node.song_data
    
    def go_to_last_song(self) -> Optional[Dict]:
        """Go to the last song in the playlist."""
        if self.is_empty():
            print("Playlist is empty.")
            return None
        
        self.current_node = self.tail
        print(f"Now at last song: {self.current_node}")
        return self.current_node.song_data
    
    def display_playlist(self) -> None:
        """Display the entire playlist."""
        if self.is_empty():
            print("Playlist is empty.")
            return
        
        print(f"\n{'='*60}")
        print(f"PLAYLIST ({self.size} songs)")
        print(f"{'='*60}")
        
        current = self.head
        position = 1
        
        while current:
            # Mark current song with ▶️
            marker = "▶️ " if current == self.current_node else "   "
            print(f"{marker}{position:2d}. {current}")
            current = current.next
            position += 1
    
    def search_song(self, query: str) -> Optional[SongNode]:
        """Search for a song by title or artist."""
        if self.is_empty():
            return None
        
        current = self.head
        while current:
            if (query.lower() in current.song_data['title'].lower() or 
                query.lower() in current.song_data['artist'].lower()):
                return current
            current = current.next
        
        return None
    
    def reverse_playlist(self) -> None:
        """Reverse the order of songs in the playlist."""
        if self.size <= 1:
            return
        
        # Swap head and tail
        self.head, self.tail = self.tail, self.head
        
        # Reverse all links
        current = self.head
        while current:
            # Swap next and previous pointers
            current.next, current.previous = current.previous, current.next
            current = current.previous
        
        # Update current_node if it exists
        if self.current_node:
            # Find the new position of the current song
            temp = self.head
            while temp:
                if temp.song_data == self.current_node.song_data:
                    self.current_node = temp
                    break
                temp = temp.next
        
        print("Playlist reversed!")
    
    def shuffle_playlist(self) -> None:
        """Shuffle the playlist using a simple algorithm."""
        if self.size <= 1:
            return
        
        # Convert to list for shuffling
        songs = []
        current = self.head
        while current:
            songs.append(current.song_data)
            current = current.next
        
        # Simple shuffle: swap random pairs
        import random
        for _ in range(self.size * 2):  # Multiple swaps for better randomization
            i = random.randint(0, self.size - 1)
            j = random.randint(0, self.size - 1)
            if i != j:
                songs[i], songs[j] = songs[j], songs[i]
        
        # Rebuild the linked list
        self.head = None
        self.tail = None
        self.size = 0
        
        for song in songs:
            self.add_song_at_end(song)
        
        # Reset current node to first song
        self.current_node = self.head
        print("Playlist shuffled!")

class PlaylistManager:
    """Manager class for creating and managing multiple playlists."""
    
    def __init__(self):
        self.playlists: Dict[str, LinkedListPlaylist] = {}
        self.current_playlist_name: Optional[str] = None
    
    def create_playlist(self, name: str, description: str = "") -> bool:
        """Create a new empty playlist."""
        if name in self.playlists:
            print(f"Playlist '{name}' already exists.")
            return False
        
        new_playlist = LinkedListPlaylist()
        self.playlists[name] = new_playlist
        self.current_playlist_name = name
        
        print(f"✅ Created new playlist: '{name}'")
        if description:
            print(f"   Description: {description}")
        
        return True
    
    def delete_playlist(self, name: str) -> bool:
        """Delete a playlist."""
        if name not in self.playlists:
            print(f"Playlist '{name}' not found.")
            return False
        
        if self.current_playlist_name == name:
            self.current_playlist_name = None
        
        del self.playlists[name]
        print(f"🗑️  Deleted playlist: '{name}'")
        return True
    
    def switch_playlist(self, name: str) -> bool:
        """Switch to a different playlist."""
        if name not in self.playlists:
            print(f"Playlist '{name}' not found.")
            return False
        
        self.current_playlist_name = name
        print(f"🔄 Switched to playlist: '{name}'")
        return True
    
    def get_current_playlist(self) -> Optional[LinkedListPlaylist]:
        """Get the currently active playlist."""
        if not self.current_playlist_name:
            return None
        return self.playlists.get(self.current_playlist_name)
    
    def list_playlists(self) -> None:
        """List all available playlists."""
        if not self.playlists:
            print("No playlists created yet.")
            return
        
        print(f"\n{'='*50}")
        print("📋 AVAILABLE PLAYLISTS")
        print(f"{'='*50}")
        
        for i, (name, playlist) in enumerate(self.playlists.items(), 1):
            current_marker = " ▶️" if name == self.current_playlist_name else ""
            print(f"{i:2d}. {name} ({playlist.get_size()} songs){current_marker}")
    
    def add_song_to_current_playlist(self, song_data: Dict) -> bool:
        """Add a song to the current playlist."""
        current_playlist = self.get_current_playlist()
        if not current_playlist:
            print("No playlist selected. Please create or switch to a playlist first.")
            return False
        
        current_playlist.add_song_at_end(song_data)
        return True
    
    def create_playlist_from_library(self, name: str, music_manager: MusicPlaylistManager, 
                                   max_songs: int = 10, description: str = "") -> bool:
        """Create a new playlist and populate it with songs from the library."""
        if not self.create_playlist(name, description):
            return False
        
        song_library = music_manager.get_song_library()
        if not song_library:
            print("No songs found in library.")
            return False
        
        # Add songs to the new playlist
        songs_to_add = song_library[:max_songs]
        current_playlist = self.playlists[name]
        
        for song in songs_to_add:
            current_playlist.add_song_at_end(song)
        
        print(f"📚 Populated playlist '{name}' with {len(songs_to_add)} songs from library.")
        return True

def load_playlist_from_library(music_manager: MusicPlaylistManager, max_songs: int = 10) -> LinkedListPlaylist:
    """Load songs from the music library into a linked list playlist."""
    playlist = LinkedListPlaylist()
    song_library = music_manager.get_song_library()
    
    if not song_library:
        print("No songs found in library.")
        return playlist
    
    # Add songs to playlist (limit to max_songs)
    songs_to_add = song_library[:max_songs]
    
    for song in songs_to_add:
        playlist.add_song_at_end(song)
    
    print(f"Loaded {len(songs_to_add)} songs into playlist.")
    return playlist

def demonstrate_linked_list_operations(playlist: LinkedListPlaylist) -> None:
    """Demonstrate various linked list operations."""
    print("\n" + "="*60)
    print("LINKED LIST PLAYLIST OPERATIONS DEMONSTRATION")
    print("="*60)
    
    # Show initial playlist
    playlist.display_playlist()
    
    # Navigate through playlist
    print("\n--- Navigation Demo ---")
    playlist.go_to_first_song()
    print(f"Current song: {playlist.get_current_song()['title']}")
    
    if playlist.size > 1:
        playlist.next_song()
        print(f"Next song: {playlist.get_current_song()['title']}")
    
    if playlist.size > 2:
        playlist.next_song()
        print(f"Next song: {playlist.get_current_song()['title']}")
    
    # Insert a new song
    print("\n--- Insertion Demo ---")
    new_song = {
        'title': 'Demo Song',
        'artist': 'Demo Artist',
        'file_type': '.mp3',
        'file_path': 'demo/path',
        'file_size': 1024
    }
    
    # Insert after current song
    current_title = playlist.get_current_song()['title']
    playlist.insert_song_after(current_title, new_song)
    
    # Show updated playlist
    playlist.display_playlist()
    
    # Remove a song
    print("\n--- Deletion Demo ---")
    if playlist.size > 1:
        first_song = playlist.head.song_data['title']
        playlist.remove_song(first_song)
        playlist.display_playlist()
    
    # Search functionality
    print("\n--- Search Demo ---")
    search_result = playlist.search_song("Demo")
    if search_result:
        print(f"Found: {search_result}")
    else:
        print("No songs found matching 'Demo'")
    
    # Shuffle demo
    print("\n--- Shuffle Demo ---")
    playlist.shuffle_playlist()
    playlist.display_playlist()

def main():
    """Main function to demonstrate the linked list playlist."""
    print("🎵 LINKED LIST PLAYLIST IMPLEMENTATION 🎵")
    print("=" * 60)
    
    # Initialize music manager
    music_dir = input("Enter music directory path (or press Enter for default): ").strip()
    if not music_dir:
        music_dir = r"D:\projects\Music_Stream\music"
    
    try:
        music_manager = MusicPlaylistManager(music_dir)
        song_library = music_manager.get_song_library()
        
        if not song_library:
            print("No songs found in library.")
            return
        
        print(f"Found {len(song_library)} songs in library.")
        
        # Load songs into linked list playlist
        playlist = load_playlist_from_library(music_manager, max_songs=8)
        
        if playlist.is_empty():
            print("Failed to load songs into playlist.")
            return
        
        # Demonstrate linked list operations
        demonstrate_linked_list_operations(playlist)
        
        # Interactive menu
        while True:
            print("\n" + "=" * 50)
            print("LINKED LIST PLAYLIST MENU")
            print("=" * 50)
            print("1. Display Playlist")
            print("2. Next Song")
            print("3. Previous Song")
            print("4. Go to First Song")
            print("5. Go to Last Song")
            print("6. Add Song at End")
            print("7. Insert Song After")
            print("8. Remove Song")
            print("9. Search Song")
            print("10. Shuffle Playlist")
            print("11. Reverse Playlist")
            print("12. Exit")
            print("-" * 50)
            
            choice = input("Enter your choice (1-12): ").strip()
            
            if choice == '1':
                playlist.display_playlist()
            
            elif choice == '2':
                playlist.next_song()
            
            elif choice == '3':
                playlist.previous_song()
            
            elif choice == '4':
                playlist.go_to_first_song()
            
            elif choice == '5':
                playlist.go_to_last_song()
            
            elif choice == '6':
                title = input("Enter song title: ").strip()
                artist = input("Enter artist name: ").strip()
                if title and artist:
                    new_song = {
                        'title': title,
                        'artist': artist,
                        'file_type': '.mp3',
                        'file_path': 'manual/entry',
                        'file_size': 1024
                    }
                    playlist.add_song_at_end(new_song)
            
            elif choice == '7':
                target = input("Enter song title to insert after: ").strip()
                title = input("Enter new song title: ").strip()
                artist = input("Enter new artist name: ").strip()
                if target and title and artist:
                    new_song = {
                        'title': title,
                        'artist': artist,
                        'file_type': '.mp3',
                        'file_path': 'manual/entry',
                        'file_size': 1024
                    }
                    playlist.insert_song_after(target, new_song)
            
            elif choice == '8':
                title = input("Enter song title to remove: ").strip()
                if title:
                    playlist.remove_song(title)
            
            elif choice == '9':
                query = input("Enter search term: ").strip()
                if query:
                    result = playlist.search_song(query)
                    if result:
                        print(f"Found: {result}")
                    else:
                        print("No songs found.")
            
            elif choice == '10':
                playlist.shuffle_playlist()
            
            elif choice == '11':
                playlist.reverse_playlist()
            
            elif choice == '12':
                print("Goodbye! 🎵")
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
