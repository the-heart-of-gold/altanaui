def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('match', '/company/match/{company_name}')
    config.add_route('company', '/company/id/{altana_canon_id}')
    #  config.add_route('company', '/company/{altana_canon_id}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
