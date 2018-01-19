from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.oauth import WeChatOAuth
from wechatpy.oauth import WeChatOAuthException
from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatClientException
from WeChat_UserInfo import WeChat_UserInfo
from django.http import HttpResponseRedirect

# Create your views here.

def get_auth(request):
	wechat_info = WeChat_UserInfo()
	back_url = wechat_info.GetAuthUrl()
	print back_url
	return redirect(to=back_url)

def call(request):
	code = request.GET.get('code')
	next_url = request.GET.get('state')
	if not code:
		return HttpResponse('You Deny Access...')

	wechat_info = WeChat_UserInfo()
	wechat_result = wechat_info.CallBack(code)
	return JsonResponse(wechat_result)
