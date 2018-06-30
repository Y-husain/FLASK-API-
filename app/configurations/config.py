import os


class Config:
    """parent configuration file
    :returns: configuration object
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """configuration for development"""
    # DEBUG = True
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """configuration for testing with a separate testing database
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True


class StagingConfig(Config):
    """config for staging
    """


class ProductionConfig(Config):
    """ config for production
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}