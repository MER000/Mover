import pygetwindow as gw
import win32api
from pynput import mouse
import time
from infi.systray import SysTrayIcon

print("Booting...")

prev_window = "0"

def get_current_screen():
    global prev_window
    # Error check if window is null
    if gw.getActiveWindow() == None:
        return

    # Get the active window
    active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)[0]
    prev_window = active_window

    # Get the window handle
    window_handle = active_window._hWnd

    # Call the Windows API to get the monitor information
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(window_handle))

    # Extract the screen index
    screen_index = monitor_info['Monitor']
    
    return screen_index

def move_prev_window_to_next_screen():
    global prev_window
    
    if prev_window == "0":
        return;
    
    # Get the window handle
    window_handle = prev_window._hWnd

    # Call the Windows API to get the monitor information
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(window_handle))

    # Extract the screen info
    screen_index = monitor_info['Monitor']

    screen_width = win32api.GetSystemMetrics(0)

    x, y = prev_window.left, prev_window.top
        
    if screen_index[0] != 0 and prev_window.isMaximized:
        new_x = 229
        new_y = 220
        prev_window.restore()
        prev_window.moveTo(new_x, new_y)
        time.sleep(0.2333)
        prev_window.maximize()
    elif screen_index[0] == 0 and prev_window.isMaximized:
        new_x = -1691
        new_y = 220
        prev_window.restore()
        prev_window.moveTo(new_x, new_y)
        time.sleep(0.2333)
        prev_window.maximize()
    elif screen_index[0] != 0:
        new_x = x + screen_width
        new_y = y
        prev_window.moveTo(new_x, new_y)
    else:
        new_x = x - screen_width
        new_y = y
        prev_window.moveTo(new_x, new_y)

def move_window_to_next_screen():
    # Error check if window is null
    #if gw.getActiveWindow() == None:
    try:
        if gw.getActiveWindow().title == "":
            move_prev_window_to_next_screen()
            return
    except AttributeError:
        move_prev_window_to_next_screen()
        return

    current_screen = get_current_screen()

    # Get the active window
    active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)[0]

    # Get the screen width
    screen_width = win32api.GetSystemMetrics(0)

    # Get the current window position and size
    x, y, width, height = active_window.left, active_window.top, active_window.width, active_window.height

    # Calculate the new position on the next screen
    if current_screen[0] != 0 and active_window.isMaximized:
        new_x = 229
        new_y = 220
        active_window.restore()
        active_window.moveTo(new_x, new_y)
        time.sleep(0.2333)
        active_window.maximize()
    elif current_screen[0] == 0 and active_window.isMaximized:
        new_x = -1691
        new_y = 220
        active_window.restore()
        active_window.moveTo(new_x, new_y)
        time.sleep(0.2333)
        active_window.maximize()
    elif current_screen[0] != 0:
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
        move_window_to_next_screen()

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
