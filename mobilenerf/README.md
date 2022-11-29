# mobilenerf

## Install

```shell
cd mobilenerf
conda install cuda -c nvidia -y
pip install --upgrade pip
pip install "jax[cuda11_cudnn82]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
pip install -r requirements.txt
```

## Run 

```shell
cd mobilenerf
python stage1.py --scene_type real360 \
                 --scene_dir ~/Desktop/data/input_colmap/ \
                 --output_dir ~/Desktop/data/output_stg1 \
                 --train_iters_cont 300000 \
                 --max_test_num 10
```
