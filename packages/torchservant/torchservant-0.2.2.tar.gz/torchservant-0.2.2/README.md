# TorchServant

[中文版本](https://github.com/QixuanAI/pytorch_AI_Engine/blob/master/README_zh-CN.md) | English Version

> **TorchServant is still in design and development stage, and more modules may be added.
Welcome interested friends to join this project.````**

TorchServant is an assembly helping quickly development for [PyTorch](https://pytorch.org) users.
The essential design idea of torchservant is to liberate researchers from tedious repetitions 
such as save&load checkpoints, make records, manage GPUs, etc.
It could help users focus on the core pipelines of design neural networks, including
**design models**,
**choose hyper-parameters**,
**design loss functions and optimizers**,
**train models**,
**evaluate models**,
and etc.



## Packages

TorchServant contains the following components:

| Package Name  |                         Explaination                         |
| :-----------: | :----------------------------------------------------------: |
|   cfgenator   |                   Configure file generator                   |
| modelservant  | Manage weights files and checkpoints, keep training process continuous. |
|  procmonitor  | API for visdom and tensorboard, visualize diagrams, illustrations and progresses. |
|     stats     | Resource statistics on GPUs, memories, cpu, and consumed time. |
| classicmodels |        Include AlexNet, VGG, Resnet, Inception, etc.         |
| visualfeature | Visualize feature maps during training and evaluation process. |
| weightransfer | An Qt-based visual tool to transfer weights between different models. |

## Install

```bash
pip install torchservant
```

## Example