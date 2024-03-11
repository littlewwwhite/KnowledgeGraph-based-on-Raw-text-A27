# Joint Entity and Relation Extraction with Set Prediction Networks
[![GitHub stars](https://img.shields.io/github/stars/DianboWork/SPN4RE?style=flat-square)](https://github.com/DianboWork/SPN4RE/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/DianboWork/SPN4RE?style=flat-square&color=blueviolet)](https://github.com/DianboWork/SPN4RE/network/members)

Source code for [Joint Entity and Relation Extraction with Set Prediction Networks](https://arxiv.org/abs/2011.01675). We would appreciate it if you cite our paper as following:

```
@article{sui2020joint,
  title={Joint Entity and Relation Extraction with Set Prediction Networks},
  author={Sui, Dianbo and Chen, Yubo and Liu, Kang and Zhao, Jun and Zeng, Xiangrong and Liu, Shengping},
  journal={arXiv preprint arXiv:2011.01675},
  year={2020}
}
```
##  Model Training
### Requirement:
```
Python: 3.7   
PyTorch: >= 1.5.0 
Transformers: 2.6.0
```

###  NYT Partial Match
* Note That: Replacing BERT_DIR in the command line with the actual directory of BERT-base-cased in your machine!!!
* 注意：需将命令行中的BERT_DIR替换为你机器中实际存储BERT的目录！！！

```shell
python -m main --bert_directory /data_F/zhijian/fuchuang-kg/SPN4RE/bert_pretrain --num_generated_triples 15 --na_rel_coef 1 --max_grad_norm 1 --max_epoch 10 --max_span_length 10 --visible_gpu 
```

###  NYT Exact Match

```shell
python -m main --bert_directory /data_F/zhijian/fuchuang-kg/SPN4RE/bert_pretrain --num_generated_triples 15 --max_grad_norm 2.5 --na_rel_coef 0.25 --max_epoch 20 --max_span_length 10 --visible_gpu 3
```
or 
```shell
python -m main --bert_directory BERT_DIR --num_generated_triples 15 --max_grad_norm 1 --na_rel_coef 0.5 --max_epoch 100 --max_span_length 10
```

### WebNLG Partial Match
```shell
python -m main --bert_directory BERT_DIR --batch_size 4 --num_generated_triples 10 --na_rel_coef 0.25 --max_grad_norm 20  --max_epoch 100 --encoder_lr 0.00002 --decoder_lr 0.00005 --num_decoder_layers 4 --max_span_length 10 --weight_decay 0.000001 --lr_decay 0.02
```
## Trained Model Parameters
Model parameters can be download in [Baidu Pan](https://pan.baidu.com/s/1nL-qZs16x684d98APVn8FQ) (key: SetP) :sunglasses:
