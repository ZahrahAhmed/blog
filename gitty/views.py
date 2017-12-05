from django.shortcuts import render
from django.http import JsonResponse
import requests


def memberlist(request):
	user = request.user

	social_account = user.socialaccount_set.get(user=user.id)
	social_token = social_account.socialtoken_set.get(account=social_account.id)
	token = social_token.token

	# url = "https://api.github.com/orgs/joinCODED/members"
	url = "https://api.github.com/users/ZahrahAhmed/repos"
	res = requests.get(url, headers={"Authorization": "token "+token})
	return JsonResponse(res.json(), safe=False)