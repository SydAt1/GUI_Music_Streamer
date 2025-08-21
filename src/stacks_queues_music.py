import pygame
from .Lists_and_Tuples import MusicPlaylistManager

class SongQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, song):
        self.queue.append(song)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def get_size(self):
        return len(self.queue)

    def clear_queue(self):
        self.queue.clear()

    def display_queue(self):
        for i, song in enumerate(self.queue, 1):
            print(f"{i}. {song['title']} - {song['artist']}")

class PrioritySongQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, song, priority=0):
        self.queue.append((song, priority))
        self.queue.sort(key=lambda x: x[1], reverse=True)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)[0]
        return None

    def get_size(self):
        return len(self.queue)

    def clear_queue(self):
        self.queue.clear()

    def display_queue(self):
        for i, (song, priority) in enumerate(self.queue, 1):
            print(f"{i}. {song['title']} - {song['artist']} (Priority: {priority})")

    def upvote(self, song_title):
        for i, (song, priority) in enumerate(self.queue):
            if song['title'].lower() == song_title.lower():
                self.queue[i] = (song, priority + 1)
                self.queue.sort(key=lambda x: x[1], reverse=True)
                return True
        return False

class ListeningHistoryStack:
    def __init__(self):
        self.stack = []

    def push(self, song):
        self.stack.append(song)

    def get_size(self):
        return len(self.stack)

    def display_history(self, limit=10):
        for i, song in enumerate(self.stack[-limit:], 1):
            print(f"{i}. {song['title']} - {song['artist']}")

    def search_history(self, query):
        return [song for song in self.stack if query.lower() in song['title'].lower() or query.lower() in song['artist'].lower()]

class MusicPlayerStacksQueues:
    def __init__(self, music_manager):
        pygame.mixer.init()
        self.music_manager = music_manager
        self.play_next_queue = SongQueue()
        self.party_queue = PrioritySongQueue()
        self.listening_history = ListeningHistoryStack()
        self.currently_playing = None

    def play_song(self, song):
        try:
            pygame.mixer.music.load(song['file_path'])
            pygame.mixer.music.play()
            self.currently_playing = song
            self.listening_history.push(song)
            print(f"🎵 Playing: {song['title']} - {song['artist']}")
        except pygame.error as e:
            print(f"❌ Error playing song: {e}")
            self.currently_playing = None

    def stop_song(self):
        pygame.mixer.music.stop()
        self.currently_playing = None

    def add_to_play_next(self, song):
        self.play_next_queue.enqueue(song)

    def play_next_song(self):
        song = self.play_next_queue.dequeue()
        if song:
            self.play_song(song)
        else:
            print("No songs in play next queue.")

    def add_to_party_queue(self, song, priority=0):
        self.party_queue.enqueue(song, priority)

    def play_from_party_queue(self):
        song = self.party_queue.dequeue()
        if song:
            self.play_song(song)
        else:
            print("No songs in party queue.")

    def upvote_song_in_party_queue(self, song_title):
        if self.party_queue.upvote(song_title):
            print(f"Upvoted: {song_title}")
        else:
            print(f"Song not found in party queue: {song_title}")

    def display_all_queues(self):
        print("\nPlay Next Queue:")
        self.play_next_queue.display_queue()
        print("\nParty Queue:")
        self.party_queue.display_queue()
        print("\nListening History:")
        self.listening_history.display_history()