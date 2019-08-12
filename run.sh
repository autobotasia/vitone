# Create hparams and the model
model_name=transformer
hparams_set=transformer_tiny
problem_name=translate_vivi
data_dir=./data/$problem_name
tmp_dir=/tmp/$problem_name
vivi_path=./output/$problem_name/avg
decode_hparams="beam_size=4,alpha=0.6"

 export CUDA_VISIBLE_DEVICES=0,1

usage()
{
    echo "usage: run [-g | --gen | -t | --train | -p | --predict | -h]"
}

while [ "$1" != "" ]; do
    case $1 in
        -g | --gen )    echo "Start to run t2t_gendata"
                            python3 ./t2t_datagen.py \
                                --data_dir=$data_dir \
                                --tmp_dir=$tmp_dir \
                                --problem=$problem_name \
                                ;;
        -t | --train )  echo "Start to run t2t_train"
                            python3 ./t2t_trainer.py \
                                --model=$model_name \
                                --hparams_set=$hparams_set \
                                --hparams='batch_size=1024,learning_rate_cosine_cycle_steps=50000' \
                                --train_steps=1000 \
                                --eval_steps=10 \
                                --problem=$problem_name \
                                --data_dir=$data_dir \
                                --output_dir=$vivi_path \
                                --worker_gpu=2 \
                                ;;
	-p | --predict )    echo "Start to run decoder"
                            python3 ./vivi.py \
                                --decode_hparams=$decode_hparams \
                                --model=$model_name \
                                --hparams_set=$hparams_set \
                                --vivi_data_dir=$data_dir \
                                --vivi_problem=$problem_name \
                                --vivi_ckpt=$vivi_path \
                                --vivi_interactively \
                                ;;			
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done


