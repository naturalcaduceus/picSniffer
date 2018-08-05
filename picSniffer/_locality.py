import cv2  
import numpy as np  
  
def drawMatchesKnn_cv2(img1_gray,kp1,img2_gray,kp2,goodMatch):  
    try:
        h1, w1 = img1_gray.shape[:2]  
        h2, w2 = img2_gray.shape[:2]  
  
        vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)  
        vis[:h1, :w1] = img1_gray  
        vis[:h2, w1:w1 + w2] = img2_gray                    #有未知错误
  
        p1 = [kpp.queryIdx for kpp in goodMatch]  
        p2 = [kpp.trainIdx for kpp in goodMatch]  
  
        post1 = np.int32([kp1[pp].pt for pp in p1])  
        post2 = np.int32([kp2[pp].pt for pp in p2]) + (w1, 0)  
        #print('是')
        return 1
    except:     #触发无匹配异常时
        #print('不是')
        return 0

    #for (x1, y1), (x2, y2) in zip(post1, post2):  
    #    cv2.line(vis, (x1, y1), (x2, y2), (0,0,255))  
  
    #cv2.namedWindow("match",cv2.WINDOW_NORMAL)  
    #cv2.imshow("match", vis)  
  

def cv_imread(filePath):  
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)  
    ##imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化  
    ##cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)  #转成bgr
    return cv_img  



def classify_locality(img1,img2):

    #img1=r'E:\1projects\毕业设计-嗅图狗\pictures\局部识图测试\3.jpg'
    #img2=r'D:\_CODE\tf\2.jpg'

    img1_gray = cv_imread(img1)
    img2_gray = cv_imread(img2)
    #img2_gray = cv2.imread(r'D:\_CODE\tf\2.jpg')
  
    sift = cv2.xfeatures2d.SIFT_create()
    #sift = cv2.SIFT()  
    #sift = cv2.SURF()  
  
    kp1, des1 = sift.detectAndCompute(img1_gray, None)  
    kp2, des2 = sift.detectAndCompute(img2_gray, None)  
  
    # BFmatcher with default parms  
    bf = cv2.BFMatcher(cv2.NORM_L2)  
    try:
        matches = bf.knnMatch(des1, des2, k = 2)                #有未知错误
    except:
        return 0
    else:
        goodMatch = []  
        for m,n in matches:  
            if m.distance < 0.50*n.distance:  
                goodMatch.append(m)  
  
        return drawMatchesKnn_cv2(img1_gray,kp1,img2_gray,kp2,goodMatch[:20])  #画得出20个相似点就允许
  
        #cv2.waitKey(0)  
        #cv2.destroyAllWindows()