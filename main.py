# imports ------------------------------------------------------
import os
import sys
import json
# --------------------------------------------------------------

# getting path -------------------------------------------------
if getattr(sys, 'frozen', False):
    APP_PATH: str = os.path.dirname(sys.executable)
elif __file__:
    APP_PATH: str = os.path.dirname(__file__)
CALL_PATH: str = os.getcwd()
# --------------------------------------------------------------

# work functions -----------------------------------------------
def is_empty(path: str) -> bool: # function for checking is the file empty
    with open(path, 'r') as tl:
        text = tl.read()
    if text == "" or text == " " * len(text):
        return True
    else:
        return False


def init() -> None: # function for initing scd-lock.json
    with open(f"{APP_PATH}\\scd-lock.json", 'w') as sl:
        sl.write(json.dumps({"binded": {}, "saved": [], "recent": []}, ensure_ascii=False, indent=4))

def create_if_not() -> None: # function for creating scd-lock.json if there is no one
    if not os.path.exists(f"{APP_PATH}\\scd-lock.json") or is_empty(f"{APP_PATH}\\scd-lock.json"):
        init()


def get(property: str) -> dict | list: # function for getting some property
    create_if_not()
    with open(f"{APP_PATH}\\scd-lock.json", 'r') as sl:
        scd_lock: dict = json.loads(sl.read())
    return scd_lock[property]


def show(property: str) -> None: # function for showing some property
    scd_lock_property: dict | list = get(property)
    if len(scd_lock_property) == 0:
        print(f"echo {property.capitalize()} list is empty")
    else:
        if isinstance(scd_lock_property, dict):
            print("\n".join(list(map(lambda x, i: f"echo [{i}] {x}: {scd_lock_property[x]}", scd_lock_property, [i for i in range(1, len(scd_lock_property) + 1)]))))
        else:
            print("\n".join(list(map(lambda x, i: f"echo [{i}] {x}", scd_lock_property, [i for i in range(1, len(scd_lock_property) + 1)]))))

def clear(property: str) -> None: # function for clearing some property
    create_if_not()
    with open(f"{APP_PATH}\\scd-lock.json", 'r') as sl:
        scd_lock: dict = json.loads(sl.read())
    if isinstance(scd_lock[property], dict):
        scd_lock[property] = {}
    else:
        scd_lock[property] = []
    with open(f"{APP_PATH}\\scd-lock.json", 'w') as sl:
        sl.write(json.dumps(scd_lock, ensure_ascii=False, indent=4))

def add(property: str, value: str, key: str = "") -> None: # function for adding some path to some property
    create_if_not()
    with open(f"{APP_PATH}\\scd-lock.json", 'r') as sl:
        scd_lock: dict = json.loads(sl.read())
    if isinstance(scd_lock[property], dict):
        scd_lock[property] = {**{key: value}, **scd_lock[property]}
    else:
        if value not in scd_lock[property]:
            scd_lock[property] = [value] + scd_lock[property]
        else:
            scd_lock[property].pop(scd_lock[property].index(value))
            scd_lock[property] = [value] + scd_lock[property]
        scd_lock[property] = scd_lock[property][:min(len(scd_lock[property]), 25)]
    with open(f"{APP_PATH}\\scd-lock.json", 'w') as sl:
        sl.write(json.dumps(scd_lock, ensure_ascii=False, indent=4))

def delete(property: str, key: int | str) -> None: # function for deleting some path from some property
    create_if_not()
    with open(f"{APP_PATH}\\scd-lock.json", 'r') as sl:
        scd_lock: dict = json.loads(sl.read())
    scd_lock[property].pop(key)
    with open(f"{APP_PATH}\\scd-lock.json", 'w') as sl:
        sl.write(json.dumps(scd_lock, ensure_ascii=False, indent=4))
# --------------------------------------------------------------

# commands -----------------------------------------------------
def help() -> None: # function with help messages
    print("echo Hello, I'm scd")
    print("echo What I can do:")
    print("echo `scd {path}` — same as `cd {path}`")
    print("echo `scd init` — init config file")
    print("echo `scd {list name}` — show some list")
    print("echo `scd from {list name} {index}` — go from some list")
    print("echo `scd bind {key} {path}` — bind some path")
    print("echo `scd save {path}` — save some path")


def binded() -> None: # function for showing binded
    show('binded')

def saved() -> None: # function for showing saved
    show('saved')

def recent() -> None: # function for showing recent
    show('recent')


def clear_binded() -> None: # function for clearing binded
    clear('binded')

def clear_saved() -> None: # function for clearing saved
    clear('saved')

def clear_recent() -> None: # function for clearing recent
    clear('recent')


def from_binded(index: int) -> None: # function for changing directory from binded
    binded_dict: dict = get('binded')
    print(f"cd {binded_dict[list(binded_dict.keys())[index - 1]]}")

def from_saved(index: int) -> None: # function for changing directory from saved
    saved_list: list = get('saved')
    print(f"cd {saved_list[index - 1]}")

def from_recent(index: int) -> None: # function for changing directory from recent
    recent_list: list = get('recent')
    print(f"cd {recent_list[index - 1]}")


def delete_binded(index: int) -> None: # function for deleting some path from binded
    binded_dict: dict = get('binded')
    delete('binded', list(binded_dict.keys())[index - 1])

def delete_saved(index: int) -> None: # function for deleting some path from saved
    saved_list: list = get('saved')
    delete('saved', index - 1)

def delete_recent(index: int) -> None: # function for deleting some path from recent
    recent_list: list = get('recent')
    delete('recent', index - 1)


def bind(key: str, path: str) -> None: # function for binding some path
    add('binded', path, key)

def save(path: str) -> None: # function for saving some path
    add('saved', path)
# --------------------------------------------------------------

# main ---------------------------------------------------------
def main() -> None: # main function
    match len(sys.argv):
        case 1:  #'scd'
            print(f"echo {CALL_PATH}")
        case 2:
            match sys.argv[1]:
                case "init" | "clear": # 'scd init' | 'scd clear'
                    init()
                case "help": # 'scd help'
                    help()
                case "binded": # 'scd binded'
                    binded()
                case "saved": # 'scd saved'
                    saved()
                case "recent": # 'scd recent'
                    recent()
                case _:
                    binded_dict: dict = get('binded')
                    if sys.argv[1] in list(binded_dict.keys()):
                        print(f"cd {binded_dict[sys.argv[1]]}")
                    else:
                        add('recent', os.path.abspath(sys.argv[1]))
                        print(f"cd {os.path.abspath(sys.argv[1])}")
        case 3:
            match sys.argv[1]:
                case "clear":
                    match sys.argv[2]:
                        case "binded": # 'scd clear binded'
                            clear_binded()
                        case "saved": # 'scd clear saved'
                            clear_saved()
                        case "recent": # 'scd clear recent'
                            clear_recent()
                case "save": # 'scd save %path%'
                    save(os.path.abspath(sys.argv[2]))
                case _:
                    print("echo Uncorrect arguments")
        case 4:
            match sys.argv[1]:
                case "from":
                    match sys.argv[2]:
                        case "binded": # 'scd from binded %index%'
                            from_binded(int(sys.argv[3]))
                        case "saved": # 'scd from saved %index%'
                            from_saved(int(sys.argv[3]))
                        case "recent": # 'scd from recent %index%'
                            from_recent(int(sys.argv[3]))
                case "delete":
                    match sys.argv[2]:
                        case "binded": # 'scd delete binded %index%'
                            delete_binded(int(sys.argv[3]))
                        case "saved": # 'scd delete saved %index%'
                            delete_saved(int(sys.argv[3]))
                        case "recent": # 'scd delete recent %index%'
                            delete_recent(int(sys.argv[3]))
                case "bind": # 'scd bind %key% %path%'
                    bind(sys.argv[2], os.path.abspath(sys.argv[3]))
                case _:
                    print("echo Uncorrect arguments")
        case _:
            print("echo Uncorrect arguments")

if __name__ == "__main__":
    main() # run main
# --------------------------------------------------------------