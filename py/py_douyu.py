#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

class Spider(Spider):
	def getName(self):
		return "斗鱼"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"星秀": "xingxiu",
            "二次元": "ecy",
            "颜值": "yz",
			"一起看": "yqk"
			
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
		result = {}
		url = 'https://m.douyu.com/api/room/list?type=yqk&page=1'.format()
		rsp = self.fetch(url)
		content = rsp.text
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['list']
		for vod in vodList:
			aid = vod['rid']
			title = vod['roomName'].strip()
			img = vod['roomSrc'].strip()
			remark = (vod['nickname']).strip()
			videos.append({
				"vod_id": aid,
				"vod_name": title,
				"vod_pic": img,
				"vod_remarks": remark
			})
		result['list'] = videos
		
		return result
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url = 'https://m.douyu.com/api/room/list?type={0}&page={1}'.format(tid, pg)
		rsp = self.fetch(url)
		content = rsp.text
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['list']
		for vod in vodList:
			aid = vod['rid']
			title = vod['roomName'].strip()
			img = vod['roomSrc'].strip()
			remark = (vod['nickname']).strip()
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
	def detailContent(self,array):
		aid = array[0]
		url = "http://live.yj1211.work/api/live/getRoomInfo?platform=douyu&roomId={0}".format(aid)
		rsp = self.fetch(url)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		title = jo['roomName']
		pic = jo['roomPic']
		desc = str(jo['online'])
		dire = jo['ownerName']
		typeName = jo['categoryName']
		remark = jo['categoryName']
		vod = {
			"vod_id": aid,
			"vod_name": title,
			"vod_pic": pic,
			"type_name": typeName,
			"vod_year": "",
			"vod_area": "",
			"vod_remarks": remark,
			"vod_actor": '在线人数:' + desc,
			"vod_director": dire,
			"vod_content": ""
		}
		playUrl = '原画' + '${0}#'.format(aid)
		vod['vod_play_from'] = '斗鱼直播'
		vod['vod_play_url'] = playUrl

		result = {
			'list': [
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		result = {}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}

		url = 'http://live.yj1211.work:8013/api/live/getRealUrlMultiSource?platform=douyu&roomId={0}'.format(id)
		rsp = self.fetch(url)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']['线路5'][0]
		ja = jo['playUrl']
		url = ja

		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
		}
		result["contentType"] = 'video/x-flv'
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	config = {
		"player": {},
		"filter": {}
	}
	header = {}
	def localProxy(self,param):
		action = {
			'url':'',
			'header':'',
			'param':'',
			'type':'string',
			'after':''
		}
		return [200, "video/MP2T", action, ""]