import requests
from requests.exceptions import ReadTimeout
import time
import xmltodict
import os
from sqlitedict import SqliteDict

baseurl = 'http://localhost:32400'
token = 'EDLzhCqbEjXvwQuziiCz'
intervalTime = 3600 * 24 # 24시간마다
fragmentTime = 20 # 앞부분 몇 초를 잘라서 다운받을지
cacheDir = "cache" # 캐시폴더 디렉토리. 블랭크면 현재위치

###

directoryMapping = {
    '/mnt/g2/test/koreaDrama' : '/mnt/total/koreaDrama',
    '/mnt/exam1/2222' : '/test/test/test'
}

###

blacklistLib = ['영화2222' , '영화3333']    # 해당 리스트에 등록되어 있는 리스트는 전부 무시한다
whitelistLib = []                # 이 리스트가 1개 이상 보유하고 있다면, 이 리스트에 들어있는 원소를 제외하고 전부 무시한다.
libMaxCallCount = 30                      # 라이브러리마다 불러들일 컨텐츠 수, 최대 100개. 너무 많으면 다운받는 데에 시간이 오래걸릴 수 있음. 차차 조정 바람.

def processFFMPEG(mediaPath , nextEpisodeVideo):
    if not os.path.exists(mediaPath) : return
    if not cacheDir :
        rootPath = os.getcwd()
    else:
        rootPath = cacheDir
    output = os.path.join(rootPath , os.path.split(mediaPath)[-1])
    if os.path.exists(output) :
        return
    # mediaPath 처리
    for path in directoryMapping:
        if path in mediaPath:
            mediaPath = mediaPath.replace(path , directoryMapping[path])
    # analyze도 한다
    #t2 = requests.put(url=baseurl + nextEpisodeVideo['@key']  + '/refresh?X-Plex-Token=' + token)
    command = 'ffmpeg -i "' + mediaPath + '" -ss 0 -t ' + str(fragmentTime) + ' -vcodec copy -acodec copy  -y "' + str(output) + '"'
    os.system(command)
    t1 = requests.put(url=baseurl + nextEpisodeVideo['@key'] + '/analyze?X-Plex-Token=' + token , timeout=10)
    print(t1)

def start():
    res = requests.get(baseurl + '/library/sections?X-Plex-Token=' + token)
    xml = xmltodict.parse(res.text)['MediaContainer']
    dirs = xml['Directory']
    for dir in dirs:
        if whitelistLib and dir['@title'] not in whitelistLib : continue
        if dir['@title'] in blacklistLib: continue

        libCount = 0
        res = requests.get(baseurl + '/library/sections/'+str(dir['@key'])+'/recentlyAdded?X-Plex-Token=' + token)
        xml = xmltodict.parse(res.text)['MediaContainer']
        for content in xml['Video']:
            if isinstance(content['Media'], list):
                tarVidPaths = [item['Part']['@file'] for item in content['Media']]
            else:
                try:
                    if isinstance(content['Media']['Part'] , dict):
                        tarVidPaths = [content['Media']['Part']['@file']]
                    elif isinstance(content['Media']['Part'] , list):
                        tarVidPaths = [item['@file'] for item in content['Media']['Part'] ] # CD1 CD2
                except:
                    continue
            for tarVidPath in tarVidPaths:
                try:
                    processFFMPEG(tarVidPath , nextEpisodeVideo=content)
                except ReadTimeout:
                    continue
                except Exception as e:
                    continue
            libCount += 1
            if libCount >= libMaxCallCount :
                break # 한계 초과


if __name__ == '__main__':
    while True:
        start()
        time.sleep(intervalTime)
