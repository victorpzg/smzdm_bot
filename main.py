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
        self.session.headers['Cookie'] = '__ckguid=VkW55HaOQ9Sx3yR72qBxBK5; r_sort_type=score; __jsluid_s=ef0f559c6fb1aef3e7c403b7eb52d793; smzdm_user_source=750BDD2F8B6AFAF2897257600617C5D0; device_id=2028365440162666547642214110c74a0d9b545f81cf75952396e23976; __jsluid_h=08e325e17f98cd8a57a5315e201289b6; userId=user:5952881280|5952881280; homepage_sug=d; footer_floating_layer=0; ad_date=13; ad_json_feed=%7B%7D; _zdmA.vid=*; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1634098384; zdm_qd=%7B%22referrer%22%3A%22https%3A%2F%2Fgithub.com%2Fvictorpzg%2Fsmzdm_bot%22%7D; __gads=ID=f443fe3f4c50d1a7:T=1627662836:S=ALNI_MYuozN4zQ_UEIjvmXmdfqRCjs3idQ; _gid=GA1.2.562810322.1634098390; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%225952881280%22%2C%22first_id%22%3A%2217abccf76294f1-0e98e18f9ce2a7-6373264-1327104-17abccf762a75e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fgithub.com%2Fvictorpzg%2Fsmzdm_bot%22%7D%2C%22%24device_id%22%3A%2217abccf76294f1-0e98e18f9ce2a7-6373264-1327104-17abccf762a75e%22%7D; sess=AT-wdNP6ZNZXSn1tBVhWhlq6Tw9Tpf5%2BBM63cebgZjvXaj8yK4oN5a4YvRLo25%2BaSulWG8Q30I4zjZ80JAcJ6nuB75OAbiLPuuDBuKcOpExLsOKiEowDsyt3SE1; user=user%3A5952881280%7C5952881280; smzdm_id=5952881280; _zdmA.uid=ZDMA.QfzSwYujH.1634098847.2419200; _ga=GA1.2.964977847.1626665351; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1634098847; bannerCounter=%5B%7B%22number%22%3A1%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A1%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A1%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%5D; amvid=67653031f8123036b69923af6f857eee; _zdmA.time=1634098855832.0.https%3A%2F%2Fwww.smzdm.com%2F; _gat_UA-27058866-1=1; _ga_09SRZM2FDD=GS1.1.1634098384.26.1.1634098888.0'

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
