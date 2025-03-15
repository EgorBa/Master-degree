import torch
from PIL import Image
import torchvision.transforms as transforms

from constants import HEIGHT, WIDTH, DIM
from data_storage.data_storage import DataStorage
from encoder.encoder import Encoder
from huffman.codec import HuffmanCodec
from quantization.quantization import Quantization
from utils import get_model_name_by_quantization_level


def encode_image_and_save(path_to_image, quantization_level):
    path_to_encode_file = "file.txt"
    encoded_image, codes = encode_image(path_to_image=path_to_image,
                                        path_to_model=get_model_name_by_quantization_level(quantization_level, True),
                                        quantization_level=quantization_level)
    d = DataStorage(path_to_encode_file)
    d.write_to_file(encoded_image, codes, quantization_level)
    return path_to_encode_file


def encode_image(path_to_image, path_to_model, quantization_level):
    img = Image.open(path_to_image)
    transform = transforms.Compose([
        transforms.PILToTensor(),
        transforms.Resize((HEIGHT, WIDTH))
    ])
    img_tensor = transform(img).unsqueeze(0).float()

    encoder = Encoder(encoded_space_dim=DIM, quantization_level=quantization_level, is_training=False)
    encoder.load_state_dict(torch.load(path_to_model, map_location=torch.device('cpu')))
    encoder.eval()

    with torch.no_grad():
        encoded_data = encoder(img_tensor).numpy()[0]

    q = Quantization(b=quantization_level)
    data = q.quant(encoded_data)

    str_data = ""
    for i in data:
        str_data += str(i) + "|"
    str_data = str_data[:-1]

    h = HuffmanCodec()
    h.culc_huffman_codes(str_data)
    encoded_str = h.encode_str(str_data)
    return encoded_str, h.codes


encode_image_and_save(path_to_image="images/pappers.png", quantization_level=10)
