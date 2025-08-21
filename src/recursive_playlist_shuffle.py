#!/usr/bin/env python3
"""
Simple Recursive Playlist Shuffle
Demonstrates recursion for shuffling playlist song order
"""

import random
import os
import sys
from typing import List, Dict

# Add the src directory to the path so we can import Lists_and_Tuples
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Lists_and_Tuples import MusicPlaylistManager

def recursive_shuffle_playlist(playlist: List[Dict], depth: int = 0) -> List[Dict]:
    """
    Recursively shuffle a playlist using divide-and-conquer approach.
    
    Args:
        playlist: List of song dictionaries
        depth: Current recursion depth (for safety)
    
    Returns:
        Shuffled list of songs
    """
    # Safety check to prevent infinite recursion
    if depth > 50:
        print("Warning: Max recursion depth reached, using simple shuffle")
        return random.sample(playlist, len(playlist))
    
    # Base cases
    if len(playlist) <= 1:
        return playlist
    
    if len(playlist) == 2:
        # Randomly swap or keep order
        return playlist if random.random() < 0.5 else playlist[::-1]
    
    # Divide: split playlist in half
    mid = len(playlist) // 2
    left_half = playlist[:mid]
    right_half = playlist[mid:]
    
    # Recursively shuffle each half
    shuffled_left = recursive_shuffle_playlist(left_half, depth + 1)
    shuffled_right = recursive_shuffle_playlist(right_half, depth + 1)
    
    # Conquer: merge halves with random interleaving
    return merge_with_random_order(shuffled_left, shuffled_right, depth + 1)

def merge_with_random_order(left: List[Dict], right: List[Dict], depth: int) -> List[Dict]:
    """Recursively merge two lists with random ordering decisions."""
    if depth > 50:
        # Fallback to simple merge if recursion too deep
        result = []
        left_idx = right_idx = 0
        
        while left_idx < len(left) and right_idx < len(right):
            if random.random() < 0.5:
                result.append(left[left_idx])
                left_idx += 1
            else:
                result.append(right[right_idx])
                right_idx += 1
        
        result.extend(left[left_idx:])
        result.extend(right[right_idx:])
        return result
    
    # Recursive merge
    if not left:
        return right
    if not right:
        return left
    
    # Randomly choose which list to take from next
    if random.random() < 0.5:
        return [left[0]] + merge_with_random_order(left[1:], right, depth + 1)
    else:
        return [right[0]] + merge_with_random_order(left, right, depth + 1)

def main():
    """Demonstrate the recursive shuffle function."""
    print("🎵 Simple Recursive Playlist Shuffle 🎵")
    print("=" * 50)
    
    # Initialize music manager
    music_dir = input("Enter music directory path (or press Enter for default): ").strip()
    if not music_dir:
        music_dir = r"D:\projects\Music_Stream\music"
    
    # Check if directory exists
    if not os.path.exists(music_dir):
        print(f"Error: Music directory '{music_dir}' does not exist!")
        print("Current working directory:", os.getcwd())
        print("Available directories:")
        for item in os.listdir('.'):
            if os.path.isdir(item):
                print(f"  - {item}")
        return
    
    print(f"Using music directory: {music_dir}")
    
    try:
        music_manager = MusicPlaylistManager(music_dir)
        song_library = music_manager.get_song_library()
        
        print(f"Song library loaded. Found {len(song_library)} songs.")
        
        if not song_library:
            print("No songs found in library. Checking directory contents...")
            # List what's actually in the music directory
            if os.path.exists(music_dir):
                print(f"Contents of {music_dir}:")
                for item in os.listdir(music_dir):
                    print(f"  - {item}")
            return
        
        # Create a simple playlist with first 10 songs
        playlist = song_library[:10]
        
        print("\nOriginal playlist order:")
        for i, song in enumerate(playlist, 1):
            print(f"{i:2d}. {song['title']} - {song['artist']}")
        
        # Shuffle recursively
        print("\nShuffling playlist recursively...")
        shuffled_playlist = recursive_shuffle_playlist(playlist)
        
        print("\nShuffled playlist order:")
        for i, song in enumerate(shuffled_playlist, 1):
            print(f"{i:2d}. {song['title']} - {song['artist']}")
        
        print("\nRecursive shuffle completed! 🎵")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
