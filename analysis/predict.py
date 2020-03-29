# from __future__ import absolute_import, division, print_function

import argparse
# import glob
import logging
import os
import random

# import numpy as np
import torch
# from torch.utils.data import (DataLoader, RandomSampler, SequentialSampler,
                            #   TensorDataset)
# from torch.utils.data.distributed import DistributedSampler
# from tensorboardX import SummaryWriter
from tqdm import tqdm, trange

from pytorch_transformers import (WEIGHTS_NAME, BertConfig,
                                  BertForSequenceClassification, BertTokenizer,
                                  XLMConfig, XLMForSequenceClassification,
                                  XLMTokenizer, XLNetConfig,
                                  XLNetForSequenceClassification,
                                  XLNetTokenizer)

# from pytorch_transformers import AdamW, WarmupLinearSchedule

from analysis.utils_glue import (compute_metrics, convert_examples_to_features,
                        output_modes, processors)

MODEL_CLASSES = {
    'bert': (BertConfig, BertForSequenceClassification, BertTokenizer),
    'xlnet': (XLNetConfig, XLNetForSequenceClassification, XLNetTokenizer),
    'xlm': (XLMConfig, XLMForSequenceClassification, XLMTokenizer),
}

#changed to never cache
def load_and_cache_examples(args, task, tokenizer, evaluate=True):  #evaluate dafualt changed to true
    def transform_examples_to_hr(exmpls):
        examples_hr = ['[CLS] ' + exp.text_a + ' [SEP] ' + exp.text_b + ' [LABEL] ' + exp.label for exp in exmpls]
        return examples_hr

    processor = processors[task]()
    output_mode = output_modes[task]

    examples=None
    tokenized_examples=None

    logger.info("Creating features from dataset file at %s", args.data_dir)
    label_list = processor.get_labels()
    examples = processor.get_dev_examples(args.data_dir) if evaluate else processor.get_train_examples(args.data_dir)
    features, tokenized_examples = convert_examples_to_features(examples, label_list, args.max_seq_length, tokenizer, output_mode,
        cls_token_at_end=bool(args.model_type in ['xlnet']),            # xlnet has a cls token at the end
        cls_token=tokenizer.cls_token,
        sep_token=tokenizer.sep_token,
        cls_token_segment_id=2 if args.model_type in ['xlnet'] else 1,
        pad_on_left=bool(args.model_type in ['xlnet']),                 # pad on the left for xlnet
        pad_token_segment_id=4 if args.model_type in ['xlnet'] else 0)

    # Convert to Tensors and build dataset
    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
    if output_mode == "classification":
        all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.long)
    elif output_mode == "regression":
        all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.float)

    dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
    return dataset, transform_examples_to_hr(examples) 


def evaluate(args, model, tokenizer, prefix=""):
    # Loop to handle MNLI double evaluation (matched, mis-matched)
    eval_task_names = ("mnli", "mnli-mm") if args.task_name == "mnli" else (args.task_name,)
    eval_outputs_dirs = (args.output_dir, args.output_dir + '-MM') if args.task_name == "mnli" else (args.output_dir,)

    # results = {}
    for eval_task, eval_output_dir in zip(eval_task_names, eval_outputs_dirs):
        eval_dataset, _ = load_and_cache_examples(args, eval_task, tokenizer, evaluate=True)

        if not os.path.exists(eval_output_dir) and args.local_rank in [-1, 0]:
            os.makedirs(eval_output_dir)

        args.eval_batch_size = args.per_gpu_eval_batch_size * max(1, args.n_gpu)
        # Note that DistributedSampler samples randomly
        eval_sampler = SequentialSampler(eval_dataset) #eval_sampler changed to never distributed 
        eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=args.eval_batch_size)

        # Eval!
        logger.info("***** Running evaluation {} *****".format(prefix))
        logger.info("  Num examples = %d", len(eval_dataset))
        logger.info("  Batch size = %d", args.eval_batch_size)
        # eval_loss = 0.0
        # nb_eval_steps = 0
        preds = None
        # out_label_ids = None
        for batch in tqdm(eval_dataloader, desc="Evaluating"):
            model.eval()
            batch = tuple(t.to(args.device) for t in batch)

            with torch.no_grad():
                inputs = {'input_ids':      batch[0],
                          'attention_mask': batch[1],
                          'token_type_ids': batch[2] if args.model_type in ['bert', 'xlnet'] else None,  # XLM don't use segment_ids
                          'labels':         batch[3]}
                outputs = model(**inputs)
                a, logits = outputs[:2]

                # eval_loss += tmp_eval_loss.mean().item()
            # nb_eval_steps += 1
            if preds is None:
                preds = logits.detach().cpu().numpy()
                # out_label_ids = inputs['labels'].detach().cpu().numpy()
            else:
                preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)
                # out_label_ids = np.append(out_label_ids, inputs['labels'].detach().cpu().numpy(), axis=0)

        # eval_loss = eval_loss / nb_eval_steps
        if args.output_mode == "classification":
            preds = np.argmax(preds, axis=1)
        elif args.output_mode == "regression":
            preds = np.squeeze(preds)
        # result = compute_metrics(eval_task, preds, out_label_ids)
        # results.update(result)

        # output_eval_file = os.path.join(eval_output_dir, "eval_results.txt")
        # with open(output_eval_file, "w") as writer:
        #     logger.info("***** Eval results {} *****".format(prefix))
        #     for key in sorted(result.keys()):
        #         logger.info("  %s = %s", key, str(result[key]))
        #         writer.write("%s = %s\n" % (key, str(result[key])))

    return preds

def main():
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--data_dir", default="data/transformed", type=str, required=False,
                        help="The input data dir. Should contain the .tsv files (or other data files) for the task.")
    parser.add_argument("--model_type", default="bert", type=str, required=False,
                        help="Model type selected in the list: " )
    # parser.add_argument("--model_name_or_path", default=None, type=str, required=True,
                        # help="Path to pre-trained model or shortcut name selected in the list: " + ", ".join(ALL_MODELS))
    parser.add_argument("--task_name", default="semeval2014-atsc", type=str, required=False,
                        help="The name of the task to train selected in the list: " + ", ".join(processors.keys()))
    parser.add_argument("--output_dir", default="../model", type=str, required=False,
                        help="The output directory where the model predictions and checkpoints will be written.")
    # # Other parameters
    # parser.add_argument("--config_name", default="", type=str,
    #                     help="Pretrained config name or path if not the same as model_name")
    # parser.add_argument("--tokenizer_name", default="", type=str,
    #                     help="Pretrained tokenizer name or path if not the same as model_name")
    # parser.add_argument("--cache_dir", default="", type=str,
    #                     help="Where do you want to store the pre-trained models downloaded from s3")
    # parser.add_argument("--max_seq_length", default=128, type=int,
    #                     help="The maximum total input sequence length after tokenization. Sequences longer "
    #                             "than this will be truncated, sequences shorter will be padded.")
    # parser.add_argument("--do_train", action='store_true',
    #                     help="Whether to run training.")
    # parser.add_argument("--do_eval", action='store_true',
    #                     help="Whether to run eval on the dev set.")
    # parser.add_argument("--evaluate_during_training", action='store_true',
    #                     help="Rul evaluation during training at each logging step.")
    # parser.add_argument("--do_lower_case", action='store_true',
    #                     help="Set this flag if you are using an uncased model.")

    # parser.add_argument("--per_gpu_train_batch_size", default=8, type=int,
    #                     help="Batch size per GPU/CPU for training.")
    # parser.add_argument("--per_gpu_eval_batch_size", default=8, type=int,
    #                     help="Batch size per GPU/CPU for evaluation.")
    # parser.add_argument('--gradient_accumulation_steps', type=int, default=1,
    #                     help="Number of updates steps to accumulate before performing a backward/update pass.")
    # parser.add_argument("--learning_rate", default=5e-5, type=float,
    #                     help="The initial learning rate for Adam.")
    # parser.add_argument("--weight_decay", default=0.0, type=float,
    #                     help="Weight deay if we apply some.")
    # parser.add_argument("--adam_epsilon", default=1e-8, type=float,
    #                     help="Epsilon for Adam optimizer.")
    # parser.add_argument("--max_grad_norm", default=1.0, type=float,
    #                     help="Max gradient norm.")
    # parser.add_argument("--num_train_epochs", default=3.0, type=float,
    #                     help="Total number of training epochs to perform.")
    # parser.add_argument("--max_steps", default=-1, type=int,
    #                     help="If > 0: set total number of training steps to perform. Override num_train_epochs.")
    # parser.add_argument("--warmup_steps", default=0, type=int,
    #                     help="Linear warmup over warmup_steps.")

    # parser.add_argument('--logging_steps', type=int, default=50,
    #                     help="Log every X updates steps.")
    # parser.add_argument('--save_steps', type=int, default=50,
    #                     help="Save checkpoint every X updates steps.")
    # parser.add_argument("--eval_all_checkpoints", action='store_true',
    #                     help="Evaluate all checkpoints starting with the same prefix as model_name ending and ending with step number")
    # parser.add_argument("--no_cuda", action='store_true',
    #                     help="Avoid using CUDA when available")
    # parser.add_argument('--overwrite_output_dir', action='store_true',
    #                     help="Overwrite the content of the output directory")
    # parser.add_argument('--overwrite_cache', action='store_true',
    #                     help="Overwrite the cached training and evaluation sets")
    # parser.add_argument('--seed', type=int, default=42,
    #                     help="random seed for initialization")

    # parser.add_argument('--fp16', action='store_true',
    #                     help="Whether to use 16-bit (mixed) precision (through NVIDIA apex) instead of 32-bit")
    # parser.add_argument('--fp16_opt_level', type=str, default='O1',
    #                     help="For fp16: Apex AMP optimization level selected in ['O0', 'O1', 'O2', and 'O3']."
    #                             "See details at https://nvidia.github.io/apex/amp.html")
    # parser.add_argument("--local_rank", type=int, default=-1,
    #                     help="For distributed training: local_rank")
    # parser.add_argument('--server_ip', type=str, default='', help="For distant debugging.")
    # parser.add_argument('--server_port', type=str, default='', help="For distant debugging.")
    args = parser.parse_args()


    device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")

    model = model_class.from_pretrained(args.output_dir)
    model.to(args.device)

    tokenizer = tokenizer_class.from_pretrained(args.output_dir)

    return evaluate(args, model, tokenizer)