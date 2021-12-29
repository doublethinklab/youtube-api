# Simplified YouTube API Wrapper

## Getting Started

1. Install Docker - [instructions](https://docs.docker.com/engine/install/).
2. Get a YouTube API key - [instructions](https://hackmd.io/o08YEPCWRyCDlgYU4H6PPA).
   Save this as a file named anything in a folder in the root directory called `api_keys`.
3. Build the image: `./build_image.sh`.

## Usage

Run the `jupyter.sh` script to bring up a jupyter notebook
server that you can use. You need to specify a port.
A good default is `8888`. So:

```
./jupyter.sh 8888
```

**NOTE**: if you are using Windows, use the `jupyter-windows.sh` script.
