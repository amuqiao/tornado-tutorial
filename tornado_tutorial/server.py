# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
__author__ = 'wangqiao'
__date__ = '2017/9/21 下午5:45'

import os
import logging.config
from tornado.options import define, options
from login_service import consts

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

define('port', default=consts.PORT, type=int, help='app listen port')
define('debug', default=consts.DEBUG, help='debug option')
define('base_dir', default=BASE_DIR, help='put the config path here')


def logging_init():
    config_path = os.path.join(options.base_dir, 'config')
    log_template = os.path.join(config_path, 'loggin.conf')
    if not os.path.exists(log_template):
        return
    log_path = os.path.join(options.base_dir, ('%d' % options.port), 'logs')
    log_config_file = os.path.join(options.base_dir, ('%d' % options.port),
                                   'loggin.conf')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    with open(log_template, 'r') as f0:
        values = f0.read()
        with open(log_config_file, 'w') as f1:
            f1.write(values.format(log_path=log_path))
    logging.config.fileConfig(log_config_file)



def app_init():
    from login_service.api.urls import urls
    from tornado.web import Application
    from tornado.httpserver import HTTPServer
    app = Application(urls, debug=options.debug)
    server = HTTPServer(app, xheaders=True)
    server.listen(options.port)
    print("http://127.0.0.1:%d" % options.port)


def main():
    options.parse_command_line()
    logging_init()
    app_init()
    import tornado.ioloop
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()


if __name__ == '__main__':
    main()
