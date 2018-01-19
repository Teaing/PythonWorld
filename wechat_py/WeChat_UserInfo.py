from wechatpy.oauth import WeChatOAuth
from wechatpy.oauth import WeChatOAuthException
from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatClientException

class WeChat_UserInfo:
	def __init__(self):
		self.APPID = 'xxx'
		self.TOKEN = 'xxx'
		self.AESKEY = 'xxx'
		self.APPSECRET = 'xxx'
		self.REDIRECT_URL = 'http://xxxx.xxx.com/zwx/call'


	def GetAuthUrl(self):
		WeChatOAuthCall = WeChatOAuth(app_id=self.APPID,secret=self.APPSECRET,redirect_uri=self.REDIRECT_URL,scope='snsapi_base',state='state')
		return WeChatOAuthCall.authorize_url

	def CallBack(self,code):
		OAuth = WeChatOAuth(app_id=self.APPID,secret=self.APPSECRET,redirect_uri='')
		try:
			OAuth.fetch_access_token(code=code)
		except WeChatOAuthException as e:
			return False
		openid = OAuth.open_id
		UserInfo = OAuth.get_user_info()
		json_data = {
			'openid': openid,
			'nickname': UserInfo['nickname'],
			'pic': UserInfo['headimgurl'],
			'openid2': UserInfo['openid'],
		}
		return json_data

	def get_all_followers(self):
		client = WeChatClient(self.APPID, self.APPSECRET)
		followers = client.user.get_followers()
		try:
			return followers
		except WeChatClientException as e:
			return False
