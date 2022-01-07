import requests
import argparse
from bs4 import BeautifulSoup
import subprocess
import json

FILE_NAME = "manga_hst.json"


def append_history(line):
    with open(FILE_NAME, 'w') as file:
        file.write(line)

def get_input():
    manga = input("Enter the name of the manga: ").replace(" " ,"-")
    url = input("Enter the url(https://some-url/some/endpoint/{chapternumber}): ")
    chapter = input("Enter the chapter number: ")
    jsn = { 'name': manga,
           'url' : url,
           'chapter' : chapter}
    history.append(jsn)
    append_history(json.dumps(history))


######################################
#     Creating History File          #
######################################
ret = subprocess.run("ls", capture_output=True)

if FILE_NAME not in ret.stdout.decode():
    f = open(FILE_NAME, 'w')
    f.write("[]")
    f.close()


######################################
#       Parsing Argument             #
######################################

parser = argparse.ArgumentParser(description='Read Manga From Terminal.')
parser.add_argument('-S', help='Search Manga by name')
parser.add_argument('-H', help="Show History", action="store_true")
parser.add_argument('-N', help="Start New Manga", action="store_true")

args = parser.parse_args()

f = open(FILE_NAME)
global history
try:
    history = json.load(f)
except:
    get_input()

def construct_url(manga):
    ini = manga['url']
    return ini[:ini.index('{')]+manga['chapter']+ini[ini.index('}')+1:]

def attribute_finder(image):
    img_types = ['.png', '.jpg', '.jpeg']
    for attr in image.keys():
        for typ in img_types:
            if typ in image[attr]:
                return attr
    return None


def update_chapter(index,ofset=1):
    global history
    history[index]['chapter'] = str(int(history[index]['chapter'])+ofset)
    append_history(json.dumps(history))


def get_chapter(index):
    manga = history[index]
    url = construct_url(manga)
    print(url)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    chapterList =  []
    for image in soup.find_all('img'):
        attribute = attribute_finder(image.attrs)
        src = image.get(attribute)
        if src:
            if 'https:' not in src:
                chapterList.append('https:'+src.strip(' \n'))
            else:
                chapterList.append(src.strip(' \n\t'))
        else:
            print("Error")
    if len(chapterList) < 10:
        inp = input("The New Chapter isn't out yet\n Go to prev chapter [y/n]?")
        if 'y' in inp.lower():
            update_chapter(index,ofset=-1)
            get_chapter(index)
        else:
            quit()
    subprocess.run("pkill feh", shell=True)
    subprocess.Popen("feh -q --reload int --title "+manga['name']+" ".join(chapterList),shell=True)
    print("##################################################################")
    next = input("Next? [y/n]: ")
    if 'y' in next.lower():
        update_chapter(index)
        get_chapter(index)
    else:
        quit()

def show_history():
    print("History:")
    for n,jsn in enumerate(history):
        print(f"[{n+1}] {jsn['name']}")
    manga = int(input("Choose the manga: ")) -1
    get_chapter(manga)

if args.H:
    show_history()
elif args.N:
    get_input()

