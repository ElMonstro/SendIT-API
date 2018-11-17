import os

class Config:
    """config class."""
    DEBUG = False
    SECRET = 'Iam254mbaya'
    
class DevConfig(Config):
    """Development"""
    DEBUG = True
    DB_URL = 'postgresql://elmonstro:password@localhost:5432/sendit'

class DeploymentConfig(Config):
    """Deployment Config"""
    SECRET = os.getenv('SECRET')
    DB_URL = os.getenv('DB_URL')

class TestConfig(Config):
    """Testing config"""
    DEBUG = True
    DB_URL = 'postgresql://elmonstro:password@localhost:5432/test_db'

config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'deploy': DeploymentConfig
}