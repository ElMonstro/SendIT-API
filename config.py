import os

class Config:
    """config class."""
    DEBUG = False
    SECRET = 'Iam254mbaya'
    
class DevConfig(Config):
    """Development"""
    DEBUG = True
    DB_URL = os.getenv('DB_URL')

class DeploymentConfig(Config):
    """Deployment Config"""
    SECRET = os.getenv('SECRET')
    DB_URL = os.getenv('DB_URL')

class TestConfig(Config):
    """Testing config"""
    DEBUG = True
    DB_URL = os.getenv('TEST_DB_URL')

config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'deploy': DeploymentConfig
}