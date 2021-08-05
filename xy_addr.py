# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 13:41:35 2021

@author: Chicken is Right

kakao api 사용

  coordinate(address) :
      주소를 입력 하면 x,y 좌표를 return해
      
      ____________________
      
      coordinate 하나로 통합 나머지 함수들도 하나의 함수로 변경할 것
  xy_addr:
      x,y 좌표를 도로명주소로 변경해 보내줌 
      이 함수부턴 str, list 함수를 따로 구분 없이 파라미터의 유형에 따라
      값을 다르게 처리하도록 함
      
      xy_addr 모둘과 road_lot 모듈 모두 공통으로 사용할 non_check() 체크 기능도 함께 추가 
"""

from key import req_data 

def non_check(address):
    if str(type(address)) != "<class 'NoneType'>":
        return True
    else :
        return False    

def coordinate(address):
    val = []
    url = "https://dapi.kakao.com/v2/local/search/address.json?&query=" 
    
    
    try :
        if str(type(address)) == "<class 'str'>" :
        
            json_obj = req_data(url+address).json()
            for document in json_obj['documents']:
                val = [document['address_name'], document['x'], document['y']]
            
                return val
        
        elif str(type(address)) == "<class 'list'>" or str(type(address)) == "<class 'pandas.core.series.Series'>":
        
            for addr in address :
            
                json_obj = req_data(url+addr).json()
            
                for document in json_obj['documents']:
                    val.append([document['address_name'], document['x'], document['y']])
            
         
            return val
            
    
        else :
            return str(type(address))
        
    except KeyError :
        return
    
    
def xy_addr(x, y) :
    val = []
    url = "https://dapi.kakao.com/v2/local/geo/coord2address.json?" 
    query = "x="+str(x)+"&y="+str(y)
    json_obj = req_data(url+query).json()
    
    
    try :
        if json_obj['code'] == -2 :
            return
        
         
    except KeyError :
        
        
        try :
            if json_obj['documents'][0]['road_address'] is None :
                val.append(json_obj['documents'][0]['address']['address_name']) 
            else :
                val.append(json_obj['documents'][0]['road_address']['address_name'])
                val.append(json_obj['documents'][0]['address']['address_name']) 
                
         
        except IndexError:
            return
   
    
    return val

