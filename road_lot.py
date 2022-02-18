# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 16:44:18 2021
revise 07-15 15:08 2021
@author: ttyy4

kakao import 해서 사용

도로명 주소를 지번 주소로 
혹은 지번 주소를 도로명 주소로 변환해 전달해줌
kakao 모듈처럼 주소 하나 (str), 리스트로 전달 받은 주소들 변환 기능 제공



type_check(address):
    주소를 문자열로 받으면 도로명 주소인지 지번 주소인지 확인
    도로명 주소일 경우 'road', 지번 주소일 경우 'region' return한다
    후에 확장을 위해 boolean 사용안함
    

road_lot_str(address):
    도로명 주소를 문자열로 전달 받으면 지번 주소로 변환해 문자열로 제공해주는 함수
 
road_lot_list(address):
    도로명 주소들을 리스트로 전달 받으면 지번 주소들로 변환해 리스트로 제공해주는 함수
    
lot_road_str(address):
    지번 주소를 문자열로 전달 받으면 도로명 주소로 변환해 문자열로 제공해주는 함수
    
lot_road_list(address):
    지번 주소들을 리스토로 전달 받으면 도로명 주소들로 변환해 리스트로 제공해주는 함수
    

    
none_check(address):
    카카오 api가 주소를 인식하지 못해 NoneType 에러를 발생시키나를 확인하는 함수
    NoneType 아니면 true , NoneType일 경우 false 반환    
"""

from key import req_data 
import xy_addr as ka

def type_check(address) :
    url = "https://dapi.kakao.com/v2/local/search/address.json?&query=" +address
    json_obj = req_data(url).json()
    
    for document in json_obj['documents']:
        if document['address_type'] == 'ROAD_ADDR' :
            return 'road'
        elif document['address_type'] == 'REGION_ADDR' :
            return 'region'
        

def road_region(address):
    
    url = "https://dapi.kakao.com/v2/local/geo/coord2address.json?"

    if str(type(address)) == "<class 'str'>" :
        
        list = ka.coordinate(address)
        
        if list is not None :
            url_rev = url + "x={}&y={}".format(list[1], list[2])
            json_obj = req_data(url_rev).json()
        
            for document in json_obj['documents']:
        
                val = document['address']['address_name']

            return val
        else :
            pass

    elif str(type(address)) == "<class 'list'>" or str(type(address)) == "<class 'pandas.core.series.Series'>":
        val = []
        for addr in address :
            list = ka.coordinate(addr)
            url_rev = url + "x={}&y={}".format(list[1], list[2])
            json_obj = req_data(url_rev).json()
            
            for document in json_obj['documents']:

                val.append(document['address']['address_name'])
        return val

    else :
        return str(type(address))

def region_road(address):
    
    url = "https://dapi.kakao.com/v2/local/geo/coord2address.json?"

    if str(type(address)) == "<class 'str'>" :
        
        list = ka.coordinate(address)
        
        if list is not None :
            url_rev = url + "x={}&y={}".format(list[1], list[2])
            json_obj = req_data(url_rev).json()
        
            for document in json_obj['documents']:
                if ka.non_check(document['road_address']) :
                    val = document['road_address']['address_name']
                else :
                    return None
                
            return val
                
        else :
            pass
        

    elif str(type(address)) == "<class 'list'>" or str(type(address)) == "<class 'pandas.core.series.Series'>":
        val = []
        for addr in address :
            list = ka.coordinate(addr)
            url_rev = url + "x={}&y={}".format(list[1], list[2])
            json_obj = req_data(url_rev).json()
            
            for document in json_obj['documents']:
                if ka.non_check(document['road_address']) :
                    val.append(document['road_address']['address_name'])
                    
                else :
                    val.append('nonType')
        return val

    else :
        return None