import click, os, eyed3, shutil, path


@click.command()
@click.option('--s', '--src-dir', default='./',
              help='Папка с файлами для сортировки')
@click.option('--d', '--dst-dir', default='./',
              help='Папка с результатом')
def sort(s, d):
    while not os.path.exists(s) or not os.access(s, os.W_OK):
        s = input("Папка с файлами не существует или нет прав доступа. Введите другую: ")
    while not os.path.exists(d) or not os.access(s, os.W_OK):
        d = input("Папка для результата не существует или нет прав доступа. Введите другую: ")

    files = os.listdir(path=s)
    if len(files) == 0:
        print("Не найдены mp3")
    for file in files:
        path_file = os.path.join(s, file)
        if os.path.splitext(file)[1].lower() != ".mp3":
            continue
        audiofile = eyed3.load(path_file)
        if audiofile.tag:
            artist = audiofile.tag.artist
            album = audiofile.tag.album
            title = audiofile.tag.title
            if artist and album:
                new_path_file = os.path.join(d, cor_names(artist), cor_names(album))
                if not os.path.exists(new_path_file):
                    try:
                        os.makedirs(new_path_file)
                    except OSError as e:
                        print("Не удалось создать папку: ", new_path_file)
                try:
                    shutil.move(path_file, os.path.join(new_path_file, file))
                except shutil.Error as e:
                    print("Не удалось переместить файл: ", file)
                if title:
                    new_name = cor_names(f'{title} - {artist} - {album}.mp3')
                    try:
                        os.rename(os.path.join(new_path_file, file), os.path.join(new_path_file, new_name))
                        file = new_name
                    except OSError as e:
                        print("Не удалось переименовать файл ", file)
                print(path_file, " -> ", os.path.join(new_path_file, file))
                print('Done')


def cor_names(text):
    text = text.encode("cp1252").decode("cp1251")
    symbols = '\/?:*"><|'
    for symbol in symbols:
        if symbol in text:
            text = text.replace(symbol, '')
    return text


if __name__ == "__main__":
    sort()
