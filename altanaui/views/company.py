import requests
import pycountry
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import notfound_view_config
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
        if response.status_code == 404:
            raise HTTPNotFound()
        json_data = response.json()
        company_data = self.get_company_data(json_data)

        return company_data

    @view_config(route_name='match')
    def match(self):
        company_name = self.request.matchdict['company_name'].replace(' ', '%20')
        url = self.altana_base_url + '/company/match/' + company_name
        response = requests.get(url, headers=self.altana_headers)
        if response.status_code == 404:
            raise HTTPNotFound()
        json_data = response.json()
        company_data = self.get_company_data(json_data)

        return company_data

    @notfound_view_config(renderer='altanaui:templates/404.pt')
    def notfound(self):
        return Response('Not Found', status='404 Not Found')

    def get_company_data(self, json_data):
        company_data = {'altana_canon_id': json_data['altana_canon_id']}
        company_context = {'buyers': self.get_companies(json_data['company_context']['buyers']),
                           'countries_of_destination': self.get_countries(
                               json_data['company_context']['countries_of_destination']),
                           'countries_of_operation': self.get_countries(
                               json_data['company_context']['countries_of_operation']),
                           'countries_of_origin': self.get_countries(
                               json_data['company_context']['countries_of_origin']),
                           'hs_traded': self.get_hs_traded(json_data['company_context']['hs_traded']),
                           'industries': json_data['company_context']['industries'],
                           'number_records': json_data['company_context']['number_records'],
                           'products_received': self.get_products(json_data['company_context']['products_received']),
                           'products_sent': self.get_products(json_data['company_context']['products_sent']),
                           'suppliers': self.get_companies(json_data['company_context']['suppliers']),
                           'trading_partners': self.get_companies(json_data['company_context']['trading_partners']),
                           }
        company_data['company_context'] = company_context
        company_data['company_name'] = json_data['company_name']
        company_data['data_sources'] = json_data['data_sources']
        company_data['restrictions'] = json_data['restrictions']
        company_data['risks'] = json_data['risks']

        return company_data

    def get_companies(self, company_ids):
        companies = []
        for company_id in company_ids:
            url = self.altana_base_url + '/company/id/' + company_id
            response = requests.get(url, headers=self.altana_headers)
            json_data = response.json()
            companies.append({'altana_canon_id': company_id,
                              'company_name': json_data['company_name'].title()})
        return companies

    def get_countries(self, alpha_2_codes):
        countries = []
        for alpha_2_code in alpha_2_codes:
            country = pycountry.countries.get(alpha_2=alpha_2_code)
            print(country)
            countries.append({'alpha_2': country.alpha_2,
                              'alpha_3': country.alpha_3,
                              'name': country.name,
                              'official_name': country.name,
                              #  'official_name': country.official_name,
                              })
        return countries

    def get_hs_traded(self, hs_traded_codes):
        hs_traded = []
        for hs_traded_code in hs_traded_codes:
            url = 'https://www.trade-tariff.service.gov.uk/api/v2/commodities/' + hs_traded_code + '0000'
            response = requests.get(url)
            if response.status_code == 404:
                return hs_traded_codes
            hs_description = response.json()['data']['attributes']['description']
            hs_traded.append({'hs_code': hs_traded_code, 'hs_description': hs_description})
        return hs_traded_codes

    def get_products(self, product_ids):
        products = []
        for product_id in product_ids:
            url = self.altana_base_url + '/product/id/' + product_id
            response = requests.get(url, headers=self.altana_headers)
            json_data = response.json()
            product_name = json_data['name'].title()
            products.append({'product_id': product_id, 'product_name': product_name})
        return products
