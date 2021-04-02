import requests

from pyramid.view import (
    view_config,
    view_defaults,
)


@view_defaults(route_name='company', renderer='altanaui:templates/company.pt')
class CompanyViews:
    def __init__(self, request):
        self.request = request
        self.view_name = 'CompanyViews'
        self.logged_in = request.authenticated_userid

    @view_config(route_name='company')
    def company(self):
        base_url = 'https://api.altana.ai/atlas/v1'
        fragment = '/company/match/lloyds'
        api_secret = self.request.registry.settings['api.secret1']
        headers = {
            'Accept': 'application/json',
            'X-Api-Key': api_secret,
        }
        response = requests.get(base_url + fragment, headers=headers)
        return response.json()
