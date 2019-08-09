# Create hparams and the model
model_name=transformer
hparams_set=transformer_tiny
vien_path=checkpoints/translate_vien_iwslt32k_tiny/avg
envi_path=checkpoints/translate_envi_iwslt32k_tiny/avg
decode_hparams="beam_size={2},alpha={0.6}"

python3 ./back_translate.py --lang=vi \
--decode_hparams=$decode_hparams \
--model=$model_name \
--hparams_set=$hparams_set \
--vien_ckpt=$vien_path \
--envi_ckpt=$envi_path \
--backtranslate_interactively
