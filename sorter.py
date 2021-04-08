# -*- coding: CP1251 -*-

import click, os, eyed3, shutil, path


@click.command()
@click.option('--s', '--src-dir', default='C:/Users/bogdanova_dv/Downloads/�������� ������',
              help='����� � ������� ��� ����������')
@click.option('--d', '--dst-dir', default='C:/Users/bogdanova_dv/Downloads/�������� ������',
              help='����� � �����������')
def sort(s, d):
    while not os.path.exists(s):
        s = input("����� � ������� �� ����������. ������� ������: ")
    while not os.path.exists(d):
        d = input("����� ��� ���������� �� ����������. ������� ������: ")

    files = os.listdir(path=s)
    if len(files) == 0:
        print("� ����� ��� mp3-������")
    for file in files:
        path_file = os.path.join(s, file)
        new_path_file = ""
        if os.path.splitext(file)[1].lower() != ".mp3":
            # print(path_file, " -> ���� �� mp3")
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