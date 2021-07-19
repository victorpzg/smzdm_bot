"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config
from utils.serverchan_push import push_to_wechat

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = '__ckguid=VkW55HaOQ9Sx3yR72qBxBK5; r_sort_type=score; __jsluid_s=ef0f559c6fb1aef3e7c403b7eb52d793; sajssdk_2015_cross_new_user=1; _zdmA.vid=*; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1626665352; footer_floating_layer=0; ad_date=19; ad_json_feed=%7B%7D; zdm_qd=%7B%7D; _gid=GA1.2.844911543.1626665353; smzdm_user_view=28E888F829251DEC32DB2A1A3496CD30; smzdm_user_source=750BDD2F8B6AFAF2897257600617C5D0; device_id=2028365440162666547642214110c74a0d9b545f81cf75952396e23976; sess=AT-wdNP6ZNZXSn1vQBZJc3RReUsg4Ax2O%2BAvmkemEjNrzcIddlVDVDhGx1XX1qrqe9bqFbbzCwq6JB8OprH%2FjZ2Wdee52B21tVaCsnxn40b0sKqfY6pdHZz2xYd; user=user%3A5952881280%7C5952881280; smzdm_id=5952881280; __jsluid_h=08e325e17f98cd8a57a5315e201289b6; homepage_sug=c; _zdmA.uid=ZDMA.YdHyX1yG1.1626665476.2419200; userId=user:5952881280|5952881280; bannerCounter=%5B%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A1%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A1%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%5D; __gads=ID=f443fe3f4c50d1a7:T=1626665477:S=ALNI_MZd7XoDwyQpoQVE5vBmrKSOgLAuIw; amvid=4aa2599833cdc74bd66915fad8e2859e; _zdmA.time=1626665523010.25719.https%3A%2F%2Fwww.smzdm.com%2F; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%225952881280%22%2C%22first_id%22%3A%2217abccf76294f1-0e98e18f9ce2a7-6373264-1327104-17abccf762a75e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_landing_page%22%3A%22https%3A%2F%2Fwww.smzdm.com%2F%22%7D%2C%22%24device_id%22%3A%2217abccf76294f1-0e98e18f9ce2a7-6373264-1327104-17abccf762a75e%22%7D; _gat_UA-27058866-1=1; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1626665705; _ga=GA1.2.964977847.1626665351; _ga_09SRZM2FDD=GS1.1.1626665352.1.1.1626665722.0'

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content




if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["COOKIES"]
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    print(res)
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY"]
    print('sc_key: ', SERVERCHAN_SECRETKEY)
    if isinstance(SERVERCHAN_SECRETKEY,str) and len(SERVERCHAN_SECRETKEY)>0:
        print('检测到 SCKEY， 准备推送')
        push_to_wechat(text = '什么值得买每日签到',
                        desp = str(res),
                        secretKey = SERVERCHAN_SECRETKEY)
    print('代码完毕')
