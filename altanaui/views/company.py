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
        self.altana_api_secret = request.registry.settings['api.secret1']
        self.altana_base_url = 'https://api.altana.ai/atlas/v1'
        self.altana_headers = {
            'Accept': 'application/json',
            'X-Api-Key': self.altana_api_secret,
        }

    @view_config(route_name='company', renderer='altanaui:templates/company.pt')
    def company(self):
        company_id = self.request.matchdict['altana_canon_id']
        url = self.altana_base_url + '/company/id/' + company_id
        response = requests.get(url, headers=self.altana_headers)
        return response.json()

    @view_config(route_name='match')
    def match(self):
        company_name = self.request.matchdict['company_name'].replace(' ', '%20')
        url = self.altana_base_url + '/company/match/' + company_name
        response = requests.get(url, headers=self.altana_headers)
        return response.json()
