import click, os, eyed3, shutil, path


@click.command()
@click.option('--s', '--src-dir', default='./', help='Папка с файлами для сортировки')
@click.option('--d', '--dst-dir', default='./', help='Папка с результатом')
def sort(s, d):
    while not os.path.exists(s):
        s = input("Папка с файлами не существует. Введите другую: ")
    while not os.path.exists(d):
        d = input("Папка для результата не существует. Введите другую: ")

    files = os.listdir(path=s)
    if len(files) == 0:
        print("Â ïàïêå íåò mp3-ôàéëîâ")
    for file in files:
        path_file = os.path.join(s, file)
        new_path_file = ""
        if os.path.splitext(file)[1].lower() != ".mp3":
            # print(path_file, " -> ôàéë íå mp3")
            continue
        audiofile = eyed3.load(path_file)
        if audiofile.tag:
            artist = audiofile.tag.artist
            album = audiofile.tag.album
            title = audiofile.tag.title
        if artist and album:
            if title:
                file_name = f'{title} - {artist} - {album}.mp3'
                file_name = cor_names(file_name)
                new_path_file = os.path.join(d, cor_names(artist), cor_names(album))
                if not os.path.exists(new_path_file):
                    try:
                        os.makedirs(new_path_file)
                    except PermissionError as e:
                        print(str(e))
                try:
                    shutil.move(path_file, os.path.join(new_path_file, file_name))
                except PermissionError as e:
                    print(str(e))
                print(path_file, " -> ", new_path_file)


def cor_names(text):
    text = text.encode("cp1252").decode("cp1251")
    symbols = '\/?:*"><|'
    for symbol in symbols:
        if symbol in text:
            text = text.replace(symbol, '')
    return text


if __name__ == "__main__":
    sort()
