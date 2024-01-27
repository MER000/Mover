import pygetwindow as gw
import win32api
from pynput import mouse
import time
from infi.systray import SysTrayIcon
from contextlib import suppress

print("Booting...")

prev_window = "0"
anim_time = 0.23

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
    
    print("memory: " + prev_window.title)

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
            print("empty wuzza")
            move_prev_window_to_next_screen()
            return
    except AttributeError:
        print("wuzza")
        move_prev_window_to_next_screen()
        return

    # Get the active window
    active_window = gw.getWindowsAt(x, y)[0]
    print("active: " + active_window.title)
    prev_window = active_window

    # Extract the screen info
    screen_index = get_screen_index(active_window)
    screen_width = win32api.GetSystemMetrics(0)

    # Get the current window position and size
    x, y = active_window.left, active_window.top

    # Calculate the new position on the next screen
    if  screen_index[0] != 0 and active_window.isMaximized:
        new_x = 229
        new_y = 220
        with suppress(Exception):
            active_window.activate()
        active_window.restore()
        active_window.moveTo(new_x, new_y)
        time.sleep(anim_time)
        active_window.maximize()
    elif screen_index[0] == 0 and active_window.isMaximized:
        new_x = -1691
        new_y = 220
        with suppress(Exception):
            active_window.activate()
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
    if pressed and button == mouse.Button.x2:
        move_window_to_next_screen(x, y)


# Create a mouse listener
mouse_listener = mouse.Listener(on_click=on_click)

print("......")

# Start the listener in a separate thread
mouse_listener.start()

print("We Up!")

# Keep the script running
# mouse_listener.join()                                                     ancient code


def on_quit_callback(systray):
    mouse_listener.stop()
    systray.shutdown()


def movin(systray):
    systray.update(hover_text="Moovin...")


menu_options = (("", None, movin),)
systray = SysTrayIcon("movericon2.ico", "Mover", menu_options, on_quit=on_quit_callback)
systray.start()
