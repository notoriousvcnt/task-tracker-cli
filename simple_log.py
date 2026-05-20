# --- SIMPLE LOG FUNCTION ---- #
active = False
def log(msg):
    global active
    if active:
        print(msg)