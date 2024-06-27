import os
import sys
import pygame
import typing
import time
import tkinter
import win32gui
import screeninfo
import math
from pynput import mouse
from pynput import keyboard as pynputkeyboard
import pygetwindow as gw

from pathlib import Path

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(os.path.abspath(os.path.dirname(sys.executable)))
    elif __file__:
        return Path(os.path.abspath(os.path.dirname(__file__))).resolve()
    
BASE_DIR: Path = get_base_dir()

class App():
    def __init__(self) -> None:
        self.path = {
            'songs': BASE_DIR / 'songs'
            }
        
        try:
            self.roblox_window = gw.getWindowsWithTitle("Roblox")[0]
        except IndexError:
            print("Open Roblox first and then open this program.")
            print('>>> ')
            exit()

        self.current_display = None

        for m in screeninfo.get_monitors():
            if m.is_primary:
                self.current_display = m
                break
            
        self.roblox_resolution = (self.roblox_window.width, self.roblox_window.height)

        window_handle = win32gui.FindWindow(None, "Roblox")
        window_rect = win32gui.GetWindowRect(window_handle)
        client_rect = list(win32gui.GetClientRect(window_handle))
        
        self.roblox_resolution = (client_rect[2], client_rect[3])
        self.roblox_offset_x, self.roblox_offset_y = window_rect[0], window_rect[1]
        # pyperclip.copy(f'((self.roblox_resolution[0] / {self.roblox_resolution[0] / 1209}, self.roblox_resolution[1] / {self.roblox_resolution[1] / 512}), (self.roblox_resolution[0] / {self.roblox_resolution[0] / 1253}, self.roblox_resolution[1] / {self.roblox_resolution[1] / 563}))')

        if not os.path.exists(BASE_DIR / "songs"):
            os.mkdir(BASE_DIR / "songs")

        if math.floor(self.roblox_resolution[0] / self.roblox_resolution[1] * 100) / 100.0 == math.floor(16 / 9 * 100) / 100.0:
            screen_mode = '16:9'
        elif math.floor(self.roblox_resolution[0] / self.roblox_resolution[1] * 100) / 100.0 == math.floor(5 / 4 * 100) / 100.0:
            screen_mode = '5:4'
        elif math.floor(self.roblox_resolution[0] / self.roblox_resolution[1] * 100) / 100.0 == math.floor(4 / 3 * 100) / 100.0:
            screen_mode = '4:3'
        else:
            print('Unknown screen type found. This program may not work as expected. Switching to 16:9 mode...')
            screen_mode = '16:9'
            time.sleep(1.5)
        
        self.screen_data = {
            '16:9': {'pos': {
                'play_button': ((self.roblox_resolution[0] / 6.530612244897959,
                                 self.roblox_resolution[1] / 1.487603305785124),
                                (self.roblox_resolution[0] / 2.9024943310657596,
                                 self.roblox_resolution[1] / 1.1783960720130933)),
                
                'play_button_unpublished': ((self.roblox_resolution[0] / 1.951219512195122,
                                             self.roblox_resolution[1] / 1.4090019569471623),
                                            (self.roblox_resolution[0] / 1.5292712066905616,
                                             self.roblox_resolution[1] / 1.306715063520871)),
                
                'play_button_editor': ((self.roblox_resolution[0] / 1.0569777043765483,
                                        self.roblox_resolution[1] / 2.376237623762376),
                                       (self.roblox_resolution[0] / 1.019108280254777,
                                        self.roblox_resolution[1] / 2.039660056657224)),
                
                'play_music_button_editor': ((self.roblox_resolution[0] / 1.0569777043765483,
                                              self.roblox_resolution[1] / 2.0),
                                             (self.roblox_resolution[0] / 1.019108280254777,
                                              self.roblox_resolution[1] / 1.7183770883054892)),
                
                'stop_music_button_editor': ((self.roblox_resolution[0] / 1.124780316344464,
                                              self.roblox_resolution[1] / 2.0168067226890756),
                                             (self.roblox_resolution[0] / 1.0810810810810811,
                                              self.roblox_resolution[1] / 1.7307692307692308)),
                
                'restart_button': ((self.roblox_resolution[0] / 1.4222222222222223,
                                    self.roblox_resolution[1] / 1.509433962264151),
                                   (self.roblox_resolution[0] / 1.3291796469366564,
                                    self.roblox_resolution[1] / 1.338289962825279)),
                
                'close_button': ((self.roblox_resolution[0] / 1.610062893081761,
                                  self.roblox_resolution[1] / 2.4161073825503356),
                                 (self.roblox_resolution[0] / 1.4065934065934067,
                                  self.roblox_resolution[1] / 1.7349397590361446)),
                
                'pause_button': ((self.roblox_resolution[0] / 1.0774410774410774,
                                  self.roblox_resolution[1] / 15.319148936170214),
                                 (self.roblox_resolution[0] / 1.019108280254777,
                                  self.roblox_resolution[1] / 6.260869565217392)),
                
                'resume_button': ((self.roblox_resolution[0] / 2.237762237762238,
                                   self.roblox_resolution[1] / 2.5),
                                  (self.roblox_resolution[0] / 1.8104667609618104,
                                   self.roblox_resolution[1] / 1.6941176470588235))
            }},
            '5:4': {'pos': {
                'play_button': ((self.roblox_resolution[0] / 9.257142857142858,
                                self.roblox_resolution[1] / 1.5303030303030303),
                                (self.roblox_resolution[0] / 3.24,
                                 self.roblox_resolution[1] / 1.286624203821656)),
                
                'play_button_unpublished': ((self.roblox_resolution[0] / 1.9696048632218845,
                                             self.roblox_resolution[1] / 1.3741496598639455),
                                            (self.roblox_resolution[0] / 1.5558223289315727,
                                             self.roblox_resolution[1] / 1.2849872773536897)),
                
                'play_button_editor': ((self.roblox_resolution[0] / 1.0719602977667493,
                                        self.roblox_resolution[1] / 2.234513274336283),
                                       (self.roblox_resolution[0] / 1.034317637669593,
                                        self.roblox_resolution[1] / 2.0079522862823063)),
                
                'play_music_button_editor': ((self.roblox_resolution[0] / 1.0719602977667493,
                                              self.roblox_resolution[1] / 1.97265625),
                                             (self.roblox_resolution[0] / 1.034317637669593,
                                              self.roblox_resolution[1] / 1.7939609236234457)),

                'stop_music_button_editor': ((self.roblox_resolution[0] / 1.1592128801431127,
                                              self.roblox_resolution[1] / 2.0159680638722555),
                                             (self.roblox_resolution[0] / 1.0881612090680102,
                                              self.roblox_resolution[1] / 1.7474048442906573)),
                
                'restart_button': ((self.roblox_resolution[0] / 1.481142857142857,
                                    self.roblox_resolution[1] / 1.4962962962962962),
                                   (self.roblox_resolution[0] / 1.3224489795918368,
                                    self.roblox_resolution[1] / 1.303225806451613)),

                'close_button': ((self.roblox_resolution[0] / 1.683116883116883,
                                  self.roblox_resolution[1] / 2.3488372093023258),
                                 (self.roblox_resolution[0] / 1.3935483870967742,
                                  self.roblox_resolution[1] / 1.7413793103448276)),
                
                'pause_button': ((self.roblox_resolution[0] / 1.1124463519313306,
                                  self.roblox_resolution[1] / 28.857142857142858),
                                 (self.roblox_resolution[0] / 1.016470588235294,
                                  self.roblox_resolution[1] / 6.733333333333333)),
                
                'resume_button': ((self.roblox_resolution[0] / 2.4,
                                   self.roblox_resolution[1] / 2.4634146341463414),
                                  (self.roblox_resolution[0] / 1.7753424657534247,
                                   self.roblox_resolution[1] / 1.6833333333333333))
            }},
            '4:3': {'pos': {
                'play_button': ((self.roblox_resolution[0] / 9.014084507042254,
                                self.roblox_resolution[1] / 1.5311004784688995),
                                (self.roblox_resolution[0] / 3.18407960199005,
                                 self.roblox_resolution[1] / 1.2581913499344692655)),
                
                'play_button_unpublished': ((self.roblox_resolution[0] / 1.9541984732824427,
                                             self.roblox_resolution[1] / 1.3953488372093024),
                                            (self.roblox_resolution[0] / 1.5292712066905616,
                                             self.roblox_resolution[1] / 1.2990527740189446)),
                
                'play_button_editor': ((self.roblox_resolution[0] / 1.0587262200165426,
                                        self.roblox_resolution[1] / 2.302158273381295),
                                       (self.roblox_resolution[0] / 1.0207336523125996,
                                        self.roblox_resolution[1] / 2.0168067226890756)),
                
                'play_music_button_editor': ((self.roblox_resolution[0] / 1.0587262200165426,
                                              self.roblox_resolution[1] / 2.00836820083682),
                                             (self.roblox_resolution[0] / 1.0207336523125996,
                                              self.roblox_resolution[1] / 1.7744916820702403)),

                'stop_music_button_editor': ((self.roblox_resolution[0] / 1.1297440423654015,
                                              self.roblox_resolution[1] / 2.0125786163522013),
                                             (self.roblox_resolution[0] / 1.0865874363327674,
                                              self.roblox_resolution[1] / 1.7777777777777777)),
                
                'restart_button': ((self.roblox_resolution[0] / 1.4269788182831662,
                                    self.roblox_resolution[1] / 1.4837712519319939),
                                   (self.roblox_resolution[0] / 1.3250517598343685,
                                    self.roblox_resolution[1] / 1.3407821229050279)),

                'close_button': ((self.roblox_resolution[0] / 1.6558861578266495,
                                  self.roblox_resolution[1] / 2.4242424242424243),
                                 (self.roblox_resolution[0] / 1.3719185423365488,
                                  self.roblox_resolution[1] / 1.7266187050359711)),
                
                'pause_button': ((self.roblox_resolution[0] / 1.0774410774410774,
                                  self.roblox_resolution[1] / 18.46153846153846),
                                 (self.roblox_resolution[0] / 1.0182975338106603,
                                  self.roblox_resolution[1] / 7.933884297520661)),
                
                'resume_button': ((self.roblox_resolution[0] / 2.335766423357664,
                                   self.roblox_resolution[1] / 2.4935064935064934),
                                  (self.roblox_resolution[0] / 1.7510259917920656,
                                   self.roblox_resolution[1] / 1.6901408450704225))
            }}
        }
        
        self.target_song_id: int | None = None
        self.is_song_playing: bool = False
        self.is_song_paused: bool = False
        self.is_game_paused: bool = False
        self.mode = 'normal'
        self.screen_mode = screen_mode
        
        pygame.mixer.init()

        self.root = tkinter.Tk()
        self.root.withdraw()

        self.mouse = mouse.Controller()
        self.keyboard = pynputkeyboard.Controller()
    
    def play_song(self):
        self.is_song_playing: bool = True
        self.is_game_paused: bool = False
        self.is_song_paused: bool = False
        pygame.mixer.music.play()
        
    def pause_song(self, pause_game=True):
        if not self.is_song_paused:
            pygame.mixer.music.pause()
            
        else:
            pygame.mixer.music.unpause()
        
        self.is_song_paused: bool = not self.is_song_paused
        self.is_game_paused: bool = not self.is_game_paused
    
    def stop_song(self):
        self.is_song_playing: bool = False
        self.is_song_paused: bool = False
        self.is_game_paused: bool = False
        pygame.mixer.music.stop()
        
    def on_mouse_click(self, x, y, button, pressed):
        if str(button) == 'Button.left':
            if pressed:
                if self.roblox_window.isActive:
                    if self.target_song_id != None:
                        if self.mode == 'normal':
                            if (self.screen_data[self.screen_mode]['pos']['close_button'][0][0] + self.roblox_offset_x <= x <= self.screen_data[self.screen_mode]['pos']['close_button'][1][0] + self.roblox_offset_x) and (self.screen_data[self.screen_mode]['pos']['close_button'][0][1] + self.roblox_offset_y <= y <= self.screen_data[self.screen_mode]['pos']['close_button'][1][1] + self.roblox_offset_y) and self.is_song_paused:
                                if self.is_game_paused:
                                    self.stop_song()

                            elif (self.screen_data[self.screen_mode]['pos']['pause_button'][0][0] + self.roblox_offset_x <= x <= self.screen_data[self.screen_mode]['pos']['pause_button'][1][0] + self.roblox_offset_x) and (self.screen_data[self.screen_mode]['pos']['pause_button'][0][1] + self.roblox_offset_y <= y <= self.screen_data[self.screen_mode]['pos']['pause_button'][1][1] + self.roblox_offset_y):
                                time.sleep(0.15)
                                self.pause_song()

                            elif (self.screen_data[self.screen_mode]['pos']['play_button'][0][0] + self.roblox_offset_x <= x <= self.screen_data[self.screen_mode]['pos']['play_button'][1][0] + self.roblox_offset_x) and (self.screen_data[self.screen_mode]['pos']['play_button'][0][1] + self.roblox_offset_y <= y <= self.screen_data[self.screen_mode]['pos']['play_button'][1][1] + self.roblox_offset_y):
                                if (not self.is_song_playing and not self.is_song_paused) or (self.is_song_paused and self.is_song_playing):
                                    time.sleep(1)
                                    self.play_song()

                            elif (self.screen_data[self.screen_mode]['pos']['play_button_unpublished'][0][0] + self.roblox_offset_x <= x <= self.screen_data[self.screen_mode]['pos']['play_button_unpublished'][1][0] + self.roblox_offset_x) and (self.screen_data[self.screen_mode]['pos']['play_button_unpublished'][0][1] + self.roblox_offset_y <= y <= self.screen_data[self.screen_mode]['pos']['play_button_unpublished'][1][1] + self.roblox_offset_y):
                                if (not self.is_song_playing and not self.is_song_paused) or (self.is_song_paused and self.is_song_playing):
                                    time.sleep(1)
                                    self.play_song()

                            elif (self.screen_data[self.screen_mode]['pos']['restart_button'][0][0] + self.roblox_offset_x <= x <= self.screen_data[self.screen_mode]['pos']['restart_button'][1][0] + self.roblox_offset_x) and (self.screen_data[self.screen_mode]['pos']['restart_button'][0][1] + self.roblox_offset_y <= y <= self.screen_data[self.screen_mode]['pos']['restart_button'][1][1] + self.roblox_offset_y):
                                if self.is_game_paused:
                                    time.sleep(0.25)
                                    self.play_song()

                            elif (self.screen_data[self.screen_mode]['pos']['resume_button'][0][0] + self.roblox_offset_x <= x <= self.screen_data[self.screen_mode]['pos']['resume_button'][1][0] + self.roblox_offset_x) and (self.screen_data[self.screen_mode]['pos']['resume_button'][0][1] + self.roblox_offset_y <= y <= self.screen_data[self.screen_mode]['pos']['resume_button'][1][1] + self.roblox_offset_y):
                                if self.is_game_paused:
                                    time.sleep(0.15)
                                    self.pause_song()
                        else:
                            if (self.screen_data[self.screen_mode]['pos']['play_music_button_editor'][0][0] + self.roblox_offset_x <= x <= self.screen_data[self.screen_mode]['pos']['play_music_button_editor'][1][0] + self.roblox_offset_x) and (self.screen_data[self.screen_mode]['pos']['play_music_button_editor'][0][1] + self.roblox_offset_y <= y <= self.screen_data[self.screen_mode]['pos']['play_music_button_editor'][1][1] + self.roblox_offset_y):
                                if not self.is_song_playing:
                                    self.is_song_paused = False
                                    time.sleep(0.15)
                                    self.play_song()
                                else:
                                    time.sleep(0.15)
                                    self.pause_song()

                            elif (self.screen_data[self.screen_mode]['pos']['stop_music_button_editor'][0][0] + self.roblox_offset_x <= x <= self.screen_data[self.screen_mode]['pos']['stop_music_button_editor'][1][0] + self.roblox_offset_x) and (self.screen_data[self.screen_mode]['pos']['stop_music_button_editor'][0][1] + self.roblox_offset_y <= y <= self.screen_data[self.screen_mode]['pos']['stop_music_button_editor'][1][1] + self.roblox_offset_y) and self.is_song_playing:
                                time.sleep(0.15)
                                self.stop_song()

                            elif (self.screen_data[self.screen_mode]['pos']['play_button_editor'][0][0] + self.roblox_offset_x <= x <= self.screen_data[self.screen_mode]['pos']['play_button_editor'][1][0] + self.roblox_offset_x) and (self.screen_data[self.screen_mode]['pos']['play_button_editor'][0][1] + self.roblox_offset_y <= y <= self.screen_data[self.screen_mode]['pos']['play_button_editor'][1][1] + self.roblox_offset_y):
                                if not self.is_song_playing:
                                    self.is_song_paused = False
                                    time.sleep(0.15)
                                    self.play_song()
                            
    def on_mouse_move(self, x, y):
        if not self.roblox_window.isActive:
            if self.target_song_id != None:
                if self.is_song_playing and not self.is_song_paused:
                    time.sleep(0.15)
                    self.pause_song()
                        
    def on_keyboard_click(self, key):
        key = str(key)
        
        if self.roblox_window.isActive:
            if self.target_song_id != None:
                if key in ['Key.tab', 'Key.esc']:
                    if self.is_song_playing:
                        time.sleep(0.15)
                        self.pause_song()

                if key == "'r'":
                    self.keyboard.press(pynputkeyboard.Key.tab)
                    self.keyboard.release(pynputkeyboard.Key.tab)

                    pos = list(self.screen_data[self.screen_mode]['pos']['restart_button'])
                    temp_pos = ((pos[0][0] + pos[1][0]) / 2 + self.roblox_offset_x, (pos[0][1] + pos[1][1]) / 2 + self.roblox_offset_y)

                    self.is_song_paused = True
                    self.is_game_paused = True

                    cursor_previous_pos = self.mouse.position
                    self.mouse.position = temp_pos
                    self.mouse.click(mouse.Button.left)
                    self.mouse.position = cursor_previous_pos

                elif key == "<57>":
                    self.stop_song()
        else:
            if key == "<48>":
                self.menu()
            
            if self.target_song_id != None:
                if self.is_song_playing and not self.is_song_paused:
                    time.sleep(0.15)
                    self.pause_song()
                
    def set_song(self) -> int:
        while True:
            self.target_song_id = input('Song ID: (type none to not select it) ')
            if self.target_song_id.lower() != 'none':
                if os.path.exists(self.path.get('songs') / (self.target_song_id + ".mp3")):
                    pygame.mixer.music.load(self.path.get('songs') / (self.target_song_id + ".mp3"))
                    break
                else:
                    print('This song does not exists.\n')
                    input('>>> ')
                    os.system('cls')
            else:
                break
        
        return self.target_song_id

    def menu(self) -> typing.NoReturn:
        
        os.system('cls')

        print('NoCH (Non creator hub) songs for Beat Bounce v_beta1.1\n')
        print('Press Ctrl+0 to open settings\n')

        print('Available settings:')
        print('- set song (1)')
        
        if self.mode == 'normal': print('- switch to editor mode (2)')
        else: print('- switch to normal mode (2)')
        
        print('- see keybinds (3)')
        print('- refresh program (4)')
        print('- manually change screen shape (5)')
        print('')
        
        setting = input('>>> ')

        match setting:
            case '1':
                os.system('cls')
                self.set_song()

            case '2':
                if self.mode == 'normal':
                    self.mode = 'editor'
                    
                else:
                    self.mode = 'normal'

            case '3':
                os.system('cls')
                print('')
                print('Keybinds:')
                print('- Ctrl+0 - opens settings menu')
                print('- Ctrl+9- stops the music (in editor playtest or if something went wrong)')
                print('- R - restarts the level')
                print('- Tab - in-game keybind, pauses the game and song')
                print('- Escape - Roblox keybind, pauses the game and song')
                print('')
                input('>>> ')
                
            case '4':
                os.system('cls')
                
                # self.roblox_window = gw.getWindowsWithTitle("Roblox")[0]
                # self.roblox_resolution = (self.roblox_window.width, self.roblox_window.height)
                window_handle = win32gui.FindWindow(None, "Roblox")
                window_rect = win32gui.GetWindowRect(window_handle)
                client_rect = list(win32gui.GetClientRect(window_handle))
                
                self.roblox_resolution = (client_rect[2], client_rect[3])
                self.roblox_offset_x, self.roblox_offset_y = window_rect[0], window_rect[1]
                
                self.screen_data = {
                    '16:9': {'pos': {
                        'play_button': ((self.roblox_resolution[0] / 6.530612244897959,
                                         self.roblox_resolution[1] / 1.487603305785124),
                                        (self.roblox_resolution[0] / 2.9024943310657596,
                                         self.roblox_resolution[1] / 1.1783960720130933)),
                        
                        'play_button_unpublished': ((self.roblox_resolution[0] / 1.951219512195122,
                                                     self.roblox_resolution[1] / 1.4090019569471623),
                                                    (self.roblox_resolution[0] / 1.5292712066905616,
                                                     self.roblox_resolution[1] / 1.306715063520871)),
                        
                        'play_button_editor': ((self.roblox_resolution[0] / 1.0569777043765483,
                                                self.roblox_resolution[1] / 2.376237623762376),
                                               (self.roblox_resolution[0] / 1.019108280254777,
                                                self.roblox_resolution[1] / 2.039660056657224)),
                        
                        'play_music_button_editor': ((self.roblox_resolution[0] / 1.0569777043765483,
                                                      self.roblox_resolution[1] / 2.0),
                                                     (self.roblox_resolution[0] / 1.019108280254777,
                                                      self.roblox_resolution[1] / 1.7183770883054892)),
                        
                        'stop_music_button_editor': ((self.roblox_resolution[0] / 1.124780316344464,
                                                      self.roblox_resolution[1] / 2.0168067226890756),
                                                     (self.roblox_resolution[0] / 1.0810810810810811,
                                                      self.roblox_resolution[1] / 1.7307692307692308)),
                        
                        'restart_button': ((self.roblox_resolution[0] / 1.4222222222222223,
                                            self.roblox_resolution[1] / 1.509433962264151),
                                           (self.roblox_resolution[0] / 1.3291796469366564,
                                            self.roblox_resolution[1] / 1.338289962825279)),
                        
                        'close_button': ((self.roblox_resolution[0] / 1.610062893081761,
                                          self.roblox_resolution[1] / 2.4161073825503356),
                                         (self.roblox_resolution[0] / 1.4065934065934067,
                                          self.roblox_resolution[1] / 1.7349397590361446)),
                        
                        'pause_button': ((self.roblox_resolution[0] / 1.0774410774410774,
                                          self.roblox_resolution[1] / 15.319148936170214),
                                         (self.roblox_resolution[0] / 1.019108280254777,
                                          self.roblox_resolution[1] / 6.260869565217392)),
                        
                        'resume_button': ((self.roblox_resolution[0] / 2.237762237762238,
                                           self.roblox_resolution[1] / 2.5),
                                          (self.roblox_resolution[0] / 1.8104667609618104,
                                           self.roblox_resolution[1] / 1.6941176470588235))
                    }},
                    '5:4': {'pos': {
                        'play_button': ((self.roblox_resolution[0] / 9.257142857142858,
                                        self.roblox_resolution[1] / 1.5303030303030303),
                                        (self.roblox_resolution[0] / 3.24,
                                         self.roblox_resolution[1] / 1.286624203821656)),
                        
                        'play_button_unpublished': ((self.roblox_resolution[0] / 1.9696048632218845,
                                                     self.roblox_resolution[1] / 1.3741496598639455),
                                                    (self.roblox_resolution[0] / 1.5558223289315727,
                                                     self.roblox_resolution[1] / 1.2849872773536897)),
                        
                        'play_button_editor': ((self.roblox_resolution[0] / 1.0719602977667493,
                                                self.roblox_resolution[1] / 2.234513274336283),
                                               (self.roblox_resolution[0] / 1.034317637669593,
                                                self.roblox_resolution[1] / 2.0079522862823063)),
                        
                        'play_music_button_editor': ((self.roblox_resolution[0] / 1.0719602977667493,
                                                      self.roblox_resolution[1] / 1.97265625),
                                                     (self.roblox_resolution[0] / 1.034317637669593,
                                                      self.roblox_resolution[1] / 1.7939609236234457)),
        
                        'stop_music_button_editor': ((self.roblox_resolution[0] / 1.1592128801431127,
                                                      self.roblox_resolution[1] / 2.0159680638722555),
                                                     (self.roblox_resolution[0] / 1.0881612090680102,
                                                      self.roblox_resolution[1] / 1.7474048442906573)),
                        
                        'restart_button': ((self.roblox_resolution[0] / 1.481142857142857,
                                            self.roblox_resolution[1] / 1.4962962962962962),
                                           (self.roblox_resolution[0] / 1.3224489795918368,
                                            self.roblox_resolution[1] / 1.303225806451613)),
        
                        'close_button': ((self.roblox_resolution[0] / 1.683116883116883,
                                          self.roblox_resolution[1] / 2.3488372093023258),
                                         (self.roblox_resolution[0] / 1.3935483870967742,
                                          self.roblox_resolution[1] / 1.7413793103448276)),
                        
                        'pause_button': ((self.roblox_resolution[0] / 1.1124463519313306,
                                          self.roblox_resolution[1] / 28.857142857142858),
                                         (self.roblox_resolution[0] / 1.016470588235294,
                                          self.roblox_resolution[1] / 6.733333333333333)),
                        
                        'resume_button': ((self.roblox_resolution[0] / 2.4,
                                           self.roblox_resolution[1] / 2.4634146341463414),
                                          (self.roblox_resolution[0] / 1.7753424657534247,
                                           self.roblox_resolution[1] / 1.6833333333333333))
                    }},
                    '4:3': {'pos': {
                        'play_button': ((self.roblox_resolution[0] / 9.014084507042254,
                                        self.roblox_resolution[1] / 1.5311004784688995),
                                        (self.roblox_resolution[0] / 3.18407960199005,
                                         self.roblox_resolution[1] / 1.2581913499344692655)),
                        
                        'play_button_unpublished': ((self.roblox_resolution[0] / 1.9541984732824427,
                                                     self.roblox_resolution[1] / 1.3953488372093024),
                                                    (self.roblox_resolution[0] / 1.5292712066905616,
                                                     self.roblox_resolution[1] / 1.2990527740189446)),
                        
                        'play_button_editor': ((self.roblox_resolution[0] / 1.0587262200165426,
                                                self.roblox_resolution[1] / 2.302158273381295),
                                               (self.roblox_resolution[0] / 1.0207336523125996,
                                                self.roblox_resolution[1] / 2.0168067226890756)),
                        
                        'play_music_button_editor': ((self.roblox_resolution[0] / 1.0587262200165426,
                                                      self.roblox_resolution[1] / 2.00836820083682),
                                                     (self.roblox_resolution[0] / 1.0207336523125996,
                                                      self.roblox_resolution[1] / 1.7744916820702403)),
        
                        'stop_music_button_editor': ((self.roblox_resolution[0] / 1.1297440423654015,
                                                      self.roblox_resolution[1] / 2.0125786163522013),
                                                     (self.roblox_resolution[0] / 1.0865874363327674,
                                                      self.roblox_resolution[1] / 1.7777777777777777)),
                        
                        'restart_button': ((self.roblox_resolution[0] / 1.4269788182831662,
                                            self.roblox_resolution[1] / 1.4837712519319939),
                                           (self.roblox_resolution[0] / 1.3250517598343685,
                                            self.roblox_resolution[1] / 1.3407821229050279)),
        
                        'close_button': ((self.roblox_resolution[0] / 1.6558861578266495,
                                          self.roblox_resolution[1] / 2.4242424242424243),
                                         (self.roblox_resolution[0] / 1.3719185423365488,
                                          self.roblox_resolution[1] / 1.7266187050359711)),
                        
                        'pause_button': ((self.roblox_resolution[0] / 1.0774410774410774,
                                          self.roblox_resolution[1] / 18.46153846153846),
                                         (self.roblox_resolution[0] / 1.0182975338106603,
                                          self.roblox_resolution[1] / 7.933884297520661)),
                        
                        'resume_button': ((self.roblox_resolution[0] / 2.335766423357664,
                                           self.roblox_resolution[1] / 2.4935064935064934),
                                          (self.roblox_resolution[0] / 1.7510259917920656,
                                           self.roblox_resolution[1] / 1.6901408450704225))
                    }}
                }
                
            case '5':
                while True:
                    print('Pick a screen shape (16:9, 5:4, 4:3)')
                    print('Type none to not change it')
                    shape = input('>>> ')
                    
                    if shape.lower() in ['16:9', '5:4', '4:3', 'none']:
                        if shape.lower() != 'none':
                            self.screen_mode = shape
                        break
                    else:
                        print('This screen shape is not implemented')
                        input('>>> ')
                        os.system('cls')
            case _:
                os.system('cls')
                print('This setting does not exists.')
                print('>>> ')

        os.system('cls')
        print('NoCH (Non creator hub) songs for Beat Bounce v_beta1.1\n')
        print('Press Ctrl+0 to open settings\n')
    
    def run(self) -> typing.NoReturn:
        os.system('cls')
        
        self.menu()
        
        pynputkeyboard.Listener(on_press=self.on_keyboard_click).start()
        
        with mouse.Listener(on_click=self.on_mouse_click) as listener:
            listener.join()
    
if __name__ == '__main__':
    app = App()
    app.run()
            
            

