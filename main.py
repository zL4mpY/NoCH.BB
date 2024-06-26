import os
import sys
import keyboard
import pygame
import typing
import time
import tkinter
import pyperclip
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

try:
    roblox_window = gw.getWindowsWithTitle("Roblox")[0]
except IndexError:
    print("Open Roblox first and then open this program.")
    exit()

size = (roblox_window.width, roblox_window.height)
offset_x, offset_y = roblox_window.topleft

# pyperclip.copy(f'((size[0] / {size[0] / 1209}, size[1] / {size[1] / 512}), (size[0] / {size[0] / 1253}, size[1] / {size[1] / 563}))')

if not os.path.exists(BASE_DIR / "songs"):
    os.mkdir(BASE_DIR / "songs")

class App():
    def __init__(self) -> None:
        self.path = {
            'songs': BASE_DIR / 'songs'
            }
        
        self.data = {
            'pos': {
                'play_button': ((size[0] / 9.257142857142858,
                                size[1] / 1.5303030303030303),
                                (size[0] / 3.24,
                                 size[1] / 1.286624203821656)),
                
                'play_button_unpublished': ((size[0] / 1.9696048632218845,
                                             size[1] / 1.3741496598639455),
                                            (size[0] / 1.5558223289315727,
                                             size[1] / 1.2849872773536897)),
                
                'play_button_editor': ((size[0] / 1.0719602977667493,
                                        size[1] / 2.234513274336283),
                                       (size[0] / 1.034317637669593,
                                        size[1] / 2.0079522862823063)),
                
                'play_music_button_editor': ((size[0] / 1.0719602977667493,
                                              size[1] / 1.97265625),
                                             (size[0] / 1.034317637669593,
                                              size[1] / 1.7939609236234457)),

                'stop_music_button_editor': ((size[0] / 1.1592128801431127,
                                              size[1] / 2.0159680638722555),
                                             (size[0] / 1.0881612090680102,
                                              size[1] / 1.7474048442906573)),
                
                'restart_button': ((size[0] / 1.481142857142857,
                                    size[1] / 1.4962962962962962),
                                   (size[0] / 1.3224489795918368,
                                    size[1] / 1.303225806451613),
                                   ((size[0] / 1.481142857142857 + size[0] / 1.3224489795918368) / 2,
                                    (size[1] / 1.4962962962962962 + size[1] / 1.303225806451613) / 2)),

                'close_button': ((size[0] / 1.683116883116883,
                                  size[1] / 2.3488372093023258),
                                 (size[0] / 1.3935483870967742,
                                  size[1] / 1.7413793103448276)),
                
                'pause_button': ((size[0] / 1.1124463519313306,
                                  size[1] / 28.857142857142858),
                                 (size[0] / 1.016470588235294,
                                  size[1] / 6.733333333333333)),
                
                'resume_button': ((size[0] / 2.4,
                                   size[1] / 2.4634146341463414),
                                  (size[0] / 1.7753424657534247,
                                   size[1] / 1.6833333333333333))
            }
        }
        
        self.target_song_id: int | None = None
        self.is_song_playing: bool = False
        self.is_song_paused: bool = False
        self.is_game_paused: bool = False
        self.mode = 'normal'
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
                if roblox_window.isActive:
                    if self.mode == 'normal':
                        if (self.data['pos']['close_button'][0][0] + offset_x <= x <= self.data['pos']['close_button'][1][0] + offset_x) and (self.data['pos']['close_button'][0][1] + offset_y <= y <= self.data['pos']['close_button'][1][1] + offset_y) and self.is_song_paused:
                            if self.is_game_paused:
                                self.stop_song()

                        elif (self.data['pos']['pause_button'][0][0] + offset_x <= x <= self.data['pos']['pause_button'][1][0] + offset_x) and (self.data['pos']['pause_button'][0][1] + offset_y <= y <= self.data['pos']['pause_button'][1][1] + offset_y):
                            time.sleep(0.15)
                            self.pause_song()

                        elif (self.data['pos']['play_button'][0][0] + offset_x <= x <= self.data['pos']['play_button'][1][0] + offset_x) and (self.data['pos']['play_button'][0][1] + offset_y <= y <= self.data['pos']['play_button'][1][1] + offset_y):
                            if (not self.is_song_playing and not self.is_song_paused) or (self.is_song_paused and self.is_song_playing):
                                time.sleep(1)
                                self.play_song()

                        elif (self.data['pos']['play_button_unpublished'][0][0] + offset_x <= x <= self.data['pos']['play_button_unpublished'][1][0] + offset_x) and (self.data['pos']['play_button_unpublished'][0][1] + offset_y <= y <= self.data['pos']['play_button_unpublished'][1][1] + offset_y):
                            if (not self.is_song_playing and not self.is_song_paused) or (self.is_song_paused and self.is_song_playing):
                                time.sleep(1)
                                self.play_song()

                        elif (self.data['pos']['restart_button'][0][0] + offset_x <= x <= self.data['pos']['restart_button'][1][0] + offset_x) and (self.data['pos']['restart_button'][0][1] + offset_y <= y <= self.data['pos']['restart_button'][1][1] + offset_y):
                            if self.is_game_paused:
                                time.sleep(0.25)
                                self.play_song()

                        elif (self.data['pos']['resume_button'][0][0] + offset_x <= x <= self.data['pos']['resume_button'][1][0] + offset_x) and (self.data['pos']['resume_button'][0][1] + offset_y <= y <= self.data['pos']['resume_button'][1][1] + offset_y):
                            if self.is_game_paused:
                                time.sleep(0.15)
                                self.pause_song()
                    else:
                        if (self.data['pos']['play_music_button_editor'][0][0] + offset_x <= x <= self.data['pos']['play_music_button_editor'][1][0] + offset_x) and (self.data['pos']['play_music_button_editor'][0][1] + offset_y <= y <= self.data['pos']['play_music_button_editor'][1][1] + offset_y):
                            if not self.is_song_playing:
                                self.is_song_paused = False
                                time.sleep(0.15)
                                self.play_song()
                            else:
                                self.pause_song()
                                
                        elif (self.data['pos']['stop_music_button_editor'][0][0] + offset_x <= x <= self.data['pos']['stop_music_button_editor'][1][0] + offset_x) and (self.data['pos']['stop_music_button_editor'][0][1] + offset_y <= y <= self.data['pos']['stop_music_button_editor'][1][1] + offset_y) and self.is_song_playing:
                            self.stop_song()
                            
                        elif (self.data['pos']['play_button_editor'][0][0] + offset_x <= x <= self.data['pos']['play_button_editor'][1][0] + offset_x) and (self.data['pos']['play_button_editor'][0][1] + offset_y <= y <= self.data['pos']['play_button_editor'][1][1] + offset_y):
                            if not self.is_song_playing:
                                self.is_song_paused = False
                                time.sleep(0.15)
                                self.play_song()
                            
    def on_mouse_move(self, x, y):
        if not roblox_window.isActive:
            time.sleep(0.15)
            self.pause_song()
                        
    def on_keyboard_click(self, key):
        key = str(key)
        
        if roblox_window.isActive:
            if key in ['Key.tab', 'Key.esc']:
                if self.is_song_playing:
                    time.sleep(0.15)
                    self.pause_song()

            if key == "'r'":
                self.keyboard.press(pynputkeyboard.Key.tab)
                self.keyboard.release(pynputkeyboard.Key.tab)

                pos = list(self.data['pos']['restart_button'])
                temp_pos = (pos[2][0] + offset_x, pos[2][1] + offset_y)

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
            
            if self.is_song_playing and not self.is_song_paused:
                time.sleep(0.15)
                self.pause_song()
                
    def set_song(self) -> int:
        while True:
            self.target_song_id = input('Song ID: ')
            if os.path.exists(self.path.get('songs') / (self.target_song_id + ".mp3")):
                pygame.mixer.music.load(self.path.get('songs') / (self.target_song_id + ".mp3"))
                break
            else:
                print('This song does not exists.\n')
        
        print('\nHave fun!')
        time.sleep(0.5)
        return self.target_song_id

    def menu(self) -> typing.NoReturn:
        os.system('cls')

        print('NoCH (Non creator hub) songs for Beat Bounce v1.0\n')
        print('Press Ctrl+0 to open settings\n')

        print('Available settings:')
        print('- set song (1)')
        if self.mode == 'normal': print('- switch to editor mode (2)')
        else: print('- switch to normal mode (2)')
        print('- see keybinds (3)')
        print('')
        
        setting = int(input('>>> '))

        match setting:
            case 1:
                self.set_song()

            case 2:
                if self.mode == 'normal':
                    self.mode = 'editor'
                    
                else:
                    self.mode = 'normal'

            case 3:
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
            case _:
                pass

        os.system('cls')
        print('NoCH (Non creator hub) songs for Beat Bounce v1.0\n')
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
            
            

