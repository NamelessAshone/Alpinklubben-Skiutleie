# -*- coding: utf-8 -*-

from app import create_app

config_filename = 'config.development'
app = create_app(config_filename)

if __name__ == '__main__':
    app.run()
