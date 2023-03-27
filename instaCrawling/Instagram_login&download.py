from fileinput import filename

import requests
from matplotlib import pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os 
import time

import cv2

# haarcascade 불러오기
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

headers = \
        {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}


chrome = '/Users/hoseheon/Desktop/python_study/chromedriver'
browser = webdriver.Chrome(executable_path=chrome)

# Instagram ID & PW
ID = ''
PW = ''

url = 'https://www.instagram.com/accounts/login/'
browser.get(url)
browser.implicitly_wait(3)


e = browser.find_element(By.NAME, 'username')
e.clear()
e.send_keys(ID)

e = browser.find_element(By.NAME, 'password')
e.clear()
e.send_keys(PW)
# time.sleep(5)
e.send_keys(Keys.ENTER)
# time.sleep(5)

browser.implicitly_wait(5) # 페이지 넘어갈 때마다 해주기

browser.find_element(By.CLASS_NAME, '_acan._acao._acas').click() # 클릭할 곳 class name으로 찾아 더블클릭
browser.find_element(By.CLASS_NAME, '_a9--._a9_1').click() # 중간에 있는 띄어쓰기에만 . 붙임

# browser.find_element(By.CLASS_NAME, '_ab6-').click() # 돋보기 모양
browser.find_element(By.CLASS_NAME, '_aaw9').click() # 검색창 한 번 클릭하고

s = browser.find_element(By.CLASS_NAME, '_aauy') # 찾아서 send
s.send_keys('#셀카')
s.send_keys(Keys.ENTER)
s.send_keys(Keys.ENTER)

browser.implicitly_wait(5)

# 이미지 폴더 생성
img_folder = './instagram_imgs'
if not os.path.isdir(img_folder) : # 없으면 새로 생성하는 조건문
    os.mkdir(img_folder)


imgUrls = set([])
for j in range(1,4):
    tag = browser.find_elements(By.CLASS_NAME, '_aagv') # _aagv tag
    for i in tag:
        img = i.find_element(By.TAG_NAME, 'img') # img tag
        imgUrl = img.get_attribute('src') # 해당 tag 내 attribute 접근
        print(imgUrl)
        imgUrls.add(imgUrl)
        print('='*60)

    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(5)

try:
    p = 1
    for k in imgUrls:
        # img 다운로드 부분
        file_name = f'./instagram_imgs/{p}.jpg'
        file = open(file_name, 'wb')
        site = requests.get(k, headers=headers)
        file.write(site.content)
        file.close()
        p = p + 1
except Exception as e:
    print('에러', e)


k = 1
# p = 1
faceImgs = set([])
for x in range(1, len(imgUrls)):

    # 이미지 불러오기
    rImg = cv2.imread(f'./instagram_imgs/{x}.jpg') # 불러온 이미지
    gray = cv2.cvtColor(rImg, cv2.COLOR_BGR2GRAY)

    # 얼굴 찾기
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(150, 150))

    # detectMultiScale(img, scaleFactor, minNeighbors)
    # img: 인식할 영상
    # scaleFactor: 이미지 확대 크기 제한, 1.3~1.5 (큰값: 인식기회 증가, 속도 감소)
    # minNeighbors: 요구되는 이웃 수(큰값: 품질증가, 검출개수 감소)

    # 이미지 폴더 생성
    img_folder = './instagram_faceImgs'
    if not os.path.isdir(img_folder):  # 없으면 새로 생성하는 조건문
        os.mkdir(img_folder)

    try:
        for (x, y, w, h) in faces: # faces에 값이 없으면 NON. python은 NULL 없음. 값이 비어 있는 경우 NULL, 포인터가 비어 있는 경우 NON
            cv2.rectangle(rImg, (x, y), (x + w, y + h), (255, 0, 0), 2)
            faceImg = rImg[y:y+h, x:x+w]
            faceImg = cv2.resize(faceImg, (150, 150))
            # 추출된 얼굴 보여주기
            # for p in faces:
            # cv2.imshow('faceImg', faceImg)
            # key = cv2.waitKey(0)
            # cv2.destroyAllWindows()
            cv2.imwrite(f'./instagram_faceImgs/{k}.jpg', faceImg)
            faceImgs.add(faceImg)
            # p = p+1
    except Exception as e:
        print('에러', e)
    k = k + 1
    # 이미지 창 이동
    winname = "image"
    cv2.namedWindow(winname)
    cv2.moveWindow(winname, 200, 50)
    # 영상 출력
    cv2.imshow(winname, rImg)
    # cv2.imshow('faceImg', rImg[150:250, 150:250])

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

# myImg = cv2.imread('./myImg.jpg')
# for i in range(1, len(faceImgs)):
#     try:
#         # 이미지 불러오기
#         readFaceImg = cv2.imread(f'./instagram_faceImgs/{i}.jpg')  # 불러온 이미지
#
#     except Exception as e:
#         print("에러", e)

# img1 = cv2.imread('./myImg.jpg')
# img2 = cv2.imread('./instagram_faceImgs/1.jpg')

