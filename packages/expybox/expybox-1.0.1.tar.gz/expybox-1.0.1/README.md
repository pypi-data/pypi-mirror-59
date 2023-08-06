# ExpyBox [![Documentation Status](https://readthedocs.org/projects/expybox/badge/?version=latest)](https://expybox.readthedocs.io/en/latest/?badge=latest)

ExpyBox is a Jupyter notebook toolbox for model interpretability/explainability.
It lets you create interactive Jupyter notebooks to explain your model.

[Documentation](https://expybox.readthedocs.org)

## Usage
This package is meant to be used inside of Jupyter notebook, other usage makes little to no sense.
First you need to import and instantiate the ExpyBox class:

```python
from expybox import ExpyBox
expybox = ExpyBox(train_data, predict_function, kernel_globals=globals())
```

Now you can use the supported interpretability methods like  this
(for list of supported methods refer to the [documentation](https://expybox.readthedocs.org)):
```python
expybox.lime()
```
which creates a form:
![ExpyBox form example](docs/pictures/expybox-lime.png "ExpyBox-form")

In this form you can set up explained instance (if it's necessary for the selected method)
and method parameters. After clicking on `Run Interact` the method will be executed
and its output will be shown below the form.

You can then change the parameters or the explained instance and press `Run Interact` 
again which will rerun the method with new parameters.

You can find an example Jupyter notebook in `examples` folder. 

## Instalation
Because of *alibi* package ExpyBox requires **64-bit** Python 3.7 or higher. 
It is also recommended to create separate virtual enviroment - you can use Pythons 
[venv](https://docs.python.org/3/library/venv.html).

Otherwise the installation process is the same as for other packages, just use pip:
```bash
pip install expybox
``` 


