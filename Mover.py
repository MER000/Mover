import pygetwindow as gw
from pygetwindow import PyGetWindowException
import win32api
from pynput import mouse, keyboard
import time
from infi.systray import SysTrayIcon
from contextlib import suppress
import pywinauto

print("Booting...")

# GLOBALS
prev_window = "0"
anim_time = 0.23
active = True

def get_screen_index(window):
    # Get the window handle
    window_handle = window._hWnd

    # Call the Windows API to get the monitor information
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(window_handle))

    # Extract the screen index
    screen_index = monitor_info['Monitor']

    return screen_index

def move_prev_window_to_next_screen():
    if prev_window == "0":
        return;
    
    # Extract the screen info
    screen_index = get_screen_index(prev_window)
    screen_width = win32api.GetSystemMetrics(0)

    x, y = prev_window.left, prev_window.top

    if screen_index[0] != 0 and prev_window.isMaximized:
        new_x = 229
        new_y = 220
        prev_window.restore()
        prev_window.moveTo(new_x, new_y)
        time.sleep(anim_time)
        prev_window.maximize()
    elif screen_index[0] == 0 and prev_window.isMaximized:
        new_x = -1691
        new_y = 220
        prev_window.restore()
        prev_window.moveTo(new_x, new_y)
        time.sleep(anim_time)
        prev_window.maximize()
    elif screen_index[0] != 0:
        new_x = x + screen_width
        new_y = y
        prev_window.moveTo(new_x, new_y)
    else:
        new_x = x - screen_width
        new_y = y
        prev_window.moveTo(new_x, new_y)


def move_window_to_next_screen(x, y):
    global prev_window
    
    # Error check if window is null
    # if gw.getActiveWindow() == None:
    cur_window_title = gw.getWindowsAt(x, y)[0].title
    
    try:
        if cur_window_title == "" or cur_window_title == "Windows Input Experience":
            move_prev_window_to_next_screen()
            return
    except AttributeError:
        move_prev_window_to_next_screen()
        return

    # Get the active window
    active_window = gw.getWindowsAt(x, y)[0]
    prev_window = active_window

    # Extract the screen info
    screen_index = get_screen_index(active_window)
    screen_width = win32api.GetSystemMetrics(0)

    # Get the current window position and size
    x, y = active_window.left, active_window.top
            
    try:
        active_window.activate()
    except PyGetWindowException:
        pywinauto.application.Application().connect(handle=active_window._hWnd).top_window().set_focus()       #neccesarry to link proccess of window for everything to work smoothly
        active_window.activate()

    # Calculate the new position on the next screen
    if  screen_index[0] != 0 and active_window.isMaximized:
        new_x = 229
        new_y = 220
        active_window.restore()
        active_window.moveTo(new_x, new_y)
        time.sleep(anim_time)
        active_window.maximize()
    elif screen_index[0] == 0 and active_window.isMaximized:
        new_x = -1691
        new_y = 220
        active_window.restore()
        active_window.moveTo(new_x, new_y)
        time.sleep(anim_time)
        active_window.maximize()
    elif screen_index[0] != 0:
        new_x = x + screen_width
        new_y = y
        active_window.moveTo(new_x, new_y)
    else:
        new_x = x - screen_width
        new_y = y
        active_window.moveTo(new_x, new_y)

    # Move the window to the new position
    # active_window.moveTo(new_x, new_y)

def on_click(x, y, button, pressed):
    if pressed and active and button == mouse.Button.x2:
        move_window_to_next_screen(x, y)


# Create a mouse listener
mouse_listener = mouse.Listener(on_click=on_click)
#keyboard_listener = keyboard.Listener(on_press=on_press)

print("......")

# Start the listener in a separate thread
#keyboard_listener.start()
mouse_listener.start()

print("We Up!")

# Keep the script running
# mouse_listener.join()                                                     ancient code


def on_quit_callback(systray):
    mouse_listener.stop()
    l.stop()
    systray.shutdown()


def movin(systray):
    systray.update(hover_text="Moovin...")


menu_options = (("", None, movin),)
systray = SysTrayIcon("movericon2.ico", "Mover", menu_options, on_quit=on_quit_callback)
systray.start()

def toggle(bool):
    return not bool

def on_activate():
    global active
    active = toggle(active)

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<shift>+/'),
    on_activate)
with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
    l.join()