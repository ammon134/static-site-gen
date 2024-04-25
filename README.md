# Static Site Generator

## Description

Simple tool that serves static html pages from markdown,
inspired by [Hugo](https://gohugo.io/), [Jekyll](https://jekyllrb.com/) and the like.

## Installation

Clone the repo and cd into it

```sh
git clone https://github.com/ammon134/static-site-gen
cd static-site-gen
```

Make `main.sh` executable

```sh
chmod +x main.sh
```

Create a virtual env

```sh
python -m venv .venv
```

## Usage

Add markdown content into the `content` directory. URL of the page is the
directory name. See the existing content for examples.

Add assets like images in to `static` directory.

Generate html and start the server by executing `main.sh`

```sh
./main.sh
```
