# BFMatcher와 ORB로 매칭 (match_bf_orb.py)
import cv2
img1 = cv2.imread('./cmp_Img/myImg.jpg')
for i in range(1, 200):
    try:
        img2 = cv2.imread(f'./instagram_faceImgs/{i}.jpg')
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # SIFT 서술자 추출기 생성 ---①
        detector = cv2.ORB_create()
        # 각 영상에 대해 키 포인트와 서술자 추출 ---②
        kp1, desc1 = detector.detectAndCompute(gray1, None)
        kp2, desc2 = detector.detectAndCompute(gray2, None)

        # BFMatcher 생성, Hamming 거리, 상호 체크 ---③
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # 매칭 계산 ---④
        matches = matcher.match(desc1, desc2)
        # 매칭 결과 그리기 ---⑤
        res = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, \
                             flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

        cv2.imshow('BFMatcher + ORB', res)
        cv2.waitKey()
        cv2.destroyAllWindows()

    except Exception as e:
        print('에러', e)
