import numpy as np
import torch
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader, random_split

from constants import HEIGHT, WIDTH, DIM
from decoder.decoder import Decoder
from encoder.encoder import Encoder

data_dir = 'dataset'

train_dataset = torchvision.datasets.CIFAR100(data_dir, train=True, download=True)
test_dataset = torchvision.datasets.CIFAR100(data_dir, train=False, download=True)

train_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((HEIGHT, WIDTH))
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((HEIGHT, WIDTH))
])

train_dataset.transform = train_transform
test_dataset.transform = test_transform

m = len(train_dataset)

train_data, val_data = random_split(train_dataset, [int(m - m * 0.2), int(m * 0.2)])
batch_size = 256

train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size)
valid_loader = torch.utils.data.DataLoader(val_data, batch_size=batch_size)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

loss_fn = torch.nn.MSELoss()
torch.manual_seed(0)

quantization_level = 5

encoder = Encoder(encoded_space_dim=DIM, quantization_level=quantization_level, is_training=True)
decoder = Decoder(encoded_space_dim=DIM)
params_to_optimize = [
    {'params': encoder.parameters()},
    {'params': decoder.parameters()}
]
optim = torch.optim.Adam(params_to_optimize, lr=0.001, weight_decay=1e-05)
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print(f'Selected device: {device}')

# Move both the encoder and the decoder to the selected device
encoder.to(device)
decoder.to(device)


def train_epoch(encoder, decoder, device, dataloader, loss_fn, optimizer):
    encoder.train()
    decoder.train()
    train_loss = []
    for image_batch, _ in dataloader:
        print(image_batch.shape)
        image_batch = image_batch.to(device)
        encoded_data = encoder(image_batch)
        decoded_data = decoder(encoded_data)
        loss = loss_fn(decoded_data, image_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_loss.append(loss.detach().cpu().numpy())

    return np.mean(train_loss)


def test_epoch(encoder, decoder, device, dataloader, loss_fn):
    encoder.eval()
    decoder.eval()
    with torch.no_grad():
        conc_out = []
        conc_label = []
        for image_batch, _ in dataloader:
            image_batch = image_batch.to(device)
            encoded_data = encoder(image_batch)
            decoded_data = decoder(encoded_data)
            conc_out.append(decoded_data.cpu())
            conc_label.append(image_batch.cpu())
        conc_out = torch.cat(conc_out)
        conc_label = torch.cat(conc_label)
        val_loss = loss_fn(conc_out, conc_label)
    return val_loss.data


num_epochs = 30
diz_loss = {'train_loss': [], 'val_loss': []}
for epoch in range(num_epochs):
    train_loss = train_epoch(encoder, decoder, device, train_loader, loss_fn, optim)
    val_loss = test_epoch(encoder, decoder, device, test_loader, loss_fn)
    print('\n EPOCH {}/{} \t train loss {} \t val loss {}'.format(epoch + 1, num_epochs, train_loss, val_loss))
    diz_loss['train_loss'].append(train_loss)
    diz_loss['val_loss'].append(val_loss)

torch.save(encoder.state_dict(), f'models/encoder_b_{quantization_level}.sav')
torch.save(decoder.state_dict(), f'models/decoder_b_{quantization_level}.sav')
