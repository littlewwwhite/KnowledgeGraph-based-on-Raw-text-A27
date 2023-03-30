import argparse, os, torch
import random
import numpy as np
from utils.data import build_data
from trainer.trainer import Trainer
from models.setpred4RE import SetPred4RE


def str2bool(v):
    return v.lower() in ('true')


def add_argument_group(name):
    arg = parser.add_argument_group(name)
    return arg


def get_args():
    args, unparsed = parser.parse_known_args()
    if len(unparsed) > 1:
        print("Unparsed args: {}".format(unparsed))
    return args, unparsed


def shuffle(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    random.shuffle(lines)
    with open(path, 'w') as f:
        f.writelines(lines)

def split_data(path, train_path, valid_path, test_path):
    with open(path, 'r') as f:
        lines = f.readlines()
    train_lines = lines[:int(len(lines) * 0.4)]
    valid_lines = lines[int(len(lines) * 0.4):int(len(lines) * 0.6)]
    test_lines = lines[int(len(lines) * 0.6):]
    with open(train_path, 'w') as f:
        f.writelines(train_lines)
    with open(valid_path, 'w') as f:
        f.writelines(valid_lines)
    with open(test_path, 'w') as f:
        f.writelines(test_lines)

def set_seed(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    data_arg = add_argument_group('Data')
    
    data_arg.add_argument('--dataset_name', type=str, default="NYT-exact")
    data_arg.add_argument('--all_file', type=str, default="/data_F/zhijian/fuchuang-kg/SPN4RE/data/zhijian_data_v1/base_filtered.json")
    data_arg.add_argument('--train_file', type=str, default="/data_F/zhijian/fuchuang-kg/SPN4RE/data/zhijian_data_v1/train.json")
    data_arg.add_argument('--valid_file', type=str, default="/data_F/zhijian/fuchuang-kg/SPN4RE/data/zhijian_data_v1/valid.json")
    data_arg.add_argument('--test_file', type=str, default="/data_F/zhijian/fuchuang-kg/SPN4RE/data/zhijian_data_v1/test.json")
    # data_arg.add_argument('--train_file', type=str, default="./data/NYT/exact_data/train.json")
    # data_arg.add_argument('--valid_file', type=str, default="./data/NYT/exact_data/valid.json")
    # data_arg.add_argument('--test_file', type=str, default="./data/NYT/exact_data/test.json")
    
    # data_arg.add_argument('--dataset_name', type=str, default="NYT-partial")
    # data_arg.add_argument('--train_file', type=str, default="./data/NYT/casrel_data/new_train.json")
    # data_arg.add_argument('--valid_file', type=str, default="./data/NYT/casrel_data/new_valid.json")
    # data_arg.add_argument('--test_file', type=str, default="./data/NYT/casrel_data/new_test.json")
    
    # data_arg.add_argument('--dataset_name', type=str, default="WebNLG")
    # data_arg.add_argument('--train_file', type=str, default="./data/WebNLG/clean_WebNLG/new_train.json")
    # data_arg.add_argument('--valid_file', type=str, default="./data/WebNLG/clean_WebNLG/new_valid.json")
    # data_arg.add_argument('--test_file', type=str, default="./data/WebNLG/clean_WebNLG/new_test.json")

    data_arg.add_argument('--generated_data_directory', type=str, default="./data/generated_data/")
    data_arg.add_argument('--generated_param_directory', type=str, default="./data/generated_data/model_param/")
    data_arg.add_argument('--bert_directory', type=str, default="./bert_base_cased/")
    data_arg.add_argument("--partial", type=str2bool, default=False)
    learn_arg = add_argument_group('Learning')
    learn_arg.add_argument('--model_name', type=str, default="Set-Prediction-Networks")
    learn_arg.add_argument('--num_generated_triples', type=int, default=10)
    learn_arg.add_argument('--num_decoder_layers', type=int, default=3)
    learn_arg.add_argument('--matcher', type=str, default="avg", choices=['avg', 'min'])
    learn_arg.add_argument('--na_rel_coef', type=float, default=1)
    learn_arg.add_argument('--rel_loss_weight', type=float, default=1)
    learn_arg.add_argument('--head_ent_loss_weight', type=float, default=2)
    learn_arg.add_argument('--tail_ent_loss_weight', type=float, default=2)
    learn_arg.add_argument('--fix_bert_embeddings', type=str2bool, default=True)
    learn_arg.add_argument('--batch_size', type=int, default=8)
    learn_arg.add_argument('--max_epoch', type=int, default=50)
    learn_arg.add_argument('--gradient_accumulation_steps', type=int, default=1)
    learn_arg.add_argument('--decoder_lr', type=float, default=2e-5)
    learn_arg.add_argument('--encoder_lr', type=float, default=1e-5)
    learn_arg.add_argument('--lr_decay', type=float, default=0.01)
    learn_arg.add_argument('--weight_decay', type=float, default=1e-5)
    learn_arg.add_argument('--max_grad_norm', type=float, default=0)
    learn_arg.add_argument('--optimizer', type=str, default='AdamW', choices=['Adam', 'AdamW'])
    evaluation_arg = add_argument_group('Evaluation')
    evaluation_arg.add_argument('--n_best_size', type=int, default=100)
    evaluation_arg.add_argument('--max_span_length', type=int, default=12) #NYT webNLG 10
    misc_arg = add_argument_group('MISC')
    misc_arg.add_argument('--refresh', type=str2bool, default=False)
    misc_arg.add_argument('--use_gpu', type=str2bool, default=True)
    misc_arg.add_argument('--visible_gpu', type=int, default=0)
    misc_arg.add_argument('--random_seed', type=int, default=1)



    args, unparsed = get_args()

    # shuffle(args.all_file)
    # split_data(args.all_file, args.train_file, args.valid_file, args.test_file)

    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.visible_gpu)
    for arg in vars(args):
        print(arg, ":",  getattr(args, arg))
    set_seed(args.random_seed)
    data = build_data(args)
    model = SetPred4RE(args, data.relational_alphabet.size())
    trainer = Trainer(model, data, args)
    data.relational_alphabet.save(args.generated_data_directory, 'alphabet')
    trainer.train_model()
