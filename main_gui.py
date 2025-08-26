#!/usr/bin/env python3
"""
Pygame GUI for Music Streamer
Integrates all music player features into a graphical interface.
"""

import os
import sys
import json
import pygame
from pygame.locals import *

# Add src directory to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.Lists_and_Tuples import MusicPlaylistManager
from src.linked_list_playlist import PlaylistManager, LinkedListPlaylist
from src.stacks_queues_music import MusicPlayerStacksQueues

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60
MUSIC_END = USEREVENT + 1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (30, 30, 30)
BLUE = (50, 150, 255)
GREEN = (50, 200, 100)
RED = (200, 50, 50)
YELLOW = (255, 200, 50)

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, text_color=WHITE, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.hover_color = (min(color[0]+50,255), min(color[1]+50,255), min(color[2]+50,255))
        self.hovered = False
    
    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, width=1, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event, pos):
        self.hovered = self.rect.collidepoint(pos)
        if event.type == MOUSEBUTTONDOWN and self.hovered:
            return True
        return False

class TextInput:
    def __init__(self, x, y, width, height, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False
        self.font = pygame.font.Font(None, font_size)
        self.color = LIGHT_GRAY
        self.active_color = WHITE
        self.text_color = BLACK
    
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if self.active and event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == K_RETURN:
                pass  # Handle in caller
            else:
                self.text += event.unicode
        return self.active
    
    def draw(self, screen):
        color = self.active_color if self.active else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, GRAY, self.rect, width=1, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 5))

class ScrollableList:
    def __init__(self, x, y, width, height, items=[], font_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.items = items  # List of strings or dicts
        self.font = pygame.font.Font(None, font_size)
        self.scroll_offset = 0
        self.item_height = 30
        self.selected_index = -1
        self.is_dict = False
    
    def set_items(self, items):
        self.items = items
        self.scroll_offset = 0
        self.selected_index = -1
        self.is_dict = items and isinstance(items[0], dict)
    
    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GRAY, self.rect, border_radius=10)
        pygame.draw.rect(screen, GRAY, self.rect, width=2, border_radius=10)
        screen.set_clip(self.rect)
        
        for i, item in enumerate(self.items):
            y_pos = self.rect.y + 5 + (i * self.item_height) - self.scroll_offset
            if y_pos + self.item_height < self.rect.y or y_pos > self.rect.bottom:
                continue
            
            color = YELLOW if i == self.selected_index else WHITE
            if self.is_dict:
                text = f"{item['title']} - {item['artist']}"
            else:
                text = str(item)
            text_surf = self.font.render(text, True, color)
            screen.blit(text_surf, (self.rect.x + 15, y_pos))
        
        screen.set_clip(None)
        
        # Scrollbar
        total_height = len(self.items) * self.item_height
        if total_height > self.rect.height:
            bar_height = max(20, self.rect.height * (self.rect.height / total_height))
            bar_y = self.rect.y + (self.scroll_offset / total_height) * self.rect.height
            pygame.draw.rect(screen, LIGHT_GRAY, (self.rect.right - 10, bar_y, 8, bar_height), border_radius=4)
    
    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            rel_y = pos[1] - self.rect.y + self.scroll_offset - 5
            index = rel_y // self.item_height
            if 0 <= index < len(self.items):
                self.selected_index = index
                return self.items[index]
        return None
    
    def handle_scroll(self, direction):
        step = self.item_height * 3 if abs(direction) > 1 else self.item_height
        self.scroll_offset += -step * direction
        self.scroll_offset = max(0, min(self.scroll_offset, len(self.items) * self.item_height - self.rect.height + 10))

class TextDisplay:
    def __init__(self, x, y, width, height, font_size=20):
        self.list = ScrollableList(x, y, width, height, font_size=font_size)
    
    def set_text(self, text):
        lines = text.split('\n')
        self.list.set_items(lines)
    
    def draw(self, screen):
        self.list.draw(screen)
    
    def handle_scroll(self, direction):
        self.list.handle_scroll(direction)

class GUIMusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(MUSIC_END)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Go Streamer")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize components
        self.music_dir = r"D:\projects\Music_Stream\music"
        self.music_manager = None
        self.playlist_manager = None
        self.stacks_queues_player = None
        self.playing_playlist = None
        self.modal = None
        self.message = ""
        self.message_timer = 0
        self.library_view = 'all'
        self.selected_artist = None
        self.selected_file_type = None
        self.current_duration = 0
        self.progress_rect = pygame.Rect(SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT - 150, 600, 20)
        self.playlist_descriptions = {}  # Store playlist descriptions
        
        if not self.initialize_music_library():
            print("Failed to initialize. Exiting.")
            sys.exit(1)
        
        # Tabs
        self.tabs = ["Library", "Playlists", "Queues", "History", "Status", "Now Playing"]
        self.current_tab = "library"
        self.tab_buttons = []
        for i, tab in enumerate(self.tabs):
            btn = Button(20 + i*140, 10, 130, 40, tab, color=GRAY, font_size=26)
            self.tab_buttons.append(btn)
        
        # Library tab
        self.library_list = ScrollableList(20, 100, SCREEN_WIDTH - 40, 500)
        self.library_all_btn = Button(20, 60, 100, 30, "All Songs", GREEN)
        self.library_artist_btn = Button(130, 60, 100, 30, "By Artist", GREEN)
        self.library_type_btn = Button(240, 60, 120, 30, "By File Type", GREEN)
        self.library_stats_btn = Button(370, 60, 100, 30, "Statistics", GREEN)
        self.library_back_btn = Button(480, 60, 80, 30, "Back", RED, font_size=20)
        self.library_search_input = TextInput(580, 60, 300, 30)
        self.library_search_btn = Button(890, 60, 100, 30, "Search")
        self.refresh_library()
        
        # Playlists tab
        self.playlists_list = ScrollableList(20, 100, 300, 550)
        self.playlist_songs_list = ScrollableList(330, 100, 920, 550)
        self.playlist_buttons = [
            Button(20, 660, 140, 40, "List All"),
            Button(170, 660, 140, 40, "Create New"),
            Button(320, 660, 140, 40, "Create from Lib"),
            Button(470, 660, 140, 40, "Switch"),
            Button(620, 660, 140, 40, "Delete"),
            Button(770, 660, 140, 40, "Add Song"),
            Button(920, 660, 140, 40, "Insert After"),
            Button(1070, 660, 140, 40, "Remove Song"),
            Button(20, 710, 140, 40, "Search Song"),
            Button(170, 710, 140, 40, "Shuffle"),
            Button(320, 710, 140, 40, "Play Playlist"),
            Button(470, 710, 140, 40, "Display"),
            Button(620, 710, 140, 40, "First Song"),
            Button(770, 710, 140, 40, "Last Song"),
            Button(920, 710, 140, 40, "Next Song"),
            Button(1070, 710, 140, 40, "Prev Song")
        ]
        self.refresh_playlists()
        
        # Queues tab
        self.play_next_list = ScrollableList(20, 100, 600, 300)
        self.party_list = ScrollableList(640, 100, 600, 300)
        self.queues_buttons = [
            Button(20, 410, 140, 40, "Add to Next"),
            Button(170, 410, 140, 40, "Play Next"),
            Button(320, 410, 140, 40, "Clear Next"),
            Button(640, 410, 140, 40, "Add to Party"),
            Button(790, 410, 140, 40, "Upvote"),
            Button(940, 410, 140, 40, "Play Party"),
            Button(1090, 410, 140, 40, "Clear Party"),
            Button(20, 760, 140, 40, "View History"),
            Button(170, 760, 140, 40, "Search History")
        ]
        self.refresh_queues()
        
        # History tab
        self.history_display = ScrollableList(20, 100, SCREEN_WIDTH - 40, 650)
        self.history_search_btn = Button(20, 760, 140, 40, "Search")
        self.history_search_input = TextInput(170, 760, 300, 40)
        self.refresh_history()
        
        # Status tab
        self.status_display = TextDisplay(20, 100, SCREEN_WIDTH - 40, 650)
        self.refresh_status()
        
        # Now Playing tab
        self.now_playing_label = ""
        self.now_play_btns = [
            Button(SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT - 100, 140, 40, "Play/Pause"),
            Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 100, 140, 40, "Stop"),
            Button(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100, 140, 40, "Next"),
            Button(SCREEN_WIDTH//2 + 150, SCREEN_HEIGHT - 100, 140, 40, "Prev")
        ]
        self.volume_slider = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 80, 150, 20)
        self.volume = 1.0
        self.update_now_playing()
        
        self.running = True
    
    def initialize_music_library(self):
        try:
            self.music_manager = MusicPlaylistManager(self.music_dir)
            song_library = self.music_manager.get_song_library()
            if not song_library:
                return False
            for song in song_library:
                try:
                    sound = pygame.mixer.Sound(song['file_path'])
                    song['duration'] = sound.get_length() * 1000
                except:
                    song['duration'] = 0
            self.playlist_manager = PlaylistManager()
            self.stacks_queues_player = MusicPlayerStacksQueues(self.music_manager)
            self.load_playlists()
            return True
        except Exception as e:
            print(f"Error initializing music library: {e}")
            return False
    
    def load_playlists(self):
        try:
            if os.path.exists('playlists.json'):
                with open('playlists.json', 'r') as f:
                    data = json.load(f)
                for name, playlist_data in data.items():
                    songs = playlist_data.get('songs', [])
                    desc = playlist_data.get('description', '')
                    self.playlist_manager.create_playlist(name)
                    self.playlist_descriptions[name] = desc
                    pl = self.playlist_manager.get_current_playlist()
                    for song_data in songs:
                        # Verify song exists in library
                        if any(song['file_path'] == song_data['file_path'] for song in self.music_manager.get_song_library()):
                            pl.add_song_at_end(song_data)
                    self.playlist_manager.switch_playlist(None)  # Reset current playlist
                if data:
                    self.playlist_manager.switch_playlist(list(data.keys())[0])
        except Exception as e:
            print(f"Error loading playlists: {e}")
    
    def save_playlists(self):
        try:
            data = {}
            for name, pl in self.playlist_manager.playlists.items():
                songs = []
                curr = pl.head
                while curr:
                    songs.append(curr.song_data)
                    curr = curr.next
                data[name] = {
                    'description': self.playlist_descriptions.get(name, ''),
                    'songs': songs
                }
            with open('playlists.json', 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving playlists: {e}")
    
    def show_modal_text(self, prompt, on_confirm, default="", has_desc=False, numeric=False):
        modal_rect = Rect(SCREEN_WIDTH//4, SCREEN_HEIGHT//4, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        input_y = modal_rect.y + 100
        self.modal = {
            'rect': modal_rect,
            'type': 'text',
            'prompt': prompt,
            'numeric': numeric,
            'name_input': TextInput(modal_rect.x + 50, input_y, modal_rect.width - 100, 40),
            'desc_input': TextInput(modal_rect.x + 50, input_y + 60, modal_rect.width - 100, 40) if has_desc else None,
            'confirm': Button(modal_rect.x + 50, modal_rect.bottom - 60, 140, 40, "Confirm"),
            'cancel': Button(modal_rect.x + modal_rect.width - 190, modal_rect.bottom - 60, 140, 40, "Cancel"),
            'on_confirm': on_confirm
        }
        self.modal['name_input'].text = default
    
    def show_modal_song_select(self, on_select, title="Select Song"):
        modal_rect = Rect(SCREEN_WIDTH//4, SCREEN_HEIGHT//4, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        song_list = ScrollableList(modal_rect.x + 20, modal_rect.y + 60, modal_rect.width - 40, modal_rect.height - 120)
        song_list.set_items(self.music_manager.get_song_library())
        self.modal = {
            'rect': modal_rect,
            'type': 'song_select',
            'title': title,
            'list': song_list,
            'cancel': Button(modal_rect.x + modal_rect.width//2 - 70, modal_rect.bottom - 60, 140, 40, "Cancel"),
            'on_select': on_select
        }
    
    def show_modal_confirm(self, prompt, on_yes):
        modal_rect = Rect(SCREEN_WIDTH//4, SCREEN_HEIGHT//4, SCREEN_WIDTH//2, SCREEN_HEIGHT//4)
        self.modal = {
            'rect': modal_rect,
            'type': 'confirm',
            'prompt': prompt,
            'yes': Button(modal_rect.x + 50, modal_rect.bottom - 60, 140, 40, "Yes", GREEN),
            'no': Button(modal_rect.x + modal_rect.width - 190, modal_rect.bottom - 60, 140, 40, "No", RED),
            'on_yes': on_yes
        }
    
    def handle_modal(self, event, pos):
        if not self.modal:
            return False
        modal_type = self.modal.get('type')
        if not modal_type:
            self.modal = None
            return False
        if modal_type == 'text':
            self.modal['name_input'].handle_event(event)
            if 'desc_input' in self.modal and self.modal['desc_input']:
                self.modal['desc_input'].handle_event(event)
            if self.modal['confirm'].handle_event(event, pos):
                if self.modal['numeric'] and not self.modal['name_input'].text.isdigit():
                    self.show_message("Please enter a valid number")
                    return True
                desc = self.modal['desc_input'].text if 'desc_input' in self.modal and self.modal['desc_input'] else ""
                self.modal['on_confirm'](self.modal['name_input'].text, desc)
                self.modal = None
                return True
            if self.modal['cancel'].handle_event(event, pos):
                self.modal = None
                return True
        elif modal_type == 'song_select':
            if event.type == MOUSEBUTTONDOWN:
                selected = self.modal['list'].handle_click(pos)
                if selected:
                    self.modal['on_select'](selected)
                    self.modal = None
                    return True
            elif event.type == MOUSEWHEEL:
                self.modal['list'].handle_scroll(event.y)
            if self.modal['cancel'].handle_event(event, pos):
                self.modal = None
                return True
        elif modal_type == 'confirm':
            if self.modal['yes'].handle_event(event, pos):
                self.modal['on_yes']()
                self.modal = None
                return True
            if self.modal['no'].handle_event(event, pos):
                self.modal = None
                return True
        return True
    
    def draw_modal(self):
        pygame.draw.rect(self.screen, GRAY, self.modal['rect'], border_radius=10)
        pygame.draw.rect(self.screen, WHITE, self.modal['rect'], width=2, border_radius=10)
        prompt_surf = self.small_font.render(self.modal['prompt'] if 'prompt' in self.modal else self.modal['title'], True, WHITE)
        self.screen.blit(prompt_surf, (self.modal['rect'].x + 20, self.modal['rect'].y + 20))
        if self.modal['type'] == 'text':
            self.modal['name_input'].draw(self.screen)
            if 'desc_input' in self.modal and self.modal['desc_input']:
                desc_label = self.small_font.render("Description:", True, WHITE)
                self.screen.blit(desc_label, (self.modal['rect'].x + 50, self.modal['desc_input'].rect.y - 25))
                self.modal['desc_input'].draw(self.screen)
            name_label = self.small_font.render("Name:", True, WHITE)
            self.screen.blit(name_label, (self.modal['rect'].x + 50, self.modal['name_input'].rect.y - 25))
            self.modal['confirm'].draw(self.screen)
            self.modal['cancel'].draw(self.screen)
        elif self.modal['type'] == 'song_select':
            self.modal['list'].draw(self.screen)
            self.modal['cancel'].draw(self.screen)
        elif self.modal['type'] == 'confirm':
            self.modal['yes'].draw(self.screen)
            self.modal['no'].draw(self.screen)
    
    def refresh_library(self):
        if self.library_view == 'all':
            self.library_list.set_items(self.music_manager.get_song_library())
        elif self.library_view == 'artists':
            if self.selected_artist:
                songs = self.music_manager.filter_songs_by_artist(self.selected_artist)
                self.library_list.set_items(songs)
            else:
                artists = self.music_manager.get_artists_list()
                self.library_list.set_items(artists)
        elif self.library_view == 'file_types':
            if self.selected_file_type:
                songs = self.music_manager.filter_songs_by_file_type(self.selected_file_type)
                self.library_list.set_items(songs)
            else:
                types = self.music_manager.get_file_types_list()
                self.library_list.set_items(types)
        elif self.library_view == 'stats':
            stats = self.music_manager.get_library_statistics()
            text = f"Total Songs: {stats['total_songs']}\nTotal Size: {stats['total_size_gb']:.2f} GB\nUnique Artists: {stats['unique_artists']}\n\nTop Artists:\n"
            for artist, count in list(stats['artist_counts'].items())[:10]:
                text += f"{artist}: {count}\n"
            text += "\nFile Types:\n"
            for ft, count in stats['file_type_counts'].items():
                text += f"{ft}: {count}\n"
            self.library_list.set_items(text.split('\n'))
        self.library_back_btn.text = "Back" if self.selected_artist or self.selected_file_type else ""
    
    def refresh_playlists(self):
        pl_names = list(self.playlist_manager.playlists.keys())
        self.playlists_list.set_items(pl_names)
        current_pl = self.playlist_manager.get_current_playlist()
        if current_pl:
            songs = []
            curr = current_pl.head
            while curr:
                songs.append(curr.song_data)
                curr = curr.next
            self.playlist_songs_list.set_items(songs)
    
    def refresh_queues(self):
        next_queue = [song for song in self.stacks_queues_player.play_next_queue.queue]
        self.play_next_list.set_items(next_queue)
        party_queue = [song for song, _ in self.stacks_queues_player.party_queue.queue]
        self.party_list.set_items(party_queue)
    
    def refresh_history(self, query=None):
        history = self.stacks_queues_player.listening_history.stack
        if query:
            history = self.stacks_queues_player.listening_history.search_history(query)
        self.history_display.set_items(history[::-1])  # Recent first
    
    def refresh_status(self):
        text = "=" * 80 + "\n📊 COMPLETE MUSIC PLAYER STATUS\n" + "=" * 80 + "\n"
        song_library = self.music_manager.get_song_library()
        text += f"📚 Music Library: {len(song_library)} songs\n"
        
        total_playlists = len(self.playlist_manager.playlists)
        current_playlist_name = self.playlist_manager.current_playlist_name
        text += f"📋 Playlist Manager: {total_playlists} playlists\n"
        if current_playlist_name:
            current_playlist = self.playlist_manager.get_current_playlist()
            if current_playlist:
                text += f"   Active: {current_playlist_name} ({current_playlist.get_size()} songs)\n"
                if not current_playlist.is_empty():
                    current_song = current_playlist.get_current_song()
                    if current_song:
                        text += f"   Current: {current_song['title']} - {current_song['artist']}\n"
                desc = self.playlist_descriptions.get(current_playlist_name, '')
                if desc:
                    text += f"   Description: {desc}\n"
        
        text += f"➡️  Play Next Queue: {self.stacks_queues_player.play_next_queue.get_size()} songs\n"
        text += f"🎉 Party Queue: {self.stacks_queues_player.party_queue.get_size()} songs\n"
        text += f"📜 Listening History: {self.stacks_queues_player.listening_history.get_size()} songs\n"
        
        if self.stacks_queues_player.currently_playing:
            current = self.stacks_queues_player.currently_playing
            text += f"🎵 Currently Playing: {current['title']} - {current['artist']}\n"
        
        text += "=" * 80
        self.status_display.set_text(text)
    
    def update_now_playing(self):
        if self.stacks_queues_player.currently_playing:
            song = self.stacks_queues_player.currently_playing
            self.now_playing_label = f"🎵 {song['title']} - {song['artist']}"
            self.now_play_btns[0].text = "Pause" if pygame.mixer.music.get_busy() else "Play"
            self.current_duration = song.get('duration', 0)
        else:
            self.now_playing_label = "No song playing"
            self.current_duration = 0
    
    def show_message(self, msg, duration=180):
        self.message = msg
        self.message_timer = duration
    
    def handle_events(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MUSIC_END:
                if self.playing_playlist:
                    self.playing_playlist.next_song()
                    song = self.playing_playlist.get_current_song()
                    if song:
                        self.stacks_queues_player.play_song(song)
                    else:
                        self.playing_playlist = None
                    self.update_now_playing()
                    self.refresh_history()
            elif event.type == MOUSEWHEEL:
                if self.modal and self.modal.get('type') == 'song_select':
                    self.modal['list'].handle_scroll(event.y)
                    continue
                elif self.current_tab == "library":
                    self.library_list.handle_scroll(event.y)
                elif self.current_tab == "playlists":
                    if self.playlists_list.rect.collidepoint(pos):
                        self.playlists_list.handle_scroll(event.y)
                    elif self.playlist_songs_list.rect.collidepoint(pos):
                        self.playlist_songs_list.handle_scroll(event.y)
                elif self.current_tab == "queues":
                    if self.play_next_list.rect.collidepoint(pos):
                        self.play_next_list.handle_scroll(event.y)
                    elif self.party_list.rect.collidepoint(pos):
                        self.party_list.handle_scroll(event.y)
                elif self.current_tab == "history":
                    self.history_display.handle_scroll(event.y)
                elif self.current_tab == "status":
                    self.status_display.handle_scroll(event.y)
            if self.modal and self.handle_modal(event, pos):
                continue
            # Tab buttons
            for i, btn in enumerate(self.tab_buttons):
                if btn.handle_event(event, pos):
                    self.current_tab = self.tabs[i].lower().replace(" ", "_")
                    if self.current_tab == "status":
                        self.refresh_status()
                    break
            if self.current_tab == "library":
                self.handle_library(event, pos)
            elif self.current_tab == "playlists":
                self.handle_playlists(event, pos)
            elif self.current_tab == "queues":
                self.handle_queues(event, pos)
            elif self.current_tab == "history":
                self.handle_history(event, pos)
            elif self.current_tab == "status":
                pass
            elif self.current_tab == "now_playing":
                self.handle_now_playing(event, pos)
    
    def handle_library(self, event, pos):
        if self.library_all_btn.handle_event(event, pos):
            self.library_view = 'all'
            self.selected_artist = None
            self.selected_file_type = None
            self.refresh_library()
        elif self.library_artist_btn.handle_event(event, pos):
            self.library_view = 'artists'
            self.selected_artist = None
            self.refresh_library()
        elif self.library_type_btn.handle_event(event, pos):
            self.library_view = 'file_types'
            self.selected_file_type = None
            self.refresh_library()
        elif self.library_stats_btn.handle_event(event, pos):
            self.library_view = 'stats'
            self.refresh_library()
        elif self.library_back_btn.handle_event(event, pos) and (self.selected_artist or self.selected_file_type):
            self.selected_artist = None
            self.selected_file_type = None
            self.refresh_library()
        elif self.library_search_btn.handle_event(event, pos):
            query = self.library_search_input.text
            if query:
                results = self.music_manager.search_songs(query)
                self.library_list.set_items(results)
        self.library_search_input.handle_event(event)
        if event.type == MOUSEBUTTONDOWN:
            selected = self.library_list.handle_click(pos)
            if selected:
                if self.library_view == 'artists' and not self.selected_artist:
                    self.selected_artist = selected
                    self.refresh_library()
                elif self.library_view == 'file_types' and not self.selected_file_type:
                    self.selected_file_type = selected
                    self.refresh_library()
                elif isinstance(selected, dict):
                    self.stacks_queues_player.play_song(selected)
                    self.playing_playlist = None
                    self.update_now_playing()
                    self.show_message(f"Playing: {selected['title']}")
                    self.refresh_history()
    
    def handle_playlists(self, event, pos):
        if event.type == MOUSEBUTTONDOWN:
            pl_selected = self.playlists_list.handle_click(pos)
            if pl_selected:
                self.playlist_manager.switch_playlist(pl_selected)
                self.refresh_playlists()
                self.show_message(f"🔄 Switched to playlist: '{pl_selected}'")
            song_selected = self.playlist_songs_list.handle_click(pos)
            if song_selected:
                current_pl = self.playlist_manager.get_current_playlist()
                if current_pl:
                    curr = current_pl.head
                    for _ in range(self.playlist_songs_list.selected_index):
                        curr = curr.next
                    current_pl.current_node = curr
                    self.stacks_queues_player.play_song(song_selected)
                    self.playing_playlist = current_pl
                    self.update_now_playing()
                    self.show_message(f"Playing: {song_selected['title']}")
                    self.refresh_history()
        btns = self.playlist_buttons
        if btns[0].handle_event(event, pos):  # List All
            self.refresh_playlists()
        elif btns[1].handle_event(event, pos):  # Create New
            self.show_modal_text("Enter playlist name", lambda name, desc: (self.playlist_manager.create_playlist(name) or self.playlist_descriptions.update({name: desc}) or self.refresh_playlists() or self.save_playlists() or self.show_message(f"✅ Created new playlist: '{name}'")), has_desc=True)
        elif btns[2].handle_event(event, pos):  # Create from Lib
            self.show_modal_text("Enter playlist name", lambda name, desc: self.show_modal_text("Enter max songs", lambda max_s, _: (self.playlist_manager.create_playlist_from_library(name, self.music_manager, int(max_s or 10)) or self.playlist_descriptions.update({name: desc}) or self.refresh_playlists() or self.save_playlists() or self.show_message(f"✅ Created playlist from library: '{name}'")), has_desc=True, numeric=True))
        elif btns[3].handle_event(event, pos):  # Switch
            selected = self.playlists_list.selected_index
            if selected >= 0:
                name = self.playlists_list.items[selected]
                self.playlist_manager.switch_playlist(name)
                self.refresh_playlists()
                self.show_message(f"🔄 Switched to playlist: '{name}'")
        elif btns[4].handle_event(event, pos):  # Delete
            selected = self.playlists_list.selected_index
            if selected >= 0:
                name = self.playlists_list.items[selected]
                self.show_modal_confirm(f"Delete '{name}'?", lambda: (self.playlist_manager.delete_playlist(name) or self.playlist_descriptions.pop(name, None) or self.refresh_playlists() or self.save_playlists() or self.show_message(f"🗑️ Deleted playlist: '{name}'")))
        elif btns[5].handle_event(event, pos):  # Add Song
            self.show_modal_song_select(lambda song: (self.playlist_manager.add_song_to_current_playlist(song) or self.refresh_playlists() or self.save_playlists() or self.show_message(f"✅ Added song: {song['title']}")))
        elif btns[6].handle_event(event, pos):  # Insert After
            current_pl = self.playlist_manager.get_current_playlist()
            if current_pl and current_pl.get_current_song():
                target = current_pl.get_current_song()['title']
                self.show_modal_song_select(lambda song: (current_pl.insert_song_after(target, song) or self.refresh_playlists() or self.save_playlists() or self.show_message(f"✅ Inserted song: {song['title']} after {target}")), "Select song to insert after current")
            else:
                self.show_message("No current song")
        elif btns[7].handle_event(event, pos):  # Remove Song
            selected = self.playlist_songs_list.selected_index
            if selected >= 0:
                title = self.playlist_songs_list.items[selected]['title']
                current_pl = self.playlist_manager.get_current_playlist()
                if current_pl:
                    current_pl.remove_song(title)
                    self.refresh_playlists()
                    self.save_playlists()
                    self.show_message(f"🗑️ Removed song: {title}")
        elif btns[8].handle_event(event, pos):  # Search Song
            self.show_modal_text("Enter search term", lambda query, _: self.playlist_songs_list.set_items(current_pl.search_song(query) or []) if (current_pl := self.playlist_manager.get_current_playlist()) else self.show_message("No playlist"))
        elif btns[9].handle_event(event, pos):  # Shuffle
            current_pl = self.playlist_manager.get_current_playlist()
            if current_pl:
                current_pl.shuffle_playlist()
                self.refresh_playlists()
                self.save_playlists()
                self.show_message("🔀 Shuffled playlist")
        elif btns[10].handle_event(event, pos):  # Play Playlist
            current_pl = self.playlist_manager.get_current_playlist()
            if current_pl:
                if not current_pl.get_current_song():
                    current_pl.go_to_first_song()
                song = current_pl.get_current_song()
                if song:
                    self.stacks_queues_player.play_song(song)
                    self.playing_playlist = current_pl
                    self.update_now_playing()
                    self.refresh_history()
                    self.show_message(f"Playing: {song['title']}")
        elif btns[11].handle_event(event, pos):  # Display
            self.refresh_playlists()
        elif btns[12].handle_event(event, pos):  # First Song
            current_pl = self.playlist_manager.get_current_playlist()
            if current_pl:
                current_pl.go_to_first_song()
                self.refresh_playlists()
        elif btns[13].handle_event(event, pos):  # Last Song
            current_pl = self.playlist_manager.get_current_playlist()
            if current_pl:
                current_pl.go_to_last_song()
                self.refresh_playlists()
        elif btns[14].handle_event(event, pos):  # Next Song
            current_pl = self.playlist_manager.get_current_playlist()
            if current_pl:
                current_pl.next_song()
                self.refresh_playlists()
        elif btns[15].handle_event(event, pos):  # Prev Song
            current_pl = self.playlist_manager.get_current_playlist()
            if current_pl:
                current_pl.previous_song()
                self.refresh_playlists()
    
    def handle_queues(self, event, pos):
        if event.type == MOUSEBUTTONDOWN:
            self.play_next_list.handle_click(pos)
            self.party_list.handle_click(pos)
        btns = self.queues_buttons
        if btns[0].handle_event(event, pos):  # Add to Next
            self.show_modal_song_select(lambda song: (self.stacks_queues_player.add_to_play_next(song) or self.refresh_queues() or self.show_message(f"✅ Added to Play Next: {song['title']}")))
        elif btns[1].handle_event(event, pos):  # Play Next
            self.stacks_queues_player.play_next_song()
            self.refresh_queues()
            self.update_now_playing()
            self.refresh_history()
        elif btns[2].handle_event(event, pos):  # Clear Next
            self.stacks_queues_player.play_next_queue.clear_queue()
            self.refresh_queues()
            self.show_message("🗑️ Cleared Play Next queue")
        elif btns[3].handle_event(event, pos):  # Add to Party
            self.show_modal_song_select(lambda song: self.show_modal_text("Enter priority", lambda pri, _: (self.stacks_queues_player.add_to_party_queue(song, int(pri or 0)) or self.refresh_queues() or self.show_message(f"✅ Added to Party Queue: {song['title']}")), numeric=True))
        elif btns[4].handle_event(event, pos):  # Upvote
            selected = self.party_list.selected_index
            if selected >= 0:
                title = self.stacks_queues_player.party_queue.queue[selected][0]['title']
                self.stacks_queues_player.upvote_song_in_party_queue(title)
                self.refresh_queues()
                self.show_message(f"⬆️ Upvoted: {title}")
        elif btns[5].handle_event(event, pos):  # Play Party
            self.stacks_queues_player.play_from_party_queue()
            self.refresh_queues()
            self.update_now_playing()
            self.refresh_history()
        elif btns[6].handle_event(event, pos):  # Clear Party
            self.stacks_queues_player.party_queue.clear_queue()
            self.refresh_queues()
            self.show_message("🗑️ Cleared Party Queue")
        elif btns[7].handle_event(event, pos):  # View History
            self.refresh_history()
        elif btns[8].handle_event(event, pos):  # Search History
            self.show_modal_text("Enter search term", lambda query, _: self.refresh_history(query))
    
    def handle_history(self, event, pos):
        if self.history_search_btn.handle_event(event, pos):
            query = self.history_search_input.text
            self.refresh_history(query)
        self.history_search_input.handle_event(event)
    
    def handle_now_playing(self, event, pos):
        btns = self.now_play_btns
        if btns[0].handle_event(event, pos):  # Play/Pause
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            self.update_now_playing()
        elif btns[1].handle_event(event, pos):  # Stop
            self.stacks_queues_player.stop_song()
            self.playing_playlist = None
            self.update_now_playing()
        elif btns[2].handle_event(event, pos):  # Next
            if self.playing_playlist:
                self.playing_playlist.next_song()
                song = self.playing_playlist.get_current_song()
                if song:
                    self.stacks_queues_player.play_song(song)
                    self.update_now_playing()
                    self.refresh_history()
                    self.show_message(f"Playing: {song['title']}")
            else:
                self.stacks_queues_player.play_next_song()
                self.update_now_playing()
                self.refresh_history()
        elif btns[3].handle_event(event, pos):  # Prev
            if self.playing_playlist:
                self.playing_playlist.previous_song()
                song = self.playing_playlist.get_current_song()
                if song:
                    self.stacks_queues_player.play_song(song)
                    self.update_now_playing()
                    self.refresh_history()
                    self.show_message(f"Playing: {song['title']}")
        if event.type == MOUSEBUTTONDOWN and self.volume_slider.collidepoint(pos):
            rel_x = (pos[0] - self.volume_slider.x) / self.volume_slider.width
            self.volume = max(0, min(1, rel_x))
            pygame.mixer.music.set_volume(self.volume)
        if event.type == MOUSEBUTTONDOWN and self.progress_rect.collidepoint(pos):
            rel_x = (pos[0] - self.progress_rect.x) / self.progress_rect.width
            new_pos = rel_x * (self.current_duration / 1000)
            pygame.mixer.music.set_pos(new_pos)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Title
        title_surf = self.title_font.render("🎵 Music Streamer", True, BLUE)
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 20))
        
        # Tabs
        for btn in self.tab_buttons:
            if btn.text.lower().replace(" ", "_") == self.current_tab:
                btn.color = GREEN
            else:
                btn.color = GRAY
            btn.draw(self.screen)
        
        if self.current_tab == "library":
            self.library_all_btn.draw(self.screen)
            self.library_artist_btn.draw(self.screen)
            self.library_type_btn.draw(self.screen)
            self.library_stats_btn.draw(self.screen)
            if self.library_back_btn.text:
                self.library_back_btn.draw(self.screen)
            self.library_search_input.draw(self.screen)
            self.library_search_btn.draw(self.screen)
            self.library_list.draw(self.screen)
        elif self.current_tab == "playlists":
            self.playlists_list.draw(self.screen)
            self.playlist_songs_list.draw(self.screen)
            for btn in self.playlist_buttons:
                btn.draw(self.screen)
        elif self.current_tab == "queues":
            self.play_next_list.draw(self.screen)
            self.party_list.draw(self.screen)
            for btn in self.queues_buttons:
                btn.draw(self.screen)
            next_label = self.font.render("Play Next Queue", True, WHITE)
            self.screen.blit(next_label, (20, 60))
            party_label = self.font.render("Party Queue", True, WHITE)
            self.screen.blit(party_label, (640, 60))
        elif self.current_tab == "history":
            self.history_display.draw(self.screen)
            self.history_search_input.draw(self.screen)
            self.history_search_btn.draw(self.screen)
        elif self.current_tab == "status":
            self.status_display.draw(self.screen)
        elif self.current_tab == "now_playing":
            label_surf = self.font.render(self.now_playing_label, True, WHITE)
            self.screen.blit(label_surf, (SCREEN_WIDTH//2 - label_surf.get_width()//2, SCREEN_HEIGHT//2 - 50))
            for btn in self.now_play_btns:
                btn.draw(self.screen)
            # Volume slider
            pygame.draw.rect(self.screen, GRAY, self.volume_slider, border_radius=5)
            fill_width = self.volume * self.volume_slider.width
            pygame.draw.rect(self.screen, BLUE, (self.volume_slider.x, self.volume_slider.y, fill_width, self.volume_slider.height), border_radius=5)
            vol_label = self.small_font.render("Volume", True, WHITE)
            self.screen.blit(vol_label, (self.volume_slider.x, self.volume_slider.y - 25))
            # Progress bar
            if self.current_duration > 0:
                pos = pygame.mixer.music.get_pos()
                fill_width = (pos / self.current_duration) * self.progress_rect.width
                pygame.draw.rect(self.screen, GRAY, self.progress_rect, border_radius=5)
                pygame.draw.rect(self.screen, GREEN, (self.progress_rect.x, self.progress_rect.y, fill_width, self.progress_rect.height), border_radius=5)
                # Display time
                current_time = int(pos / 1000)  # Convert to seconds
                total_time = int(self.current_duration / 1000)  # Convert to seconds
                time_label = f"{current_time//60}:{current_time%60:02} / {total_time//60}:{total_time%60:02}"
                time_surf = self.small_font.render(time_label, True, WHITE)
                self.screen.blit(time_surf, (self.progress_rect.x, self.progress_rect.y - 25))
        
        if self.message_timer > 0:
            msg_surf = self.small_font.render(self.message, True, YELLOW)
            self.screen.blit(msg_surf, (20, SCREEN_HEIGHT - 30))
            self.message_timer -= 1
        
        if self.modal:
            # Dim background
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            self.draw_modal()
        
        pygame.display.flip()
    
    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.draw()
                self.clock.tick(FPS)
        except KeyboardInterrupt:
            print("Music player interrupted. Goodbye!")
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.save_playlists()  # Save playlists before exiting
            pygame.quit()

if __name__ == "__main__":
    player = GUIMusicPlayer()
    player.run()