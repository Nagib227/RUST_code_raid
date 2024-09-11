import threading
import keyboard
import time
import mouse
import win32api, win32con
import pyautogui
from utils.mouse import MouseControls
import pyautogui
from PIL import Image, ImageGrab
import json
from pynput.keyboard import Listener


def move(key):
    global t
    way = "right" if key == "y" else "left"
            
    while True:
        move_mouse(way)
        mouse_events.append([way, time.time()-t])
        t = time.time()
        if not keyboard.is_pressed(key):
            break
        time.sleep(0.0005)


def on_press(e):
    # print(e, e.event_type, e.name)
    if e.name.upper() == "Y" and e.event_type == "down":
            y_thread = threading.Thread(target = lambda: move("y"))
            y_thread.start()
            y_thread.join()
    elif e.name.upper() == "T" and e.event_type == "down":
            y_thread = threading.Thread(target = lambda: move("t"))
            y_thread.start()
            y_thread.join()
    
    
def play_mouse(mouse_events):
    for i in mouse_events:
        move_mouse(i[0])
        time.sleep(i[1])
        

def is_death():
    try:
        pyautogui.locateOnScreen('death.png', confidence=0.95)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def save_cur_door_screenshot(x1, y1, x2, y2):
    pic = ImageGrab.grab(bbox=(x1, y1, x2, y2)) 
    pic.save("cur_door.png", 'PNG')
    # pic = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
    # pic.save("cur_door.png")

    
def is_open_door():
    pyautogui.keyDown('e')
    time.sleep(0.2)
    mouse_control.move_relative(50, 200)
    time.sleep(0.02)
    pyautogui.click(pyautogui.position()[0] , pyautogui.position()[1])
    # time.sleep(0.5)
    mouse_control.move_relative(-32, -130)
    pyautogui.keyUp('e')

    time.sleep(0.1)
    if is_open_code_menu():
        return "open_code_menu"

    res = False
    
    pyautogui.keyDown('e')
    time.sleep(0.3)
    
    # save_cur_door_screenshot(1014, 794, 1014+76, 794+76)
    # Box(left=1134, top=720, width=76, height=76)
    try:
        pyautogui.locateOnScreen('is_open_door.png', confidence=0.95)
        res = True
    except pyautogui.ImageNotFoundException:
        res = False
    pyautogui.keyUp('e')
    
    if res:
        pyautogui.keyDown('e')
        pyautogui.keyUp('e')

    return res

# time.sleep(1)
# print(is_open_door())


def is_open_code_menu():
    mouse_control.move_relative(0, 130)
    time.sleep(0.5)
    
    save_cur_door_screenshot(820, 678, 820+275, 678+20)
    
    h1 = Image.open("cur_door.png").histogram()
    h2 = Image.open("is_open_code_menu.png").histogram()

    mouse_control.move_relative(0, -130)
    
    return h1 == h2

def open_code_menu():
    pyautogui.keyDown('e')
    pyautogui.keyUp('e')
    if is_open_code_menu():
        return 
    pyautogui.keyDown('e')
    time.sleep(0.2)
    mouse_control.move_relative(50, 200)
    time.sleep(0.05)
    pyautogui.click(pyautogui.position()[0] , pyautogui.position()[1])
    mouse_control.move_relative(-50, -200)
    pyautogui.keyUp('e')


def enter_code():
    global cur_ind_code

    pyautogui.keyDown(codes[cur_ind_code][0])
    pyautogui.keyUp(codes[cur_ind_code][0])
    # keyboard.press()
    # time.sleep(0)
    pyautogui.keyDown(codes[cur_ind_code][1])
    pyautogui.keyUp(codes[cur_ind_code][1])
    # keyboard.press(codes[cur_ind_code][1])
    # time.sleep(0)
    pyautogui.keyDown(codes[cur_ind_code][2])
    pyautogui.keyUp(codes[cur_ind_code][2])
    # keyboard.press(codes[cur_ind_code][2])
    # time.sleep(0)
    pyautogui.keyDown(codes[cur_ind_code][3])
    pyautogui.keyUp(codes[cur_ind_code][3])
    # keyboard.press(codes[cur_ind_code][3])

    print("code:", cur_ind_code + start_code, "-", codes[cur_ind_code])
    
    with open("codes.txt", "a") as f:
        f.write(codes[cur_ind_code] + "\n")
        
    cur_ind_code += 1

    
def open_code_menu_and_enter_code():
    # print(is_open_door())
    res = is_open_door()
    if res == "open_code_menu":
        enter_code()
        return
    elif res:
        exit(-1)
    # print(is_open_door())
    open_code_menu()
    if is_open_code_menu():
        enter_code()
        return
    if not is_death():
        pyautogui.keyDown('f1')
        pyautogui.keyUp('f1')
        pyautogui.keyDown('k')
        pyautogui.keyUp('k')
        pyautogui.keyDown('i')
        pyautogui.keyUp('i')
        pyautogui.keyDown('l')
        pyautogui.keyUp('l')
        pyautogui.keyDown('l')
        pyautogui.keyUp('l')
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')


# time.sleep(1)
# open_code_menu_and_enter_code()
# time.sleep(1)
# open_code_menu_and_enter_code()
# time.sleep(1)
# open_code_menu_and_enter_code()

    
def move_mouse(way):
    if way == "left":
        mouse_control.move_relative(-1, 0)
    if way == "right":
        mouse_control.move_relative(1, 0)


def start_macros(keyboard_events, mouse_events):
    # print(keyboard_events)
    # print(mouse_events)
    time.sleep(3)
    pyautogui.keyDown("space")
    pyautogui.keyUp("space")
    k_thread = threading.Thread(target = lambda: keyboard.play(keyboard_events))
    m_thread = threading.Thread(target = lambda: play_mouse(mouse_events))
    k_thread.start()
    m_thread.start()
    k_thread.join()
    m_thread.join()


def start_recording_macros():
    global t

    keyboard.hook(on_press)
    
    print("start_recording")
    # mouse.hook(mouse_events.append)
    t = time.time()
    keyboard.start_recording()



def stop_recording_macros():
    print("stop_recording")
    # mouse.unhook(mouse_events.append)
    keyboard.unhook_all()
    keyboard_events = keyboard.stop_recording()
    return keyboard_events



def record_macroses():
    print("введите кнопку спальника")
    btn = input()
    while btn not in ["z", "t", "y" "h"] and len(btn) == 1:
        keyboard_events = None
    
        print("Нажмите z, для начала записи макроса и h для остановки записи макроса")
        keyboard.wait("z")
        start_recording_macros()

        keyboard.wait("h")
        
        keyboard_events = stop_recording_macros()

        print("Сохраняем?(y/n)")
        if input() == "y":
            with open(f'{btn}_k.txt', 'w', encoding='utf-8') as f:
                f.writelines( [ ke.to_json()+'\n' for ke in keyboard_events ] )
            with open(f'{btn}_m.txt', 'w', encoding='utf-8') as f:
                f.write(str(mouse_events))
            macroses.append(btn)

        
        print("введите кнопку спальника")
        btn = input()



def main():
    while True:
        for i in macroses:
            pyautogui.keyDown(i)
            pyautogui.keyUp(i)
            time.sleep(0.5)
            if not is_death():
                with open(f'{i}_k.txt', 'r', encoding='utf-8') as f:
                    keyboard_events = [ keyboard.KeyboardEvent(**json.loads(js)) for js in f.readlines()]
                with open(f'{i}_m.txt', 'r', encoding='utf-8') as f:
                    mouse_events = eval(f.read())
                test = time.time()
                start_macros(keyboard_events, mouse_events)
                while not is_death():
                    open_code_menu_and_enter_code()
                    mouse_control.move_relative(1, 1)
                    mouse_control.move_relative(-1, -1)
                    time.sleep(0.8)
                print(time.time()-test)
        time.sleep(3)



mouse_events = []
t = None
listener = None
cur_ind_code = 0
mouse_control = MouseControls()
with open("codes.txt", "w") as f:
    f.write("History_codes:\n")    

print("буквы предидуших макросов")
macroses = list(input())
# macroses = []

print("0-10000")
start_code = int(input())
finish_code = int(input())
# start_code = 0
# finish_code = 5

with open("all_codes.txt", "r") as f:
    codes = f.read().split()[start_code:finish_code]


if __name__ == "__main__":      
    print("z, t, y, h")
    print("input.bind [кнопка] respawn_sleepingbag [id спалки в расте]")
    input()
    record_macroses()
    print("Макросы записаны, для запуска z")

    keyboard.wait("z")

    main()
