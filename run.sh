# Create hparams and the model
model_name=transformer
hparams_set=transformer_tiny
vivi_path=./checkpoints/translate_vivi_tiny/avg
decode_hparams="beam_size=2,alpha=0.6"

#python3 ./back_translate.py --lang=vi \
#--decode_hparams=$decode_hparams \
#--model=$model_name \
#--hparams_set=$hparams_set \
#--vien_ckpt=$vien_path \
#--envi_ckpt=$envi_path 
#--backtranslate_interactively

while [ "$1" != "" ]; do
    case $1 in
        -g | --gen )           shift
                                echo "Start to run t2t_gendata"
                                python3 ./t2t_datagen.py \
                                --data_dir=./data/translate_vivi \
                                --tmp_dir=/tmp/translate_vivi \
                                --problem=translate_vivi
                                $@
                                ;;
        -t | --train )    echo "Start tp rim t2t_train"
                            python3 ./t2t_trainer.py \
                                --model='transformer' \
                                --hparams_set=$hparams_set \
                                --hparams='learning_rate_cosine_cycle_steps=50000' \
                                --train_steps=1000 \
                                --eval_steps=10 \
                                --problem=translate_vivi \
                                --data_dir=./data/translate_vivi \
                                --output_dir=./output/translate_vivi
                                --use_tpu=False \
                                --worker_gpus=2 \
                                $@
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done


if [ "$1" == "gen_data" ]; then
    echo "Start to run t2t_gendata"
    python3 ./t2t_datagen.py \
	--data_dir=./data/translate_vivi \
	--tmp_dir=/tmp/translate_vivi \
	--problem=translate_vivi
	$@
else if [ "$1" == "train" ]; then
    echo "Start tp rim t2t_train"
    python3 ./t2t_trainer.py \
        --model='transformer' \
        --hparams_set=$hparams_set \
        --hparams='learning_rate_cosine_cycle_steps=50000' \
        --train_steps=1000 \
        --eval_steps=10 \
        --problem=translate_vivi \
        --data_dir=./data/translate_vivi \
        --output_dir=./output/translate_vivi
        --use_tpu=False \
        --worker_gpus=2 \
        $@
el
    #python3 ./back_translate.py 
    #--lang=vi \
    #--decode_hparams=$decode_hparams \
    #--model=$model_name \
    #--hparams_set=$hparams_set \
    #--vien_ckpt=$vien_path \
    #--envi_ckpt=$envi_path 
    #--backtranslate_interactively	
    #$@
fi


