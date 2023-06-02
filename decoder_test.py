import torch
from PIL import Image
import numpy as np
from constants import DIM
from data_storage.data_storage import DataStorage
from decoder.decoder import Decoder
from huffman.codec import HuffmanCodec
from quantization.quantization import Quantization
from utils import get_model_name_by_quantization_level


def decode_image_and_save(encode_file):
    path_to_decode_image = "test.png"
    d = DataStorage(encode_file)
    encoded_data = d.read_from_file()
    decode_image(path_to_decode_image, encoded_data)
    return path_to_decode_image


def decode_image(path_to_image, encoded_data):
    codes = encoded_data["codes"]
    data = encoded_data["data"]

    h = HuffmanCodec()
    h.set_huffman_codes(codes)
    encoded_str = h.decode_str_as_array(data)

    quantization_level = encoded_data["quantization_level"]
    q = Quantization(b=quantization_level)
    features = q.dequant(encoded_str)

    features = torch.FloatTensor([features])
    path_to_model = get_model_name_by_quantization_level(quantization_level, False)

    decoder = Decoder(encoded_space_dim=DIM)
    decoder.load_state_dict(torch.load(path_to_model, map_location=torch.device('cpu')))
    decoder.eval()

    with torch.no_grad():
        decoded_data = (decoder(features).squeeze().numpy() * 255).astype(np.uint8)

    decoded_data = np.einsum('ijk->jki', decoded_data)

    data = Image.fromarray(decoded_data)
    data.save(path_to_image)


decode_image_and_save(encode_file="file.txt")
