import requests, sys, os, shutil, urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

websiteLink = r"https://jbzd.com.pl/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
allowedSubPages = ['', 'str','oczekujace']
currentPath = os.path.dirname(os.path.realpath(__file__))
charsToReplace = {":": '-', "*": '-', "?": '-',"!": '-', " ": '-'}
for subPage in allowedSubPages:
    if subPage != "":
        newFolderPath = os.path.join(currentPath, subPage)
        if not os.path.exists(newFolderPath):
            os.mkdir(newFolderPath)

def downloadMeme(link, folder, title):
    currentTime = str(datetime.now())
    title = title + currentTime+ ".png"
    title = ''.join(charsToReplace.get(x, x) for x in title)
    folder = os.path.join(currentPath,folder, title)
    try:
        r = requests.get(link, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(folder,'wb') as f:
                shutil.copyfileobj(r.raw, f)
            
                print('Image sucessfully Downloaded: ',title)
        else:
            print('Image Couldn\'t be retreived')
    except Exception as e:
        print('Nieoczekiwany błąd podczas próby pobrania', title)

def downloadVideo(link, folder, title):
    currentTime = str(datetime.now())
    title = title + currentTime+ ".mp4"
    title = ''.join(charsToReplace.get(x, x) for x in title)
    folder = os.path.join(currentPath,folder, title)
    try:
        r = requests.get(link, stream = True)
        if r.status_code == 200:
            with open(folder,'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)
            
                print('Video sucessfully Downloaded: ',title)
        else:
            print('Video Couldn\'t be retreived')
    except Exception as e:
        print('Nieoczekiwany błąd podczas próby pobrania', title)


def downloadContent(amount, subPage):
    for i in range(1, int(amount)):
        currentSite = requests.get('{}{}/{}'.format(websiteLink, subPage, i), headers=headers)
        currentSite = BeautifulSoup(currentSite.text, 'html.parser')
        mainElement = currentSite.find("main", class_="main").find("section", id="content-container")
        memeContainers = mainElement.findAll("div", class_="article-image article-media-image")
        videoContainers = mainElement.findAll("div", class_="video-player")
        print("-"*10, "IMAGES FROM PAGE " + str(i), "-"*10)
        for memeContainer in memeContainers:
            memeLink = memeContainer.a.img["src"]
            memeTitle = memeContainer.a.img["alt"]
            downloadMeme(memeLink, subPage, memeTitle)
        if videoContainers:
            print("-"*10, "VIDEOS FROM PAGE " + str(i), "-"*10)
            for videoContainer in videoContainers:
                videoLink = videoContainer.videoplyr["video_url"]
                downloadVideo(videoLink, subPage, '')
    




def main():
    sitesAmount = input("Podaj ilość stron z których chcesz pobrać obrazki: ")
    if not sitesAmount.isnumeric(): sys.exit('Wartość musi być numerem!')
    if sitesAmount == 0: sys.exit("Minimalna liczba stron do pobrania musi wynosić 1!")
    subPage = input("Podaj nazwę podstrony z której chcesz pobrać obrazki (lub zostaw puste jezeli chcesz pobrać z głównej): ").casefold()
    if not subPage in allowedSubPages:
        print('Podano nieprawidłową podstronę, dozwolone podstrony: ')
        for subPage in allowedSubPages:
            if subPage != "":
                print('-', subPage)
        sys.exit()
    try:
        downloadContent(sitesAmount == "0" and "1" or sitesAmount, subPage == "" and 'str' or subPage)
    except Exception as e: 
        print(e)
        sys.exit('Nastąpił nieoczekiwany błąd')

if __name__ == "__main__":
    main()