# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:22:10 2022

@author: ttyy4
"""
from PyQt5.QtWidgets import *
import pandas as pd
from xy_addr import xy_addr, coordinate
from road_lot import road_region, region_road

#좌표를 주소로 변환
class frXy_addr(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.initUI()
        #self.setWindowModality(Qt.ApplicationModal)
        
    def initUI(self):
        self.btn_file1 = QPushButton('&파일 업로드', self)
        self.btn_file1.setCheckable(True)
        self.btn_file1.move(350, 40)
        self.btn_file1.resize(100, 30)
        self.btn_file1.clicked.connect(self.open)
        
        
        self.btn_file2 = QPushButton('&변환시작', self)
        self.btn_file2.setCheckable(True)
        self.btn_file2.move(60, 340)
        self.btn_file2.resize(100, 30)
        self.btn_file2.clicked.connect(self.funcExec)
        
        
        #x 콤보박스
        self.xCombo = QComboBox(self)
        #콤보박스의 내용이 바뀌는 이벤트 등록
        self.xCombo.currentIndexChanged.connect(self.printXname)
        self.xCombo.move(10, 40)
        
        
        self.xComboLabel = QLabel('x',self)
        self.xComboLabel.move(30, 20)
        self.xComboLabel.resize(10, 20)
        #x 콤보박스 END
        
        
        #y 콤보박스
        self.yCombo = QComboBox(self)
        #콤보박스의 내용이 바뀌는 이벤트 등록
        self.yCombo.currentIndexChanged.connect(self.printYname)
        self.yCombo.move(200, 40)
        
        self.yComboLabel = QLabel('y',self)
        self.yComboLabel.move(230, 20)
        self.yComboLabel.resize(10, 20)
        #y 콤보박스 END


        #진행사항 창
        self.processLabel = QLabel('진행사항',self)
        self.processLabel.move(60, 180)
        self.processLabel.resize(100, 30)
        
        self.process = QTextEdit(self)#QLineEdit(self)
        self.process.move(60, 210)
        self.process.resize(500, 100)
        #진행사항 창 END
        
        vbox = QVBoxLayout()
        self.label = QLabel(self)
        self.label.move(10, 80)
        self.label.resize(500, 30)
        self.setLayout(vbox)
        self.setGeometry(300, 400, 650, 400)
        self.show()
        
        
        # 콤보 박스 선택된 값 
        #self.xCombo.currentText()
    def open(self):
        fname = QFileDialog.getOpenFileName(self)

        self.label.setText(fname[0])
        #test = str(root.filename).strip("(").strip(")").rstrip(",").strip("'")
        #Label(root, text=root.filename).pack()
        
        if(fname[0][-3:] == 'csv'):
            self.childern = pd.read_csv(fname[0])
            for i in self.childern.columns :
                self.xCombo.addItem(i,i)
                self.yCombo.addItem(i,i) 
        elif(fname[0][-4:] == 'xlsx' or fname[0][-3:] == 'xls'):
            self.childern = pd.read_excel(fname[0])
            for i in self.childern.columns :
                self.xCombo.addItem(i,i)
                self.yCombo.addItem(i,i)
        else:
            self.process.append("csv나 xlsx파일을 입력해주시길 바랍니다")
            
 
    #파일 업로드시 콤보박스의 내용에 시트명 출력 
    def printXname(self):
        
        self.process.append("X(경도)컬럼이 선택되었습니다.")
        
    def printYname(self):

        self.process.append("y(위도)컬럼이 선택되었습니다.")

        
    #좌표 변환을 실행
    def funcExec(self) :
        list = []
        
        for i in range(0,len(self.childern)) :
            result = xy_addr(self.childern.iloc[i][self.xCombo.currentText()],self.childern.iloc[i][self.yCombo.currentText()])
            if(result is None):
                self.process.append(str(i+1)+". "+ "결과없음")
            else:
                self.process.append(str(i+1)+". "+ result[0])
            list.append([result, self.childern.iloc[i][self.xCombo.currentText()], self.childern.iloc[i][self.yCombo.currentText()] ])
        df1 = pd.DataFrame(list, columns = ['address_name', 'x', 'y'])
        df1.to_excel("result.xlsx")
        self.process.append("변환 완료")
        
        
#주소를 좌표로 변환
class frAddr_xy(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.initUI()
        #self.setWindowModality(Qt.ApplicationModal)
        
    def initUI(self):
        self.btn_file1 = QPushButton('&파일 업로드', self)
        self.btn_file1.setCheckable(True)
        self.btn_file1.move(300, 40)
        self.btn_file1.resize(100, 30)
        self.btn_file1.clicked.connect(self.open)
        
        
        self.btn_file2 = QPushButton('&변환시작', self)
        self.btn_file2.setCheckable(True)
        self.btn_file2.move(60, 340)
        self.btn_file2.resize(100, 30)
        self.btn_file2.clicked.connect(self.funcExec)
        
        
        #x 콤보박스
        self.addrCombo = QComboBox(self)
        #콤보박스의 내용이 바뀌는 이벤트 등록
        self.addrCombo.currentIndexChanged.connect(self.printAddrname)
        self.addrCombo.move(60, 40)
        
        
        self.addrComboLabel = QLabel('주소',self)
        self.addrComboLabel.move(60, 20)
        self.addrComboLabel.resize(100, 20)
        #x 콤보박스 END
        
        #진행사항 창
        self.processLabel = QLabel('진행사항',self)
        self.processLabel.move(60, 180)
        self.processLabel.resize(100, 30)
        
        self.process = QTextEdit(self)#QLineEdit(self)
        self.process.move(60, 210)
        self.process.resize(500, 100)
        #진행사항 창 END
        
        vbox = QVBoxLayout()
        self.label = QLabel(self)
        self.label.move(10, 80)
        self.label.resize(500, 30)
        self.setLayout(vbox)
        self.setGeometry(300, 400, 650, 400)
        self.show()
        
        
        # 콤보 박스 선택된 값 
        #self.xCombo.currentText()
    def open(self):
        fname = QFileDialog.getOpenFileName(self)

        self.label.setText(fname[0])
        
        if(fname[0][-3:] == 'csv'):
            self.childern = pd.read_csv(fname[0])
            for i in self.childern.columns :
                self.addrCombo.addItem(i,i)

        elif(fname[0][-4:] == 'xlsx' or fname[0][-3:] == 'xls'):
            self.childern = pd.read_excel(fname[0])
            for i in self.childern.columns :
                self.addrCombo.addItem(i,i)
        else:
            self.process.append("csv나 xlsx파일을 입력해주시길 바랍니다")
            
 
    #파일 업로드시 콤보박스의 내용에 시트명 출력 
    def printAddrname(self):       
        self.process.append("주소 컬럼이 선택되었습니다.")
             
    #좌표 변환을 실행
    def funcExec(self) :
        list = []
        
        for i in range(0,len(self.childern)) :
            result = coordinate(self.childern.iloc[i][self.addrCombo.currentText()])
            if(result is None):
                self.process.append(str(i+1)+". "+ "결과없음")
                list.append(['none', '', ''])
            else:
                self.process.append(str(i+1)+". "+ result[0] + "x: "+result[1] + " y:"+result[2])
                list.append(result);
           
        df1 = pd.DataFrame(list, columns = ['address_name', 'x', 'y'])
        df1.to_excel("addr_xy_result.xlsx")
        self.process.append("변환 완료")
        
#도로명 주소를 지번 주소로 변환
class frRoad_region(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.initUI()
        #self.setWindowModality(Qt.ApplicationModal)
        
    def initUI(self):
        self.btn_file1 = QPushButton('&파일 업로드', self)
        self.btn_file1.setCheckable(True)
        self.btn_file1.move(300, 40)
        self.btn_file1.resize(100, 30)
        self.btn_file1.clicked.connect(self.open)
        
        
        self.btn_file2 = QPushButton('&변환시작', self)
        self.btn_file2.setCheckable(True)
        self.btn_file2.move(60, 340)
        self.btn_file2.resize(100, 30)
        self.btn_file2.clicked.connect(self.funcExec)
        
        
        #x 콤보박스
        self.addrCombo = QComboBox(self)
        #콤보박스의 내용이 바뀌는 이벤트 등록
        self.addrCombo.currentIndexChanged.connect(self.printAddrname)
        self.addrCombo.move(60, 40)
        
        
        self.addrComboLabel = QLabel('주소',self)
        self.addrComboLabel.move(60, 20)
        self.addrComboLabel.resize(100, 20)
        #x 콤보박스 END
        
        #진행사항 창
        self.processLabel = QLabel('진행사항',self)
        self.processLabel.move(60, 180)
        self.processLabel.resize(100, 30)
        
        self.process = QTextEdit(self)#QLineEdit(self)
        self.process.move(60, 210)
        self.process.resize(500, 100)
        #진행사항 창 END
        
        vbox = QVBoxLayout()
        self.label = QLabel(self)
        self.label.move(10, 80)
        self.label.resize(500, 30)
        self.setLayout(vbox)
        self.setGeometry(300, 400, 650, 400)
        self.show()
        
        
        # 콤보 박스 선택된 값 
        #self.xCombo.currentText()
    def open(self):
        fname = QFileDialog.getOpenFileName(self)

        self.label.setText(fname[0])
        
        if(fname[0][-3:] == 'csv'):
            self.roadAddress = pd.read_csv(fname[0])
            for i in self.roadAddress.columns :
                self.addrCombo.addItem(i,i)

        elif(fname[0][-4:] == 'xlsx' or fname[0][-3:] == 'xls'):
            self.roadAddress = pd.read_excel(fname[0])
            for i in self.roadAddress.columns :
                self.addrCombo.addItem(i,i)
        else:
            self.process.append("csv나 xlsx파일을 입력해주시길 바랍니다")
            
 
    #파일 업로드시 콤보박스의 내용에 시트명 출력 
    def printAddrname(self):       
        self.process.append("주소 컬럼이 선택되었습니다.")
             
    #좌표 변환을 실행
    def funcExec(self) :
        list = []
        
        for i in range(0,len(self.roadAddress)) :
            result = road_region(self.roadAddress.iloc[i][self.addrCombo.currentText()])
            print(result)
            if(result is None):
                self.process.append(str(i+1)+". "+ "결과없음")
                list.append('none')
            else:
                self.process.append(str(i+1)+". "+ result)
                list.append(result);
           
        df1 = pd.DataFrame(list, columns = ['address_name'])
        df1.to_excel("road_region.xlsx")
        self.process.append("변환 완료")
        
#지번 주소를 도로명 주소로 변환
class frRegion_road(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.initUI()
        #self.setWindowModality(Qt.ApplicationModal)
        
    def initUI(self):
        self.btn_file1 = QPushButton('&파일 업로드', self)
        self.btn_file1.setCheckable(True)
        self.btn_file1.move(300, 40)
        self.btn_file1.resize(100, 30)
        self.btn_file1.clicked.connect(self.open)
        
        
        self.btn_file2 = QPushButton('&변환시작', self)
        self.btn_file2.setCheckable(True)
        self.btn_file2.move(60, 340)
        self.btn_file2.resize(100, 30)
        self.btn_file2.clicked.connect(self.funcExec)
        
        
        #x 콤보박스
        self.addrCombo = QComboBox(self)
        #콤보박스의 내용이 바뀌는 이벤트 등록
        self.addrCombo.currentIndexChanged.connect(self.printAddrname)
        self.addrCombo.move(60, 40)
        
        
        self.addrComboLabel = QLabel('주소',self)
        self.addrComboLabel.move(60, 20)
        self.addrComboLabel.resize(100, 20)
        #x 콤보박스 END
        
        #진행사항 창
        self.processLabel = QLabel('진행사항',self)
        self.processLabel.move(60, 180)
        self.processLabel.resize(100, 30)
        
        self.process = QTextEdit(self)#QLineEdit(self)
        self.process.move(60, 210)
        self.process.resize(500, 100)
        #진행사항 창 END
        
        vbox = QVBoxLayout()
        self.label = QLabel(self)
        self.label.move(10, 80)
        self.label.resize(500, 30)
        self.setLayout(vbox)
        self.setGeometry(300, 400, 650, 400)
        self.show()
        
        
        # 콤보 박스 선택된 값 
        #self.xCombo.currentText()
    def open(self):
        fname = QFileDialog.getOpenFileName(self)

        self.label.setText(fname[0])
        
        if(fname[0][-3:] == 'csv'):
            self.roadAddress = pd.read_csv(fname[0])
            for i in self.roadAddress.columns :
                self.addrCombo.addItem(i,i)

        elif(fname[0][-4:] == 'xlsx' or fname[0][-3:] == 'xls'):
            self.roadAddress = pd.read_excel(fname[0])
            for i in self.roadAddress.columns :
                self.addrCombo.addItem(i,i)
        else:
            self.process.append("csv나 xlsx파일을 입력해주시길 바랍니다")
            
 
    #파일 업로드시 콤보박스의 내용에 시트명 출력 
    def printAddrname(self):       
        self.process.append("주소 컬럼이 선택되었습니다.")
             
    #좌표 변환을 실행
    def funcExec(self) :
        list = []
        
        for i in range(0,len(self.roadAddress)) :
            result = region_road(self.roadAddress.iloc[i][self.addrCombo.currentText()])
            print(result)
            if(result is None):
                self.process.append(str(i+1)+". "+ "결과없음")
                list.append('none')
            else:
                self.process.append(str(i+1)+". "+ result)
                list.append(result);
           
        df1 = pd.DataFrame(list, columns = ['address_name'])
        df1.to_excel("road_region.xlsx")
        self.process.append("변환 완료")