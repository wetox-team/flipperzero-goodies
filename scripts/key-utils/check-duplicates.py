from collections import defaultdict
from pathlib import Path


KEYS_DIR = Path(__file__).parent.parent.parent / 'intercom-keys'
KEYS = defaultdict(list)


class KeyTypes:
    ibtn = 'ibutton'
    rfid = 'lfrfid'
    nfc = 'nfc'


def parse_data(file_path: Path, key_type: str):
    key_word = 'UID' if key_type == KeyTypes.nfc else 'Data'

    with file_path.open() as file:
        key_data = file.read()

    if key_word not in key_data:
        return ''

    start_index = key_data.index(f'{key_word}: ') + len(key_word) + 2
    end_index = len(key_data)
    if '\n' in key_data[start_index + 1:]:
        end_index = start_index + key_data[start_index + 1:].index('\n')

    return key_data[start_index:end_index]


def handle_keys(dir_path, key_type):
    for file in (dir_path / key_type).iterdir():
        if not file.is_file() or file.name == '.gitkeep':
            continue

        data = parse_data(file, key_type).replace(' ', '').strip()
        if not data:
            continue

        KEYS[f'{key_type}:{data}'].append(file)


def check_duplicates():
    for city_dir in KEYS_DIR.iterdir():
        if not city_dir.is_dir():
            continue

        keys_dir = city_dir / 'keys'
        handle_keys(keys_dir, KeyTypes.ibtn)
        handle_keys(keys_dir, KeyTypes.rfid)
        handle_keys(keys_dir, KeyTypes.nfc)


def main():
    global KEYS

    print('\nCHECK FOR DUPLICATE KEYS:\n')

    KEYS.clear()
    check_duplicates()

    result = '\n'.join(
        (f'{k}:\n\t' + '\n\t'.join(f.as_posix() for f in v))
        for k, v in KEYS.items() if len(v) > 1
    )

    if not result:
        print('no duplicates')
    else:
        print(result)


if __name__ == '__main__':
    main()
