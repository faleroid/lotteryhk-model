import os

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, '../templates')
    DATA_DIR = os.path.join(BASE_DIR, '../data') 

    MODEL_PATH = os.path.join(BASE_DIR, 'lottery_model.pkl')
    FEATURES_PATH = os.path.join(BASE_DIR, 'model_features.pkl')
    TEST_DATA_PATH = os.path.join(DATA_DIR, 'lottery_test.csv')
    TRAIN_DATA_PATH = os.path.join(DATA_DIR, 'lottery_train.csv')