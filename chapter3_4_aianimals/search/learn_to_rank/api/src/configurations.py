import os


class Configurations(object):
    api_title = os.getenv("API_TITLE", "learn_to_rank_lightgbm_ranker")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")

    model_name = os.getenv("MODEL_VERSION", "learn_to_rank_lightgbm_ranker_0.0.0")

    predictor_file_path = os.getenv(
        "PREDICTOR_FILE_PATH",
        "/opt/model/learn_to_rank_ranker.pkl",
    )
    preprocess_likes_scaler_file_path = os.getenv(
        "PREPROCESS_LIKES_SCALER_FILE_PATH",
        "/opt/model/learn_to_rank_ranker_likes_scaler.pkl",
    )
    preprocess_query_animal_category_id_encoder_file_path = os.getenv(
        "PREPROCESS_QUERY_ANIMAL_CATEGORY_ID_ENCODER_FILE_PATH",
        "/opt/model/learn_to_rank_ranker_query_animal_category_id_encoder.pkl",
    )
    preprocess_query_animal_subcategory_id_encoder_file_path = os.getenv(
        "PREPROCESS_QUERY_ANIMAL_SUBCATEGORY_ID_ENCODER_FILE_PATH",
        "/opt/model/learn_to_rank_ranker_query_animal_subcategory_id_encoder.pkl",
    )
    preprocess_query_phrase_encoder_file_path = os.getenv(
        "PREPROCESS_QUERY_PHRASE_ENCODER_FILE_PATH",
        "/opt/model/learn_to_rank_ranker_query_phrase_encoder.pkl",
    )
