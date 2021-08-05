# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 15:47:16 2021

@author: ttyy4
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QPushButton, QVBoxLayout,  QLabel, QMessageBox, QLineEdit, QInputDialog, QTextEdit
from PyQt5.QtGui import QIcon

from xy_addr import coordinate, xy_addr
from road_lot import road_region, region_road

import os

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowIcon(QIcon('icon/main.qrc'))
        self.statusBar().showMessage('버전1.0 다음 업데이트 날짜:미정')
        
        exitAction = QAction(QIcon('icon/exit.qrc'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)
        
        
        
        #좌표를 주소로 변화는 라벨 버튼
        btn1 = QPushButton('&검색시작', self)
        btn1.setCheckable(True)
        btn1.move(320,100)
        btn1.resize(100, 30)
        btn1.clicked.connect(self.xy_addr_result)
        
        label1 = QLabel('좌표를 주소로 변환', self)
        label1.move(60, 70)
        label1.resize(150, 40)


        self.xlabel = QLabel('x:', self)
        self.xlabel.move(65,100)
        
        self.xle = QLineEdit(self)
        self.xle.move(80, 100)
        self.xle.resize(100, 30)
        
        
        self.ylabel = QLabel('y:', self)
        self.ylabel.move(185,100)
        self.yle = QLineEdit(self)
        self.yle.move(210, 100)
        self.yle.resize(100, 30)
        

#주소를 좌표로 
        btn2 = QPushButton(self)
        btn2.setText('Button&2')
        btn2.move(80,200)
        btn2.clicked.connect(self.showDialog)
        
        label2 = QLabel('주소를 좌표로 변환', self)
        label2.move(60, 170)
        label2.resize(150, 40)

        
#지번 주소를 도로명 주소로
        self.btn3label = QLabel('지번 주소 -> 도로명 주소', self)
        self.btn3label.move(280,170)
        self.btn3label.resize(200, 40)

        self.btn3 = QPushButton(self)
        self.btn3.setText('주소 입력') 
        self.btn3.move(300, 200)
        self.btn3.clicked.connect(self.region_road_result)
        
        
#도로명 주소를 지번 주소로

        self.btn4label = QLabel('도로명 주소 -> 지번 주소', self)
        self.btn4label.move(500,170)
        self.btn4label.resize(200, 40)
        
        self.btn4 = QPushButton(self)
        self.btn4.setText('주소 입력') 
        self.btn4.move(520, 200)
        self.btn4.clicked.connect(self.road_region_result)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(self.xle)
        vbox.addWidget(self.yle)

        label3 = QLabel('결과창', self)
        label3.move(80, 270)
        
        self.le = QTextEdit(self)#QLineEdit(self)
        self.le.move(80, 300)
        self.le.resize(500, 100)
        
        self.lbl1 = QLabel('결과:', self)
        self.lbl1.move(80, 420)
        self.lbl1.resize(400, 30)
        vbox.addWidget(self.lbl1)
        
        
        self.setLayout(vbox)
        self.setWindowTitle('GIS 변환 프로그램')
        self.setGeometry(300, 700, 800, 500)
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
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    os.system('pause')