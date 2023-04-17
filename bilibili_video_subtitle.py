#感谢 https://github.com/SocialSisterYi/bilibili-API-collect 提供API文档!
#哔哩哔哩干杯!

import Core
import bilibili_video_info

while __name__ == "__main__" :
    List=Core.Video_info(input("请输入AV/BV号>>>"))
    if List['code'] != 0 :
        print(f"{List['code']} {Core.error_code[List['code']]}")
        continue

    data=List['data']
    s=data["subtitle"]
    print('~~~'*60)
    if not len(s['list']):
        print("此视频不包含字幕!")
        continue

    bilibili_video_info.Ouput_info( data )

    for i in s['list']:
        print('---'*60)
        print(f"{i['lan_doc']}",end=" ")#字幕语言名称
        print(f"[{i['lan']}]",end=" ")#字幕语言
        print(f"[ID {i['id']}]",end=" ")#字幕id
        print(f"[字幕状态 {['未锁定','已锁定'][i['is_lock']]}]",end=" ")#是否被锁定
        print(f"[类型 {['人工字幕','','AI字幕'][i['ai_status']]}]",end=" ")#是否为AI字幕
        if i['ai_status'] == 0:#是人工字幕
            print("|",end=" ")
            print(f"{i['author']['name']}",end=" ")#字幕作者名称
            print(f"[MID {i['author']['mid']}]",end=" ")#字幕作者MID
            print(f"[性别 {i['author']['sex']}]",end=" ")#字幕作者性别
        print(f"\n{i['subtitle_url']}")

        response = Core.requests.get(i['subtitle_url'])#获取Json字幕文件
        File_name = f"{data['title']}-{i['lan']}.srt"#字幕文件名称
        Srt_list=Core.json.loads(response.content)#加载为JSON文件
        Srt_body=Srt_list['body']#字幕主体
        
        Core.Json_to_str( File_name , Srt_body )

    print('---'*60)
    print('~~~'*60)
