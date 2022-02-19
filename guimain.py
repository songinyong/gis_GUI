# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 15:47:16 2021

@author: ttyy4

-----8/5----
지금까지 만든 카카오 api 기반으로 만든 
wgs84 좌표 <-> 주소 변경 api

지번 주소 <-> 도로명 주소 

변환 모듈들을 gui로 동작하게 만듬
GUI는 프로그래밍은 pyQt로 만듬


파일 부분 gui는 코드가 길어져 별개 파일로 만들었음 
 
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt 
from xy_addr import coordinate, xy_addr
from road_lot import road_region, region_road
import second_window


#메인 화면 클래스
class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowIcon(QIcon('icon/main.qrc'))
        self.statusBar().showMessage('버전0.2.1 업데이트내역: 서브창 안꺼지는 오류 해결')
        
        exitAction = QAction(QIcon('icon/exit.qrc'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)


        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)
        
        self.description = QLabel('*도로명 주소 -> 지번주소의 경우 일부 구간 검색에 오류가 발생하여 조치중입니다', self)
        self.description.move(80,50)
        self.description.resize(500, 30)
        #좌표를 주소로 변환 기능
        btn1 = QPushButton('&검색', self)
        btn1.setCheckable(True)
        btn1.move(340,150)
        btn1.resize(80, 30)
        btn1.clicked.connect(self.xy_addr_result)
        
        btn1f = QPushButton('&파일변환', self)
        btn1f.setCheckable(True)
        btn1f.move(420,150)
        btn1f.resize(80, 30)
        btn1f.clicked.connect(self.second_window)
        
        label1 = QLabel('좌표를 주소로 변환', self)
        label1.move(100, 120)
        label1.resize(150, 40)

        self.xlabel = QLabel('x:', self)
        self.xlabel.move(80,150)
        
        self.xle = QLineEdit(self)
        self.xle.move(100, 150)
        self.xle.resize(100, 30)
             
        self.ylabel = QLabel('y:', self)
        self.ylabel.move(210,150)
        self.yle = QLineEdit(self)
        self.yle.move(230, 150)
        self.yle.resize(100, 30)
        
        #좌표를 주소로 변환 기능 END
        

        #주소를 좌표로 변환 기능
        label2 = QLabel('주소를 좌표로 변환', self)
        label2.move(90, 220)
        label2.resize(150, 40)

        btn2 = QPushButton(self)
        btn2.setText('주소 입력')
        btn2.move(80,250)
        btn2.resize(80, 30)
        btn2.clicked.connect(self.showDialog)
        
        
        btn2f = QPushButton('&파일변환', self)
        btn2f.setCheckable(True)
        btn2f.move(160,250)
        btn2f.resize(80, 30)
        btn2f.clicked.connect(self.frAddr_xy_window)
        

        #주소를 좌표로 변환 기능 END
        
        #지번 주소를 도로명 주소로 변환 기능
        self.btn3label = QLabel('지번 주소 -> 도로명 주소', self)
        self.btn3label.move(280,220)
        self.btn3label.resize(200, 40)

        self.btn3 = QPushButton(self)
        self.btn3.setText('주소 입력') 
        self.btn3.move(280, 250)
        self.btn3.resize(80, 30)
        self.btn3.clicked.connect(self.region_road_result)
        
        self.btn3f = QPushButton(self)
        self.btn3f.setText('파일변환') 
        self.btn3f.move(360, 250)
        self.btn3f.resize(80, 30)
        self.btn3f.clicked.connect(self.frRegion_road_window)
        #지번 주소를 도로명 주소로 변환 기능 END
        

        #도로명 주소를 지번 주소로 변환 기능
        self.btn4label = QLabel('도로명 주소 -> 지번 주소', self)
        self.btn4label.move(480,220)
        self.btn4label.resize(200, 40)
        
        self.btn4 = QPushButton(self)
        self.btn4.setText('주소 입력') 
        self.btn4.move(480, 250)
        self.btn4.resize(80, 30)
        self.btn4.clicked.connect(self.road_region_result)
        
        self.btn4f = QPushButton(self)
        self.btn4f.setText('파일변환') 
        self.btn4f.move(560, 250)
        self.btn4f.resize(80, 30)
        self.btn4f.clicked.connect(self.frRoad_region_window)
        #도로명 주소를 지번 주소로 변환 기능 END

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(self.xle)
        vbox.addWidget(self.yle)

        #하단 결과 박스
        label3 = QLabel('결과창', self)
        label3.move(80, 320)
        
        self.le = QTextEdit(self)#QLineEdit(self)
        self.le.move(80, 350)
        self.le.resize(560, 100)
        
        self.lbl1 = QLabel('결과:', self)
        self.lbl1.move(80, 470)
        self.lbl1.resize(400, 30)
        vbox.addWidget(self.lbl1)
        #하단 결과 박스
              
        #메인 화면 생성 부분
        self.setLayout(vbox)
        self.setWindowTitle('GIS 변환 프로그램')
        self.setGeometry(300, 300, 720, 550)
        self.show()

        
    def region_road_result(self):
        text, ok = QInputDialog.getText(self, '지번를 도로명으로', '지번주소 입력:')
        
        if ok:
            reg = region_road(str(text))
            
            if reg is None or reg == 'non':
                self.lbl1.setText('결과: ' + "입력하신 지번 주소가 맞는지 확인해 주십시오")
                
                
            elif reg != 'non' and reg == str(text):
                self.lbl1.setText('결과: ' + "도로명 주소를 찾을 수 없음")
                
            else :
                self.le.setText(reg)
                self.lbl1.setText('결과: ' + "검색성공")
                
        else :
            self.lbl1.setText('결과: ' + "검색실패")
               
    def road_region_result(self):
        text, ok = QInputDialog.getText(self, '도로명을 지번주소로', '도로명주소 입력:')
        
        if ok:
            
            reg = road_region(str(text))
            
            if reg is not None :
                self.le.setText(reg)
                self.lbl1.setText('결과: ' + "검색성공")
            
            else :
                self.lbl1.setText('결과: ' + "주소를 찾을 수 없음")
        
    def xy_addr_result(self):
        x = self.xle.text()
        y = self.yle.text()
        
        result = xy_addr(x, y)
        
        if result is None :
            self.lbl1.setText('결과: ' + '주소를 검색할 수 없음')
            
            
        elif len(result) <2:
            self.le.setText('지번주소:'+result[0])
            self.lbl1.setText('결과: ' + '도로명 주소 구할 수 없음')
                
        else :
        
            self.le.setText('도로명주소:'+result[0]+'\n지번주소:'+result[1])
            
    def showDialog(self):
        text, ok = QInputDialog.getText(self, '주소 -> 위도경도', '주소 입력:')

        if ok :
            ten = coordinate(str(text))
                    
            status = '검색 성공'
            if ten is not None :
                result = '주소:'+ ten[0]+ ' x:'+ten[1]+' y:'+ten[2]
                self.le.setText(result)
                self.lbl1.setText('결과: ' + status)
            else :
                self.lbl1.setText('결과: 주소 검색을 진행할 수 없음' )
     
    #두번째 창 생성 부분
    def second_window(self):
        self.window_2 = second_window.frXy_addr()
                 
    def frAddr_xy_window(self):
        self.window_2 = second_window.frAddr_xy()
          
    def frRoad_region_window(self):
        self.window_2 = second_window.frRoad_region()
                
    def frRegion_road_window(self):
        self.window_2 = second_window.frRegion_road()
              
    def closeEvent(self, event):
        self.window_2.close()    
        
     #두번째 창 생성 부분 END
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    