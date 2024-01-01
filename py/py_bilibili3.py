# coding=utf-8
# !/usr/bin/python
import sys

sys.path.append('..')
from base.spider import Spider
import json
import requests
from requests import session, utils
import os
import time
import base64
from time import strftime
from time import gmtime




class Spider(Spider):  # 元类 默认的元类 type
    box_video_type = ''
    vod_area='bilidanmu'

    def getName(self):
        return "哔哩3_带直播"


    def __init__(self):


        self.getCookie()



        url = 'http://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=%s&jsonp=jsonp' % (self.userid)

        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)



        fav_list=[]


        if jo['code'] == 0:
            for fav in jo['data'].get('list'):

                fav_dict =  {'n':fav['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"').strip() ,'v':fav['id']}
                fav_list.append(fav_dict)


        if self.config["filter"].get('收藏夹'):
            for i in self.config["filter"].get('收藏夹'):
                if i['key']=='mlid':
                    i['value']=fav_list

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass


    def isVideoFormat(self, url):
        pass

    def second_to_time(self,a):
        #将秒数转化为 时分秒的格式
        if a < 3600:
            return time.strftime("%M:%S", time.gmtime(a))
        else:
            return time.strftime("%H:%M:%S", time.gmtime(a))

    def manualVideoCheck(self):

        pass

    #用户userid
    userid=''

    def get_live_userInfo(self,uid):

        url = 'https://api.live.bilibili.com/live_user/v1/Master/info?uid=%s'%uid


        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)

        if jo['code'] == 0:

            return jo['data']["info"]["uname"]



    def homeContent(self, filter):
        result = {}
        cateManual = {
            "推荐": "推荐",
            "新闻": "新闻",
            "热门": "热门",
            "排行榜": "排行榜",
            "AI孙燕姿": "AI孙燕姿",
            "舞蹈": "舞蹈",
            "频道": "频道",
            "直播": "直播",
            "动态": "动态",
            "历史记录": '历史记录',
            "收藏夹": '收藏夹',
            
            
            "宅舞": "宅舞",
            "少女": "少女",
            'cosplay':'cosplay',
             'mmd':'mmd',
            '索尼':'索尼音乐中国',
            "鬼畜": "鬼畜",
            "狗狗": "汪星人",
            '科技': '科技',

            "音声": "音声",
            "演唱会": "演唱会",
            "番剧": "1",
            "国创": "4",
            "电影": "2",
            "综艺": "7",
            "电视剧": "5",
            "纪录片": "3",

        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if (filter):
            result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        self.box_video_type = '热门'
        return self.get_hot(pg='1')

    cookies = ''

    # def getCookie(self):
    #     # 在cookies_str中填入会员或大会员cookie，以获得更好的体验。
    #     cookies_str = "buvid3=CFF74DA7-E79E-4B53-BB96-FC74AB8CD2F3184997infoc; LIVE_BUVID=AUTO4216125328906835; rpdid=|(umRum~uY~R0J'uYukYukkkY; balh_is_closed=; balh_server_inner=__custom__; PVID=4; video_page_version=v_old_home; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; blackside_state=0; fingerprint=8965144a609d60190bd051578c610d72; buvid_fp_plain=undefined; CURRENT_QUALITY=120; hit-dyn-v2=1; nostalgia_conf=-1; buvid_fp=CFF74DA7-E79E-4B53-BB96-FC74AB8CD2F3184997infoc; CURRENT_FNVAL=4048; DedeUserID=85342; DedeUserID__ckMd5=f070401c4c699c83; b_ut=5; hit-new-style-dyn=0; buvid4=15C64651-E8B7-100C-4B1F-C7CFD2DB473007906-022110820-jYQRaMeS%2BRXRfw14q70%2FLQ%3D%3D; b_nut=1667910208; b_lsid=3CE4AE79_184578915C0; is-2022-channel=1; innersign=0; SESSDATA=a5e4d58d%2C1683641322%2C2c39a%2Ab1; bili_jct=2f3126b5954e37f593130f2fef082cd8; sid=p7tjqv22; bp_video_offset_85342=726936847258746900"
    #     cookies_dic = dict([co.strip().split('=') for co in cookies_str.split(';')])
    #     rsp = session()
    #    cookies_jar = utils.cookiejar_from_dict(cookies_dic)
    #     rsp.cookies = cookies_jar
    #     content = self.fetch("http://api.bilibili.com/x/web-interface/nav", cookies=rsp.cookies)
    #     res = json.loads(content.text)
    #     if res["code"] == 0:
    #         self.cookies = rsp.cookies
    #     else:

    #         rsp = self.fetch("https://www.bilibili.com/")
    #         self.cookies = rsp.cookies
    #     return rsp.cookies
    def getCookie(self):

        #在下方cookies_str  后面 双引号里面放置你的cookies
        cookies_str = "SESSDATA=8a342237%2C1717720914%2Cad152%2Ac1CjAI7lFDbr9Wlb6WWq1gwWKrFSGHnqgFdC4gO3x6gzdxxDrCLzUwuAIPQQC6-3jY-cUSVlNDeE9rZTVjLWVPUDFRUlBBR3BuN0FhaWFIRGYxZTJqeTdsT2E1Zi1sUHM4b1VJMXdrWVprcFhtVmdNMDRiNmd4TEMxNVNEMHhuYWtlbVBESnd5aF93IIEC; bili_jct=81665ed688f163a82c181774dc069294; DedeUserID=29803158; DedeUserID__ckMd5=1a97fc9755184b19; sid=7dy2gka0"
        if cookies_str:
            cookies =  dict([co.strip().split('=') for co in cookies_str.split(';')])
            bili_jct = cookies['bili_jct']
            SESSDATA = cookies['SESSDATA']
            DedeUserID = cookies['DedeUserID']

            cookies_jar={"bili_jct":bili_jct,
                         'SESSDATA': SESSDATA,
                         'DedeUserID':DedeUserID

            }
            rsp = session()
            rsp.cookies = cookies_jar
            content = self.fetch("http://api.bilibili.com/x/web-interface/nav", cookies=rsp.cookies)
            res = json.loads(content.text)

            if res["code"] == 0:
                self.cookies = rsp.cookies
                self.userid = res["data"].get('mid')

                return rsp.cookies
        rsp = self.fetch("https://www.bilibili.com/")
        self.cookies = rsp.cookies


        return rsp.cookies

    def get_rcmd(self, pg):
        result = {}
        url = 'https://api.bilibili.com/x/web-interface/index/top/feed/rcmd?ps=20&pn={0}'.format(pg)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['item']
            for vod in vodList:
                aid = str(vod['id']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
                img = vod['pic'].strip()
                remark = str(self.second_to_time(vod['duration'])).strip()
                videos.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result
        

   

    def get_hot(self, pg):
        result = {}
        url = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={0}'.format(pg)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
                img = vod['pic'].strip()
                remark = str(self.second_to_time(vod['duration'])).strip()
                videos.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def str2sec(self,x):
        '''
          字符串时分秒转换成秒
        '''
        x=str(x)
        try:
              h, m, s = x.strip().split(':') #.split()函数将其通过':'分隔开，.strip()函数用来除去空格
              return int(h)*3600 + int(m)*60 + int(s) #int()函数转换成整数运算
        except:
               m, s = x.strip().split(':') #.split()函数将其通过':'分隔开，.strip()函数用来除去空格
               return  int(m)*60 + int(s) #int()函数转换成整数运算


    def get_rank(self,cid):
        result = {}
        url = 'https://api.bilibili.com/x/web-interface/ranking/v2?rid={0}&type=all'.format(cid)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
                img = vod['pic'].strip()
                remark = str(self.second_to_time(vod['duration'])).strip()
                videos.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result


    def filter_duration(self, vodlist, key):
        # 按时间过滤
        if key == '0':
            return vodlist
        else:


            vod_list_new = [i for i in vodlist if self.time_diff1[key][0] <= self.str2sec(str(i["vod_remarks"])) < self.time_diff1[key][1]]
            return vod_list_new
            
 

    chanel_offset=''
    def get_channel(self, pg, cid,extend,order,duration_diff):
        result = {}


        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}&duration={2}&order={3}'.format(
                cid, pg,duration_diff,order)
        rsp = self.fetch(url, cookies=self.cookies)

        content = rsp.text
        jo = json.loads(content)
        if jo.get('code') == 0:
            videos = []
            vodList = jo['data']['result']
            for vod in vodList:
                    aid = str(vod['aid']).strip()
                    title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                    img = 'https:' + vod['pic'].strip()
                    remark = str( self.second_to_time(self.str2sec(vod['duration']))).strip()
                    videos.append({
                        "vod_id": aid,
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark

                    })


                #videos=self.filter_duration(videos, duration_diff)
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result




    dynamic_offset = ''

    def get_dynamic(self, pg):
        result = {}

        if str(pg) == '1':
            url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&page=%s' % pg
        else:
            # print('偏移',self.dynamic_offset)
            url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&offset=%s&page=%s' % (
            self.dynamic_offset, pg)

        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            self.dynamic_offset = jo['data'].get('offset')
            videos = []
            vodList = jo['data']['items']
            for vod in vodList:
                if vod['type'] == 'DYNAMIC_TYPE_AV':
                    #up=vod['modules']["module_author"]['name']
                    ivod = vod['modules']['module_dynamic']['major']['archive']
                    aid = str(ivod['aid']).strip()
                    title = ivod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
                    img = ivod['cover'].strip()
                    #remark = str(ivod['duration_text']).strip()
                    remark =str( self.second_to_time(self.str2sec(ivod['duration_text']))).strip()
                    videos.append({
                        "vod_id": aid,
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark
                    })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result


    time_diff1={'1':[0,300],
    '2':[300,900],'3':[900,1800],'4':[1800,3600],
    '5':[3600,99999999999999999999999999999999]

    }

    time_diff='0'


    def get_fav_detail(self,pg,mlid,order):
        result = {}



        url = 'http://api.bilibili.com/x/v3/fav/resource/list?media_id=%s&order=%s&pn=%s&ps=20&platform=web&type=0'%(mlid,order,pg)
        rsp = self.fetch(url, cookies=self.cookies)

        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['medias']

            for vod in vodList:
                    #print(vod)
                    #只展示类型为 视频的条目
                    #过滤去掉收藏夹中的 已失效视频;如果不喜欢可以去掉这个 if条件
                    if vod.get('type') in [2]  and vod.get('title') != '已失效视频':

                        aid = str(vod['id']).strip()
                        title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                        img =  vod['cover'].strip()
                        remark = str( self.second_to_time(vod['duration'])).strip()
                        videos.append({
                            "vod_id": aid,
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": remark

                        })



                #videos=self.filter_duration(videos, duration_diff)
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999

        return result

    def get_fav(self,pg,order,extend):


    #获取自己的up_mid(也就是用户uid)


        mlid=''

        fav_config=self.config["filter"].get('收藏夹')

        #默认显示第一个收藏夹内容
        if fav_config:
            for i in fav_config:
                if i['key']=='mlid':
                    if len(i['value'])>0:
                        mlid=i['value'][0]['v']




        #print(self.config["filter"].get('收藏夹'))

        if 'mlid' in extend:
                mlid = extend['mlid']
        if mlid:
            return self.get_fav_detail(pg=pg,mlid=mlid,order=order)
        else:
            return {}



    def get_history(self,pg):
        result = {}
        url = 'http://api.bilibili.com/x/v2/history?pn=%s' % pg
        rsp = self.fetch(url,cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)   #解析api接口,转化成json数据对象
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']
            for vod in vodList:
                if vod['duration'] > 0:   #筛选掉非视频的历史记录
                    aid = str(vod["aid"]).strip()   #获取 aid
                    #获取标题
                    title = vod["title"].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;",
                                                                                                      '"')
                    #封面图片
                    img = vod["pic"].strip()

                    #获取已观看时间
                    if str(vod['progress'])=='-1':
                        process=str(self.second_to_time(vod['duration'])).strip()
                    else:
                        process = str(self.second_to_time(vod['progress'])).strip()
                    #获取视频总时长
                    total_time= str(self.second_to_time(vod['duration'])).strip()
                    #组合 已观看时间 / 总时长 ,赋值给 remark
                    remark = process+' / '+total_time
                    videos.append({
                        "vod_id": aid,
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark

                    })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result


    def get_live(self,pg,parent_area_id):
        result = {}



        url = 'https://api.live.bilibili.com/room/v3/area/getRoomList?page=%s&sort_type=online&parent_area_id=%s'%(pg,parent_area_id)
        rsp = self.fetch(url, cookies=self.cookies)

        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']

            for vod in vodList:



                        aid = str(vod['roomid']).strip()
                        title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                        img =  vod.get('cover').strip()
                        roomname = str( vod['uname']).strip()+'❤️'+str( vod['online']).strip()
                        remark = '直播间人数:'+str( vod['online']).strip()
                        videos.append({
                            "vod_id": aid,
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": roomname

                        })



                #videos=self.filter_duration(videos, duration_diff)
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999

        return result




    def categoryContent(self, tid, pg, filter, extend):

        result = {}

        if len(self.cookies) <= 0:
            self.getCookie()

        if tid == "热门":
            self.box_video_type = '热门'
            return self.get_hot(pg=pg)
        elif tid == "推荐":
            self.box_video_type = '推荐'
            return self.get_rcmd(pg=pg)
            
        elif tid == "排行榜":
            self.box_video_type = '排行榜'
            cid = '0'
            if 'cid' in extend:
                cid = extend['cid']
            return self.get_rank(cid=cid)
            
          
            
        elif tid == "新闻":
            self.box_video_type = '新闻'
            cid = '新闻&tids=202'
            duration_diff='0'
            order = 'pubdate'
            return self.get_channel(pg=pg, cid=cid,extend=extend,order=order,duration_diff=duration_diff)
      
        elif tid == "收藏夹":
            self.box_video_type = '收藏夹'
            order = 'mtime'
            if 'order' in extend:
                order = extend['order']

            return self.get_fav(pg=pg, order=order,extend=extend)

        elif tid == '直播':
            self.box_video_type = '直播'
            parent_area_id = '1&area_id=207'
            if 'parent_area_id' in extend:
                parent_area_id = extend['parent_area_id']
            return  self.get_live(pg=pg,parent_area_id=parent_area_id)

        elif tid == '舞蹈':
            self.box_video_type = '舞蹈'

            cid = '舞蹈'
            if 'cid' in extend:
                cid = extend['cid']

            duration_diff='0'
            if 'duration' in extend:
                duration_diff = extend['duration']

            order = 'pubdate'
            if 'order' in extend:
                order = extend['order']


            return self.get_channel(pg=pg, cid=cid,extend=extend,order=order,duration_diff=duration_diff)

        elif tid == 'AI孙燕姿':
            self.box_video_type = 'AI孙燕姿'

            cid = 'AI孙燕姿'
            

            duration_diff='0'
            if 'duration' in extend:
                duration_diff = extend['duration']

            order = 'pubdate'
            if 'order' in extend:
                order = extend['order']


            return self.get_channel(pg=pg, cid=cid,extend=extend,order=order,duration_diff=duration_diff)

        elif tid == '频道':
            self.box_video_type = '频道'

            cid = '生活'
            if 'cid' in extend:
                cid = extend['cid']

            duration_diff='0'
            if 'duration' in extend:
                duration_diff = extend['duration']

            order = 'pubdate'
            if 'order' in extend:
                order = extend['order']






            return self.get_channel(pg=pg, cid=cid,extend=extend,order=order,duration_diff=duration_diff)


        elif tid == '动态':
            self.box_video_type = '动态'
            return self.get_dynamic(pg=pg)

        elif tid == '历史记录':
            self.box_video_type = '历史记录'
            return self.get_history(pg=pg)
        elif tid.isdigit():
            self.box_video_type = '影视'
            url = 'https://api.bilibili.com/pgc/season/index/result?order=2&season_status=-1&style_id=-1&sort=0&area=-1&pagesize=20&type=1&st={0}&season_type={0}&page={1}'.format(
                tid, pg)
            rsp = self.fetch(url, cookies=self.cookies)
            content = rsp.text
            jo = json.loads(content)
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['season_id']).strip()
                title = vod['title'].strip()
                img = vod['cover'].strip()
                remark = vod['index_show'].strip()
                videos.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark  # 视频part数量

                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999



        else:
            duration_diff='0'
            if 'duration' in extend:
                duration_diff = extend['duration']

            order = 'totalrank'
            if 'order' in extend:
                order = extend['order']




            self.box_video_type = '其他'
            url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}&duration={2}&order={3}'.format(
                tid, pg,duration_diff,order)
            rsp = self.fetch(url, cookies=self.cookies)

            content = rsp.text
            jo = json.loads(content)

            if jo.get('code') == 0:
                videos = []
                vodList = jo['data']['result']
                for vod in vodList:
                    aid = str(vod['aid']).strip()
                    title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
                    img = 'https:' + vod['pic'].strip()
                    #remark = str(vod['duration']).strip()
                    remark =str( self.second_to_time(self.str2sec(vod['duration']))).strip()
                    videos.append({
                        "vod_id": aid,
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark

                    })


            #videos=self.filter_duration(videos, duration_diff)
                result['list'] = videos
                result['page'] = pg
                result['pagecount'] = 9999
                result['limit'] = 90
                result['total'] = 999999
        return result

    def cleanSpace(self, str):
        return str.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

    def detailContent(self, array):
        # if int(array[0])< 1000000:
        result={}
        if self.box_video_type == '影视':
            aid = array[0]
            url = "http://api.bilibili.com/pgc/view/web/season?season_id={0}".format(aid)
            rsp = self.fetch(url, headers=self.header)
            jRoot = json.loads(rsp.text)
            if jRoot['code'] == 0:
                jo = jRoot['result']
                id = jo['season_id']
                title = jo['title']
                pic = jo['cover']
                areas = jo['areas'][0]['name']
                typeName = jo['share_sub_title']
                dec = jo['evaluate']
                remark = jo['new_ep']['desc']
                vod = {
                    "vod_id": id,
                    "vod_name": title,
                    "vod_pic": pic,
                    "type_name": typeName,
                    "vod_year": "",
                    # "vod_area":areas,
                    "vod_area": self.vod_area,  #弹幕是否显示的开关
                    "vod_remarks": remark,
                    "vod_actor": "",
                    "vod_director": "",
                    "vod_content": dec
                }
                ja = jo['episodes']
                playUrl = ''
                for tmpJo in ja:
                    eid = tmpJo['id']
                    cid = tmpJo['cid']
                    part = tmpJo['title'].replace("#", "-")
                    playUrl = playUrl + '{0}${1}_{2}#'.format(part, eid, cid)

                vod['vod_play_from'] = 'B站'
                vod['vod_play_url'] = playUrl

                result = {
                    'list': [
                        vod
                    ]
                }

        elif self.box_video_type == '直播':
            
            aid = array[0]
            url = "https://api.live.bilibili.com/room/v1/Room/get_info?room_id=%s"%aid
            rsp = self.fetch(url, headers=self.header,cookies=self.cookies)
            jRoot = json.loads(rsp.text)
            if jRoot.get('code')==0:
                jo = jRoot['data']
                title = jo['title'].replace("<em class=\"keyword\">", "").replace("</em>", "")
                pic = jo.get("user_cover")
                desc = jo.get('description')

                dire = self.get_live_userInfo(jo["uid"])
                typeName = jo.get("area_name")
                area = jo.get("parent_area_name")
                remark = '在线人数:'+str(jo['online']).strip()
                playUrl = 'flv线路原画$platform=web&quality=4_' + aid + '#flv线路高清$platform=web&quality=3_' + aid + '#h5线路原画$platform=h5&quality=4_' + aid + '#h5线路高清$platform=h5&quality=3_' + aid

                vod = {
                    "vod_id": aid,
                    "vod_name": '(' + dire + ")" + title,
                    "vod_pic": pic,
                    "type_name": typeName,

                    "vod_area": area,
                     #"vod_area":"",
                    "vod_remarks": remark,
                    "vod_actor": "",
                    "vod_director": dire,
                    "vod_content": desc + 'up主:' + dire,
                    'vod_play_from':'B站',
                   'vod_play_url':playUrl,
                }
				

                result = {
                    'list': [
                        vod
                    ]
                }

        else:
            aid = array[0]
            url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(aid)
            rsp = self.fetch(url, headers=self.header)
            jRoot = json.loads(rsp.text)
            if jRoot['code'] == 0:
                jo = jRoot['data']
                title = jo['title'].replace("<em class=\"keyword\">", "").replace("</em>", "")
                pic = jo['pic']
                desc = jo['desc']
                timeStamp = jo['pubdate']
                timeArray = time.localtime(timeStamp)
                tim = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))
               
                year = str(time.strftime("%Y", timeArray))
                m = str(time.strftime("%m", timeArray))
                d = str(time.strftime("%d", timeArray))
                h = str(time.strftime("%H", timeArray))
                m1 = str(time.strftime("%M", timeArray))
                s = str(time.strftime("%S", timeArray))
                dire = jo['owner']['name']
                typeName = jo['tname']
                remark = str(jo['duration']).strip()

                vod = {
                    "vod_id": aid,
                    "vod_name": '🔥标题 : ' + title,
                    "vod_pic": pic,
                    "type_name": typeName,
                    "vod_year": year,
                    "vod_area": self.vod_area,
                    # "vod_area":"",
                    "vod_remarks": remark,
                    "vod_actor": tim,
                    "vod_director": '🔥UP主:'+dire+'❤️❤️日期:'+year+'-'+m+'-'+d+'  '+h+':'+m1+':'+s,
                    "vod_content": desc + 'up主:' + dire
                }
                ja = jo['pages']
                playUrl = ''
                for tmpJo in ja:
                    cid = tmpJo['cid']
                    part = tmpJo['part'].replace("#", "-")
                    playUrl = playUrl + '{0}${1}_{2}#'.format(part, aid, cid)

                vod['vod_play_from'] = 'B站'
                vod['vod_play_url'] = playUrl

                result = {
                    'list': [
                        vod
                    ]
                }
        return result

    def searchContent(self, key, quick):
        self.box_video_type = '搜索'
        header = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page=1'.format(key)

        rsp = self.fetch(url, cookies=self.cookies, headers=header)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] != 0:
            rspRetry = self.fetch(url, cookies=self.cookies, headers=header)
            content = rspRetry.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['result']
        for vod in vodList:
            aid = str(vod['aid']).strip()
            title = vod['title'].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;", '"')
            img = 'https:' + vod['pic'].strip()
            remark = str(vod['duration']).strip()
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        result = {
            'list': videos
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        if self.box_video_type == '影视':
            ids = id.split("_")
            header = {
                "Referer": "https://www.bilibili.com",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
            }
            url = 'https://api.bilibili.com/pgc/player/web/playurl?qn=116&ep_id={0}&cid={1}'.format(ids[0], ids[1])
            if len(self.cookies) <= 0:
                self.getCookie()
            rsp = self.fetch(url, cookies=self.cookies, headers=header)
            jRoot = json.loads(rsp.text)
            if jRoot['message'] != 'success':
                print("需要大会员权限才能观看")
                return {}
            jo = jRoot['result']
            ja = jo['durl']
            maxSize = -1
            position = -1
            for i in range(len(ja)):
                tmpJo = ja[i]
                if maxSize < int(tmpJo['size']):
                    maxSize = int(tmpJo['size'])
                    position = i

            url = ''
            if len(ja) > 0:
                if position == -1:
                    position = 0
                url = ja[position]['url']

            result["parse"] = 0
            result["playUrl"] = ''
            result["url"] = url
            result["header"] = {
                "Referer": "https://www.bilibili.com",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
            }
            
            result["contentType"] = 'video/x-flv'

        elif self.box_video_type == '直播':

            ids = id.split("_")
            url = 'https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&%s' % (ids[1], ids[0])


            if len(self.cookies) <= 0:
                self.getCookie()
            rsp = self.fetch(url, cookies=self.cookies)
            jRoot = json.loads(rsp.text)
            if jRoot['code'] == 0:


                jo = jRoot['data']
                ja = jo['durl']


                url = ''
                if len(ja) > 0:

                    url = ja[0]['url']

                result["parse"] = 0
                # result['type'] ="m3u8"
                result["playUrl"] = ''
                result["url"] = url
                result["header"] = {
                    "Referer": "https://live.bilibili.com",
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
                }




        else:

            ids = id.split("_")
            url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid={1}&qn=116'.format(ids[0], ids[1])

            if len(self.cookies) <= 0:
                self.getCookie()
            rsp = self.fetch(url, cookies=self.cookies)
            jRoot = json.loads(rsp.text)
            jo = jRoot['data']
            ja = jo['durl']

            maxSize = -1
            position = -1

            for i in range(len(ja)):
                tmpJo = ja[i]
                if maxSize < int(tmpJo['size']):
                    maxSize = int(tmpJo['size'])
                    position = i

            url = ''
            if len(ja) > 0:
                if position == -1:
                    position = 0
                url = ja[position]['url']

            result["parse"] = 0
            result["playUrl"] = ''
            result["url"] = url
            result["header"] = {
                "Referer": "https://www.bilibili.com",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
            }
            
            result["contentType"] = 'video/x-flv'
        return result

    config = {
        "player": {},
        "filter": {
        
		   "PD": [{
                "key": "cid",
                "name": "频道",
                "value": [

                 {
                        "n": "全部",
                        "v": "0"
                    },

                 {'n': '搞笑', 'v': 1833}, {'n': '美食', 'v': 20215}, {'n': '鬼畜', 'v': 68}, {'n': '天官赐福', 'v': 2544632}, {'n': '英雄联盟', 'v': 9222}, {'n': '美妆', 'v': 832569}, {'n': '必剪创作', 'v': 15775524}, {'n': '单机游戏', 'v': 17683}, {'n': '搞笑', 'v': 1833}, {'n': '科普', 'v': 5417}, {'n': '影视剪辑', 'v': 318570}, {'n': 'vlog', 'v': 2511282}, {'n': '声优', 'v': 1645}, {'n': '动漫杂谈', 'v': 530918}, {'n': 'COSPLAY', 'v': 88}, {'n': '漫展', 'v': 22551}, {'n': 'MAD', 'v': 281}, {'n': '手书', 'v': 608}, {'n': '英雄联盟', 'v': 9222}, {'n': '王者荣耀', 'v': 1404375}, {'n': '单机游戏', 'v': 17683}, {'n': '我的世界', 'v': 47988}, {'n': '守望先锋', 'v': 926988}, {'n': '恐怖游戏', 'v': 17941}, {'n': '英雄联盟', 'v': 9222}, {'n': '王者荣耀', 'v': 1404375}, {'n': '守望先锋', 'v': 926988}, {'n': '炉石传说', 'v': 318756}, {'n': 'DOTA2', 'v': 47034}, {'n': 'CS:GO', 'v': 99842}, {'n': '鬼畜', 'v': 68}, {'n': '鬼畜调教', 'v': 497221}, {'n': '诸葛亮', 'v': 51330}, {'n': '二次元鬼畜', 'v': 29415}, {'n': '王司徒', 'v': 987568}, {'n': '万恶之源', 'v': 21}, {'n': '美妆', 'v': 832569}, {'n': '服饰', 'v': 313718}, {'n': '减肥', 'v': 20805}, {'n': '穿搭', 'v': 1139735}, {'n': '发型', 'v': 13896}, {'n': '化妆教程', 'v': 261355}, {'n': '电音', 'v': 14426}, {'n': '欧美音乐', 'v': 17034}, {'n': '中文翻唱', 'v': 8043}, {'n': '洛天依', 'v': 8564}, {'n': '翻唱', 'v': 386}, {'n': '日文翻唱', 'v': 85689}, {'n': '科普', 'v': 5417}, {'n': '技术宅', 'v': 368}, {'n': '历史', 'v': 221}, {'n': '科学', 'v': 1364}, {'n': '人文', 'v': 40737}, {'n': '科幻', 'v': 5251}, {'n': '手机', 'v': 7007}, {'n': '手机评测', 'v': 143751}, {'n': '电脑', 'v': 1339}, {'n': '摄影', 'v': 25450}, {'n': '笔记本', 'v': 1338}, {'n': '装机', 'v': 413678}, {'n': '课堂教育', 'v': 3233375}, {'n': '公开课', 'v': 31864}, {'n': '演讲', 'v': 2739}, {'n': 'PS教程', 'v': 335752}, {'n': '编程', 'v': 28784}, {'n': '英语学习', 'v': 360005}, {'n': '喵星人', 'v': 1562}, {'n': '萌宠', 'v': 6943}, {'n': '汪星人', 'v': 9955}, {'n': '大熊猫', 'v': 22919}, {'n': '柴犬', 'v': 30239}, {'n': '吱星人', 'v': 6947}, {'n': '美食', 'v': 20215}, {'n': '甜点', 'v': 35505}, {'n': '吃货', 'v': 6942}, {'n': '厨艺', 'v': 239855}, {'n': '烘焙', 'v': 218245}, {'n': '街头美食', 'v': 1139423}, {'n': 'A.I.Channel', 'v': 3232987}, {'n': '虚拟UP主', 'v': 4429874}, {'n': '神楽めあ', 'v': 7562902}, {'n': '白上吹雪', 'v': 7355391}, {'n': '彩虹社', 'v': 1099778}, {'n': 'hololive', 'v': 8751822}, {'n': 'EXO', 'v': 191032}, {'n': '防弹少年团', 'v': 536395}, {'n': '肖战', 'v': 1450880}, {'n': '王一博', 'v': 902215}, {'n': '易烊千玺', 'v': 15186}, {'n': 'BLACKPINK', 'v': 1749296}, {'n': '宅舞', 'v': 9500}, {'n': '街舞', 'v': 5574}, {'n': '舞蹈教学', 'v': 157087}, {'n': '明星舞蹈', 'v': 6012204}, {'n': '韩舞', 'v': 159571}, {'n': '古典舞', 'v': 161247}, {'n': '旅游', 'v': 6572}, {'n': '绘画', 'v': 2800}, {'n': '手工', 'v': 11265}, {'n': 'vlog', 'v': 2511282}, {'n': 'DIY', 'v': 3620}, {'n': '手绘', 'v': 1210}, {'n': '综艺', 'v': 11687}, {'n': '国家宝藏', 'v': 105286}, {'n': '脱口秀', 'v': 4346}, {'n': '日本综艺', 'v': 81265}, {'n': '国内综艺', 'v': 641033}, {'n': '人类观察', 'v': 282453}, {'n': '影评', 'v': 111377}, {'n': '电影解说', 'v': 1161117}, {'n': '影视混剪', 'v': 882598}, {'n': '影视剪辑', 'v': 318570}, {'n': '漫威', 'v': 138600}, {'n': '超级英雄', 'v': 13881}, {'n': '影视混剪', 'v': 882598}, {'n': '影视剪辑', 'v': 318570}, {'n': '诸葛亮', 'v': 51330}, {'n': '韩剧', 'v': 53056}, {'n': '王司徒', 'v': 987568}, {'n': '泰剧', 'v': 179103}, {'n': '郭德纲', 'v': 8892}, {'n': '相声', 'v': 5783}, {'n': '张云雷', 'v': 1093613}, {'n': '秦霄贤', 'v': 3327368}, {'n': '孟鹤堂', 'v': 1482612}, {'n': '岳云鹏', 'v': 24467}, {'n': '假面骑士', 'v': 2069}, {'n': '特摄', 'v': 2947}, {'n': '奥特曼', 'v': 963}, {'n': '迪迦奥特曼', 'v': 13784}, {'n': '超级战队', 'v': 32881}, {'n': '铠甲勇士', 'v': 11564}, {'n': '健身', 'v': 4344}, {'n': '篮球', 'v': 1265}, {'n': '体育', 'v': 41103}, {'n': '帕梅拉', 'v': 257412}, {'n': '极限运动', 'v': 8876}, {'n': '足球', 'v': 584}, {'n': '星海', 'v': 178862}, {'n': '张召忠', 'v': 116480}, {'n': '航母', 'v': 57834}, {'n': '航天', 'v': 81618}, {'n': '导弹', 'v': 14958}, {'n': '战斗机', 'v': 24304}
                
                ]
            
                }],
          "排行榜": [{
                "key": "cid",
                "name": "分区",
                "value": [

                 {
                        "n": "全部",
                        "v": "0"
                    },

                 {"n": "舞蹈","v": "129"},{"n": "音乐","v": "3"},{'n': '生活', 'v': '160'},{'n': '美食', 'v': '211'},{'n': '动物圈', 'v': '217'},{'n': '鬼畜', 'v': '119'},{'n': '时尚', 'v': '155'},{'n': '娱乐', 'v': '5'},{'n': '影视', 'v': '181'},{"n": "游戏","v": "4"},{"n": "知识","v": "36"},{'n': '科技', 'v': '188'},{'n': '运动', 'v': '234'},{'n': '汽车', 'v': '223'},{'n': '国创相关', 'v': '168'},{'n': '动画', 'v': '1'},{'n': '原创', 'v': '0&type=origin'},{'n': '新人', 'v': '0&type=rookie'}
                
                ]
            
                }],

        "舞蹈": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {"key": "cid", "name": "分类",
                    "value":[{'n': '斗鱼', 'v': '斗鱼舞蹈'},{'n': '虎牙', 'v': '虎牙舞蹈'}, {'n': '王雨檬', 'v': '王雨檬'}, {'n': '萌七', 'v': '萌七'}, {'n': '米娜', 'v': '米娜呀'}, {'n': '周淑怡', 'v': '周淑怡'}, {'n': '沫子', 'v': '沫子'}]
                },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],



         "少女": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],
         "AI孙燕姿": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],


         "mmd": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],
"索尼音乐中国": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],

            "直播": [{
                "key": "parent_area_id",
                "name": "直播分区",
                "value": [

                 {
                        "n": "全部分区",
                        "v": "0"
                    },

                    {
                        "n": "娱乐",
                        "v": "1"
                    },
                      {
                        "n": "电台",
                        "v": "5"
                    },
                    {
                        "n": "网游",
                        "v": "2"
                    },
                     {
                        "n": "手游",
                        "v": "3"
                    },



                     {
                        "n": "单机游戏",
                        "v": "6"
                    },

                     {
                        "n": "虚拟主播",
                        "v": "9"
                    },{'n': '生活', 'v': 10},
                    {'n': '知识', 'v': 11},
                    {'n': '赛事', 'v': 13}



                ]
            },
            {
                "key": "parent_area_id",
                "name": "娱乐",
                "value": [{"n": "娱乐全部","v": "1"},{"n":"视频唱见","v":"1&area_id=21"},{"n":"萌宅领域","v":"1&area_id=530"},{"n":"视频聊天","v":"1&area_id=145"},{"n":"舞见","v":"1&area_id=207"},{"n":"情感","v":"1&area_id=706"},{"n":"户外","v":"1&area_id=123"},{"n":"日常","v":"1&area_id=399"}]
            },
            {
                "key": "parent_area_id",
                "name": "生活",
                "value": [{"n":"生活全部","v":"10"},{"n":"生活分享","v":"10&area_id=646"},{"n":"运动","v":"10&area_id=628"},{"n":"搞笑","v":"10&area_id=624"},{"n":"手工绘画","v":"10&area_id=627"},{"n":"萌宠","v":"10&area_id=369"},{"n":"美食","v":"10&area_id=367"},{"n":"时尚","v":"10&area_id=378"},{"n":"影音馆","v":"10&area_id=33"}]
            },
                ],


         "音声": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],

         "收藏夹": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "收藏时间",
                        "v": "mtime"
                    },

                    {
                        "n": "播放量",
                        "v": "view"
                    },

                    {
                        "n": "投稿时间",
                        "v": "pubtime"
                    }



                ]
            },
                {
                    "key": "mlid",
                    "name": "收藏夹分区",
                    "value": [
                    ]
                }],
         "cosplay": [{
                "key": "order",
                "name": "排序",
                "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }],





















            "频道": [
            
                    {"key": "cid", "name": "分类",
                    "value":[{'n': '生活', 'v': '生活'},{'n': '搞笑', 'v': '搞笑'}, {'n': '美食', 'v': '美食'}, {'n': '鬼畜', 'v': '鬼畜'}, {'n': '美妆', 'v': '美妆'}, {'n': 'mmd', 'v': 'mmd'}, 
                            {'n': '科普', 'v': '科普'}, {'n': 'COSPLAY', 'v': 'COSPLAY'}, {'n': '漫展', 'v': '漫展'}, {'n': 'MAD', 'v': 'MAD'}, {'n': '手书', 'v': '手书'}, 
                            {'n': '穿搭', 'v': '穿搭'}, {'n': '发型', 'v': '发型'}, {'n': '化妆教程', 'v': '化妆教程'}, 
                            {'n': '电音', 'v': '电音'}, {'n': '欧美音乐', 'v': '欧美音乐'}, {'n': '中文翻唱', 'v': '中文翻唱'}, {'n': '洛天依', 'v': '洛天依'}, {'n': '翻唱', 'v': '翻唱'}, {'n': '日文翻唱', 'v': '日文翻唱'}, 
                            {'n': '科普', 'v': '科普'}, {'n': '技术宅', 'v': '技术宅'}, {'n': '历史', 'v': '历史'}, {'n': '科学', 'v': '科学'}, {'n': '人文', 'v': '人文'}, {'n': '科幻', 'v': '科幻'}, 
                            {'n': '手机', 'v': '手机'}, {'n': '手机评测', 'v': '手机评测'}, {'n': '电脑', 'v': '电脑'}, {'n': '摄影', 'v': '摄影'}, {'n': '笔记本', 'v': '笔记本'}, {'n': '装机', 'v': '装机'}, 
                            {'n': '课堂教育', 'v': '课堂教育'}, {'n': '公开课', 'v': '公开课'}, {'n': '演讲', 'v': '演讲'}, {'n': 'PS教程', 'v': 'PS教程'}, {'n': '编程', 'v': '编程'}, {'n': '英语学习', 'v': '英语学习'}, 
                            {'n': '喵星人', 'v': '喵星人'}, {'n': '萌宠', 'v': '萌宠'}, {'n': '汪星人', 'v': '汪星人'}, {'n': '大熊猫', 'v': '大熊猫'}, {'n': '柴犬', 'v': '柴犬'},{'n': '田园犬', 'v': '田园犬'}, {'n': '吱星人', 'v': '吱星人'}, 
                            {'n': '美食', 'v': '美食'}, {'n': '甜点', 'v': '甜点'}, {'n': '吃货', 'v': '吃货'}, {'n': '厨艺', 'v': '厨艺'}, {'n': '烘焙', 'v': '烘焙'}, {'n': '街头美食', 'v': '街头美食'}, 
                            {'n': 'A.I.Channel', 'v': 'A.I.Channel'}, {'n': '虚拟UP主', 'v': '虚拟UP主'}, {'n': '神楽めあ', 'v': '神楽めあ'}, {'n': '白上吹雪', 'v': '白上吹雪'}, {'n': '婺源', 'v': '婺源'}, {'n': 'hololive', 'v': 'hololive'}, {'n': 'EXO', 'v': 'EXO'}, {'n': '防弹少年团', 'v': '防弹少年团'}, {'n': '肖战', 'v': '肖战'}, {'n': '王一博', 'v': '王一博'}, {'n': '易烊千玺', 'v': '易烊千玺'}, {'n': '赵今麦', 'v': '赵今麦'}, 
                            {'n': '宅舞', 'v': '宅舞'}, {'n': '街舞', 'v': '街舞'}, {'n': '舞蹈教学', 'v': '舞蹈教学'}, {'n': '明星舞蹈', 'v': '明星舞蹈'}, {'n': '韩舞', 'v': '韩舞'}, {'n': '古典舞', 'v': '古典舞'}, 
                            {'n': '旅游', 'v': '旅游'}, {'n': '绘画', 'v': '绘画'}, {'n': '手工', 'v': '手工'}, {'n': 'vlog', 'v': 'vlog'}, {'n': 'DIY', 'v': 'DIY'}, {'n': '手绘', 'v': '手绘'}, 
                            {'n': '综艺', 'v': '综艺'}, {'n': '国家宝藏', 'v': '国家宝藏'}, {'n': '脱口秀', 'v': '脱口秀'}, {'n': '日本综艺', 'v': '日本综艺'}, {'n': '国内综艺', 'v': '国内综艺'}, {'n': '人类观察', 'v': '人类观察'}, 
                            {'n': '影评', 'v': '影评'}, {'n': '电影解说', 'v': '电影解说'}, {'n': '影视混剪', 'v': '影视混剪'}, {'n': '影视剪辑', 'v': '影视剪辑'}, {'n': '漫威', 'v': '漫威'}, {'n': '超级英雄', 'v': '超级英雄'}, {'n': '影视混剪', 'v': '影视混剪'}, {'n': '影视剪辑', 'v': '影视剪辑'},
                            {'n': '诸葛亮', 'v': '诸葛亮'}, {'n': '韩剧', 'v': '韩剧'}, {'n': '王司徒', 'v': '王司徒'}, {'n': '泰剧', 'v': '泰剧'},
                            {'n': '郭德纲', 'v': '郭德纲'}, {'n': '相声', 'v': '相声'}, {'n': '张云雷', 'v': '张云雷'}, {'n': '秦霄贤', 'v': '秦霄贤'}, {'n': '孟鹤堂', 'v': '孟鹤堂'}, {'n': '岳云鹏', 'v': '岳云鹏'}, {'n': '假面骑士', 'v': '假面骑士'}, {'n': '特摄', 'v': '特摄'}, {'n': '奥特曼', 'v': '奥特曼'}, {'n': '迪迦奥特曼', 'v': '迪迦奥特曼'}, {'n': '超级战队', 'v': '超级战队'}, {'n': '铠甲勇士', 'v': '铠甲勇士'}, 
                            {'n': '健身', 'v': '健身'}, {'n': '篮球', 'v': '篮球'}, {'n': '体育', 'v': '体育'}, {'n': '帕梅拉', 'v': '帕梅拉'}, {'n': '极限运动', 'v': '极限运动'}, {'n': '足球', 'v': '足球'}, {'n': '星海', 'v': '星海'}, 
                            {'n': '张召忠', 'v': '张召忠'}, {'n': '航母', 'v': '航母'}, {'n': '航天', 'v': '航天'}, {'n': '导弹', 'v': '导弹'}, {'n': '战斗机', 'v': '战斗机'}]
},
                 {
                        "key": "order",
                        "name": "排序",
                        "value": [

                 {
                        "n": "综合排序",
                        "v": "totalrank"
                    },

                    {
                        "n": "最新发布",
                        "v": "pubdate"
                    },

                    {
                        "n": "最多点击",
                        "v": "click"
                    },
                     {
                        "n": "最多收藏",
                        "v": "stow"
                    },



                    {
                        "n": "最多弹幕",
                        "v": "dm"
                    },



                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                            "n": "60分钟以上",
                            "v": "4"
                        },

                        {
                            "n": "30~60分钟",
                            "v": "3"
                        },
                        {
                            "n": "5~30分钟",
                            "v": "2"
                        },
                        {
                            "n": "5分钟以下",
                            "v": "1"
                        }
                    ]
                }
            ],
        }
    }
    header = {
                "Referer": "https://www.bilibili.com",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
            }

    def localProxy(self, param):


        return [200, "video/MP2T", action, ""]


if __name__ == '__main__':
    a=Spider()
    print(a.config['filter'].get('收藏夹'))

    #print(a.get_live(pg=1,parent_area_id='0'))

    a.box_video_type='直播'
    print(a.detailContent( ['7553185']))


    print(a.playerContent('flag', '7553185_12368303#', 'vipFlags'))



    #print(a.get_fav(pg='1',order='mtime',extend={}))
