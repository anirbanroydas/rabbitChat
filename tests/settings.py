import os.path

path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))


settings = {
    # debug: If True the application runs in debug mode
    # 'debug': True,
    #


    # autoreload: If True, the server process will restart when any source
    # files change, as described
    'autorelaod': True,

    # compiled_template_cache: Default is True;
    # if False templates will be recompiled on every request.
    'compiled_template_cache': False,

    # serve_traceback: If true, the default error page will include the
    # traceback of the error.
    'serve_traceback': False,

    # static_hash_cache: Default is True; if False static urls will be
    # recomputed on every request.
    'static_hash_cache': False,


    # gzip: If True, responses in textual formats will be gzipped automatically.
    # 'gzip': True,

    # log_function: This function will be called at the end of every request
    # to log the result (with one argument, the RequestHandler object).
    # The default implementation writes to the logging module's root logger.
    # May also be customized by overriding Application.log_request.
    # 'log_function': function_name,

    # ui_modules and ui_methods:
    # http://www.tornadoweb.org/en/stable/overview.html#ui-modules

    # Used by RequestHandler.get_secure_cookie and set_secure_cookie to sign cookies.
    # 'cookie_secret': 'uxmRinfK8e7HC59jU4QKAGyEsnecPZHuVGUhmtAqHY5rdScC7FM',

    # login_url: The authenticated decorator will redirect to this url
    # if the user is not logged in. Can be further customized by
    # overriding RequestHandler.get_login_url
    # 'login_url': '/login/',

    # xsrf_cookies: If true, Cross-site request forgery protection will be enabled.
    'xsrf_cookies': True,

    # twitter_consumer_key, twitter_consumer_secret,
    # friendfeed_consumer_key, friendfeed_consumer_secret,
    # google_consumer_key, google_consumer_secret,
    # facebook_api_key, facebook_secret
    # Used in the tornado.auth module to authenticate to various APIs.

    # autoescape: Controls automatic escaping for templates.
    # May be set to None to disable escaping, or to the name of a function
    # that all output should be passed through.
    'autoescape': "xhtml_escape",

    # template_path: Directory containing template files.
    # Can be further customized by overriding RequestHandler.get_template_path
    'template_path': path(ROOT, "templates"),

    # static_path: Directory from which static files will be served.
    'static_path': path(ROOT, "static"),

    # static_url_prefix: Url prefix for static files, defaults to "/static/".
    'static_url_prefix': '/static/',

    # static_handler_class, static_handler_args:
    # May be set to use a different handler for static files instead of
    # the default tornado.web.StaticFileHandler.
    # static_handler_args, if set, should be a dictionary of keyword arguments
    # to be passed to the handler's initialize method.
    #
}
