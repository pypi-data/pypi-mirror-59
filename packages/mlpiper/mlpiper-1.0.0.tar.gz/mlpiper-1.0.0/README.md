# README

This is an example of a machine-learning pipeline that is implemented by the **'mlpiper'** platform.

This specific example is no more than a simple sklearn implementation, without using the
built-in sklearn Pipeline structure.

The pipeline description is provided by the `pipeline/pipeline.json` file.


## Setup

1. Browse to `ml_pipeline_examples/mlpiper_example`

	* ```> cd ml_pipeline_examples/mlpiper_example```

2. Create virtual env, whose name is 'mlpiper', or anything else (If you've already created it, use `workon` to activate it):

	* ```> mkvirtualenv --python=3 mlpiper```

3. Install 'mlpiper' (Skip if already installed):

	* ```> pip install -r requirements.txt```


# Run Example

(**Note:** Please make sure the environment was setup properly. Refer to ['Setup' section](#Setup) above for more information)

1. Browse to `ml_pipeline_examples/mlpiper_example`

	* ```> cd ml_pipeline_examples/mlpiper_example```


2. Run the `run.sh` script:

	* ```> run.sh```


# Results

```
...
Log Loss: 0.6571923425816221
ROC AUC Score: 0.6350086940964011
...
real	0m2.199s
user	0m2.528s
sys		0m0.295s
```
