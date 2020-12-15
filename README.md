
    baseurl = 'http://localhost:32400'
    token = 'plexToken'
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


libMaxCallCount와 실행 시간을 잘 지정해주는 것이 중요.

ex : 캐쉬 전부 remove한 후 실행한다거나 재부팅 후 실행.
