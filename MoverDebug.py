import pygetwindow as gw
import win32api
from pynput import mouse

def get_current_screen():
    # Get the active window
    active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)[0]

    # Get the window handle
    window_handle = active_window._hWnd

    # Call the Windows API to get the monitor information
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(window_handle))

    # Extract the screen index
    screen_index = monitor_info['Monitor']
    
    print(screen_index)
    return screen_index

def move_window_to_next_screen():
    current_screen = get_current_screen()

    # Get the active window
    active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)[0]

    # Get the screen width
    screen_width = win32api.GetSystemMetrics(0)
    print(screen_width)

    # Get the current window position and size
    x, y, width, height = active_window.left, active_window.top, active_window.width, active_window.height
    print(x,y)

    # Calculate the new position on the next screen
    if current_screen[0] != 0 and active_window.isMaximized:
        new_x = 229
        new_y = 220
        active_window.restore()
        active_window.moveTo(new_x, new_y)
        active_window.maximize()
        print("first max " + str(new_x) + " " + str(new_y))
    elif current_screen[0] == 0 and active_window.isMaximized:
        new_x = -1691
        new_y = 220
        active_window.restore()
        active_window.moveTo(new_x, new_y)
        active_window.maximize()
        print("last max " + str(new_x) + " " + str(new_y))
    elif current_screen[0] != 0:
        new_x = x + screen_width
        new_y = y
        active_window.moveTo(new_x, new_y)
        print("first " + str(new_x) + " " + str(new_y))
    else:
        new_x = x - screen_width
        new_y = y
        active_window.moveTo(new_x, new_y)
        print("last " + str(new_x) + " " + str(new_y))

    # Move the window to the new position
    # active_window.moveTo(new_x, new_y)

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.x2:
        move_window_to_next_screen()

# Create a mouse listener
mouse_listener = mouse.Listener(on_click=on_click)

# Start the listener in a separate thread
mouse_listener.start()

# Keep the script running
mouse_listener.join()