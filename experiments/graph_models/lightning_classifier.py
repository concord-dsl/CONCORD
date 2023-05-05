import torch
import pytorch_lightning as pl
from torch.optim import Adam
import torchmetrics

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ConcordClassifier(pl.LightningModule):
    def __init__(self, graph_model, loss_func, lr=1e-3, weight_decay=5e-4):
        super().__init__()
        self.save_hyperparameters()
        #### Graph encoder (GGNN, GATv2, GCN)
        self.graph_model = graph_model
        #### loss function
        self.loss_func = loss_func
        #### Metrics
        self.acc = torchmetrics.Accuracy(task='binary')
        self.f1 = torchmetrics.F1Score(task='binary')
        self.mcc = torchmetrics.MatthewsCorrCoef(task='binary')
        self.p = torchmetrics.classification.BinaryPrecision()
        self.r = torchmetrics.classification.BinaryRecall()

        self.acc_val = torchmetrics.Accuracy(task='binary')
        self.f1_val = torchmetrics.F1Score(task='binary')
        self.mcc_val = torchmetrics.MatthewsCorrCoef(task='binary')
        self.p_val = torchmetrics.classification.BinaryPrecision()
        self.r_val = torchmetrics.classification.BinaryRecall()

        self.acc_test = torchmetrics.Accuracy(task='binary')
        self.f1_test = torchmetrics.F1Score(task='binary')
        self.mcc_test = torchmetrics.MatthewsCorrCoef(task='binary')
        self.p_test = torchmetrics.classification.BinaryPrecision()
        self.r_test = torchmetrics.classification.BinaryRecall()
        #### Optimizer params
        self.lr=lr
        self.weight_decay=weight_decay
    

    def forward(self, x):
        x = self.graph_model(x)

        return x

    def training_step(self, batch, batch_idx):
        g, y = batch
        logits = self.graph_model(g)
        y = y.type(torch.LongTensor)
        y = y.to(device)
        loss = self.loss_func(logits, y)
        preds = torch.argmax(logits, dim=1)
        # Accumulate Accuracy, F1 and MCC (Training)
        self.log('train_loss', loss, on_epoch=True)
        self.acc(preds, y)
        self.f1(preds, y)
        self.mcc(preds, y)
        self.p(preds, y)
        self.r(preds, y)

        return loss
    
    def validation_step(self, batch, batch_idx):
        g, y = batch
        logits = self.graph_model(g)
        y = y.type(torch.LongTensor)
        y = y.to(device)
        loss = self.loss_func(logits, y)
        preds = torch.argmax(logits, dim=1)
        # Accumulate Accuracy, F1 and MCC (Validation)
        self.log('val_loss', loss, on_epoch=True)
        val_acc = self.acc_val(preds, y)
        val_f1 = self.f1_val(preds, y)
        val_mcc = self.mcc_val(preds, y)
        val_p = self.p_val(preds, y)
        val_r = self.r_val(preds, y)

        return loss
    
    def test_step(self, batch, batch_idx):
        g, y = batch
        logits = self.graph_model(g)
        y = y.type(torch.LongTensor)
        y = y.to(device)
        loss = self.loss_func(logits, y)
        preds = torch.argmax(logits, dim=1)
        acc = self.acc_test(preds, y)
        f1 = self.f1_test(preds, y)
        mcc = self.mcc_test(preds, y)
        p = self.p_test(preds, y)
        r = self.r_test(preds, y)
        self.log('test_loss', loss,  on_epoch=True, logger=True)
        self.log('test_acc', acc,  on_epoch=True, logger=True)
        self.log('test_f1', f1,  on_epoch=True, logger=True)
        self.log('test_mcc', mcc,  on_epoch=True, logger=True)
        self.log('test_precision', p,  on_epoch=True, logger=True)
        self.log('test_recall', r,  on_epoch=True, logger=True)


        return loss
    
    def on_train_epoch_end(self):
        # Compute metrics
        t_acc = self.acc.compute()
        t_f1 = self.f1.compute()
        t_mcc = self.mcc.compute()
        t_precision = self.p.compute()
        t_recall = self.r.compute()
        self.log('train_acc', t_acc)
        self.log('train_f1', t_f1)
        self.log('train_mcc', t_mcc)
        self.log('train_precision', t_precision)
        self.log('train_mcc', t_recall)
        
        self.acc.reset()
        self.f1.reset()
        self.mcc.reset()
        self.p.reset()
        self.r.reset()


        
    def on_validation_epoch_end(self):
        v_acc =  self.acc_val.compute()
        v_f1 = self.f1_val.compute()
        v_mcc = self.mcc_val.compute()
        v_precision = self.p_val.compute()
        v_recall = self.r_val.compute()
        self.log('val_acc',v_acc)
        self.log('val_f1', v_f1)
        self.log('val_mcc', v_mcc)
        self.log('val_precision', v_precision)
        self.log('val_recall', v_recall)
        
        self.acc_val.reset()
        self.f1_val.reset()
        self.mcc_val.reset()
        self.r_val.reset()
        self.p_val.reset()

        print(f"\nValidation accuracy: {v_acc}, "\
    f"f1: {v_f1}, mcc: {v_mcc}, precision: {v_precision}, recall: {v_recall}")
        

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=1e-3, weight_decay=1e-2)
        return optimizer