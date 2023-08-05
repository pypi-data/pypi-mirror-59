### A Simple pytorch implementation of GradCAM[1], and GradCAM++[2]
<br>
<p align="center">
<img src=assets/readme.png>
</p>

### Installation

```sh
pip install pytorch-gradcam
```

### Supported torchvision models
- alexnet
- vgg
- resnet
- densenet
- squeezenet

### Usage
please refer to `example.ipynb` for general usage and refer to documentations of each layer-finding functions in `utils.py` if you want to know how to set `target_layer_name` properly.

Use your own model and layer:
```python
model = MyModel()
target_layer = model.my_submodule
gradcam = GradCAM(model, target_layer)
```

### References:
[1] Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization, Selvaraju et al, ICCV, 2017 <br>
[2] Grad-CAM++: Generalized Gradient-based Visual Explanations for Deep Convolutional Networks, Chattopadhyay et al, WACV, 2018
