<p align="center"><img width="300" src="docs/source/images/ipycanvas_logo.svg"></p>
<h1 align="center">ipycanvas</h1>
<h2 align="center"> Interactive Canvas in Jupyter </h1>

[![Documentation](http://readthedocs.org/projects/ipycanvas/badge/?version=latest)](https://ipycanvas.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/martinRenou/ipycanvas/stable?filepath=examples)
[![Build Status](https://travis-ci.org/martinRenou/ipycanvas.svg?branch=master)](https://travis-ci.org/martinRenou/ipycanvas)

ipycanvas is a lightweight, fast and stable library exposing the [browser's Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) to Python.
It allows you to draw simple primitives directly from Python like text, lines, polygons, arcs, images etc. This simple toolset allows you to draw literally anything!

## Try it online!

You can try it online by clicking on this badge:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/martinRenou/ipycanvas/stable?filepath=examples)

## Documentation

You can read the documentation following this link: https://ipycanvas.readthedocs.io/en/latest/

## Examples

### Create John Conway's Game Of Life
![John Conway's Game Of Life](docs/source/images/ipycanvas_gameoflife.png)

### Draw Particles from IPython
![Particles](docs/source/images/ipycanvas_particles.png)

### Custom Sprites
![Sprites](docs/source/images/ipycanvas_sprites.png)

### Draw data directly from a NumPy array
![NumPy](docs/source/images/ipycanvas_binary.png)

### Create your own plotting library **fully** in Python
![Plotting](docs/source/images/ipycanvas_scatter.png)

## Installation

You can install using `pip`:

```bash
pip install ipycanvas
```

Or using `conda`:

```bash
conda install -c conda-forge ipycanvas
```

And if you use jupyterlab:

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipycanvas
```

## Installation from sources

You can install using `pip`:

```bash
git clone https://github.com/martinRenou/ipycanvas
cd ipycanvas
pip install .
```

And if you use jupyterlab:

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install .
```

And you use the classical Jupyter:

```bash
jupyter nbextension install --py --symlink --sys-prefix ipycanvas
jupyter nbextension enable --py --sys-prefix ipycanvas
```
