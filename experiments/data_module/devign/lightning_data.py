from dataset import DevignDataset
import pytorch_lightning as pl
import dgl

class DataModule(pl.LightningDataModule):
    def __init__(self, samples, args, num_workers = 4 , batch_size = 32):
        super().__init__()

        train_split, test_split, val_split = samples
        self.train_split = DevignDataset(train_split, 'train', args)
        self.test_split = DevignDataset(test_split, 'test' , args)
        self.val_split = DevignDataset(val_split, 'valid' , args)

        self.batch_size = batch_size
        self.num_workers = num_workers

    def train_dataloader(self):
        return dgl.dataloading.GraphDataLoader(
        self.train_split,
        batch_size=self.batch_size,
        num_workers=self.num_workers,
        shuffle=True,
        pin_memory=True,
    )

    def val_dataloader(self):
        return dgl.dataloading.GraphDataLoader(
        self.val_split,
        batch_size=self.batch_size,
        num_workers=self.num_workers,
        shuffle=False,
        pin_memory=True,
    )

    def test_dataloader(self):
        return dgl.dataloading.GraphDataLoader(
        self.test_split,
        batch_size=self.batch_size,
        num_workers=self.num_workers,
        shuffle=False
    )
