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
    DB_URL = 'postgres://gjmfftiqogkmro:094234a259032a6aa229e5b2680d98f5c582ade219feac97b263f360010dc709@ec2-54-204-36-249.compute-1.amazonaws.com:5432/d1csuju2i60r9m'

class TestConfig(Config):
    """Testing config"""
    DEBUG = True
    DB_URL = os.getenv('TEST_DB_URL')

config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'deploy': DeploymentConfig
}