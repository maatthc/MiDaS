# Image Depth generator API

## Setup on AWS Linux Arm

```
# sudo yum groupinstall "Development Tools"
python3 -m pip install --upgrade pip
```

```
sudo python3 -m pip install --pre torch torchvision  -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
```

```
sudo yum install opencv
```

```
sudo python3 -m pip install timm flask requests
## sudo python3 -m pip install opencv-python
```

```
wget https://github.com/AlexeyAB/MiDaS/releases/download/midas_dpt/midas_v21_small-70d6b9c8.pt -O weights/midas_v21_small-70d6b9c8.pt
```

This will generate an error:

```
python3 run
```

So this will fix it:
(waiting on this to be solved: https://github.com/rwightman/gen-efficientnet-pytorch/pull/62)

```
wget https://raw.githubusercontent.com/instinct79/gen-efficientnet-pytorch/fix-pyT-1.8-error/geffnet/conv2d_layers.py -O /home/ec2-user/.cache/torch/hub/rwightman_gen-efficientnet-pytorch_master/geffnet/conv2d_layers.py
```

## Run

```
export FLASK_ENV=development
export FLASK_APP=api-server
flask run
```
