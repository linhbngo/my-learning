# Test Environment


## Setup

- Run the following to setup from inside `llms-from-scratch` directory

```bash
conda env create -f environment.yml
conda activate llms_from_scratch_env
uv pip install -e .
```

- Login to hugging face via cli:

```bash
hf auth login
```



