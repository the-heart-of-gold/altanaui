from pyramid.config import Configurator

from .views.security import SecurityPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings, root_factory='.resources.Root') as config:
        config.include('pyramid_chameleon')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()

        config.set_security_policy(
            SecurityPolicy(
                secret=settings['altanaui.secret']
            ),
        )

    return config.make_wsgi_app()
