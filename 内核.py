#感谢 https://github.com/SocialSisterYi/bilibili-API-collect 提供API文档!
#哔哩哔哩干杯!

import requests
import json
import time

#错误代码
error_code = {
    -400 : "请求错误" ,
    -403 : "权限不足" ,
    -404 : "无视频" ,
    62002 : "稿件不可见" , 
    62004 : "稿件审核中"
}

#秒级时间戳转字符串
def T(Time):return time.strftime("|Y/|m/|d |H:|M:|S".replace("|","%"),time.localtime(Time))

#判断到底是AV号还是BV号
def Is_av_or_bv( av_or_bv : str ) :
    maby_is_av = "".join( av_or_bv.lower().split( "av" ) )
    if av_or_bv.isdigit() :
        return "aid" , maby_is_av
    else : return "bvid" , av_or_bv

#获取视频信息
def Video_info(av_or_bv):
    params = {}
    id_type , id = Is_av_or_bv( av_or_bv )
    params[ id_type ] = id
    response=requests.get(f"https://api.bilibili.com/x/web-interface/view" , params = params )#调用API
    List=json.loads(response.content)
    return List

#把秒转换为Srt可识别的格式
def Time(T):
    millisecond=int(T*1000)
    second=int(T%60)
    minute=int(T/60%60)
    hour=int(T/60/60%60)
    return str(hour)+":"+str(minute)+":"+str(second)+","+str(millisecond)[-3:]

#把JSON字幕转为str字幕 (上传小破站时都是str文件 为什么不干脆使用str文件储存 而是JSON 害得我还得转回来 Z_Z )
def Json_to_str( File_name : str , Srt_body : list ):
    with open( File_name , "w" , encoding = "utf-8" ) as file:
        for i in range(len(Srt_body)):
            file.write(f"{str(i+1)}\n")
            file.write(f"{Time(Srt_body[i]['from'])} --> {Time(Srt_body[i]['to'])}\n")
            file.write(f"{Srt_body[i]['content']}\n\n")
