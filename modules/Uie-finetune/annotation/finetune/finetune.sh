
# shell doccona标注文件生成
python doccano.py \
    --doccano_file Uie-finetune/data/doccano.json \
    --task_type ext \
    --save_dir ./data/41line \
    --splits 0.8 0.2 0 \
    --schema_lang ch


# shell finetune-arg 突出的部分为主要修改的部分
export finetuned_model=./checkpoint/model_best_77line_200ep

python -u -m paddle.distributed.launch --gpus "1" finetune.py \
    --device gpu \
    --logging_steps 10 \
    --save_steps 200 \
    --eval_steps 200 \
    --seed 42 \
    --model_name_or_path uie-base \
    --output_dir $finetuned_model \
         --train_path data/77line/train.txt \
         --dev_path data/77line/dev.txt  \
    --max_seq_length 512  \
    --per_device_eval_batch_size 8 \
    --per_device_train_batch_size  8 \
         --num_train_epochs 200 \
    --learning_rate 1e-5 \
    --label_names 'start_positions' 'end_positions' \
    --do_train \
    --do_eval \
    --do_export \
    --export_model_dir $finetuned_model \
    --overwrite_output_dir \
    --disable_tqdm True \
    --metric_for_best_model eval_f1 \
    --load_best_model_at_end  True \
    --save_total_limit 1

