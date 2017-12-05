from django.shortcuts import render
from urllib.parse import quote
import requests
from django.http import JsonResponse
from allauth.socialaccount.admin import SocialApp
from requests_oauthlib import OAuth1

def twitt(request):
	search_term = "zm99__"
	query = quote(search_term)
	url = "https://api.twitter.com/1.1/search/tweets.json?q=%s"%(query)
	

	user = request.user
	social_account = user.socialaccount_set.get(user=user.id)
	social_token = social_account.socialtoken_set.get(account=social_account.id)

	token = social_token.token
	token_secret = social_token.token_secret

	social_app = SocialApp.objects.get(provider=social_account.provider)
	client_id = social_app.client_id 
	client_secret = social_app.secret

	auth_value = OAuth1(client_id, client_secret, token, token_secret)

	resp = requests.get(url, auth=auth_value)

	return JsonResponse(resp.json(), safe= False)