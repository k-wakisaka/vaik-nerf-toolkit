# mobilenerf

## Install

```shell
pip install --upgrade pip
pip install "jax[cuda11_cudnn82]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
```

## Run 

```shell
python stage1.py --scene_type real360 \
                 --scene_dir ~/Desktop/data/input_colmap/
```
