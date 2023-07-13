class Config(object):
    pass

class  ProdConfig(Config):
    pass

class DevConfig(Config):
    debug = True