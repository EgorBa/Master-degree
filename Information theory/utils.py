def get_model_name_by_quantization_level(quantization_level, encode):
    if encode:
        begin = 'en'
    else:
        begin = 'de'
    model_name = f'models/{begin}coder_b_{quantization_level}.sav'
    return model_name
