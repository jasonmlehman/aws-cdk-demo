# Overview

There are two types of python layers that have to be accounted for and each are done differently.

The first layer is one that doesn't have any other dependencies, other than the python package.  Libraries like requests and flask are these types.  To implement these layers follow the first section.

The other type of layer is one that has more dependencies specific to the docker image.  These are a little bit trickier and there are a couple of ways to account for it.  You can using docker bundling within the class, but that is a last resort if you can't find a prepackaged layer.  A good example of this type of package is pyodbc.  See the second section for how to get these in lambda layers.

## Creating a Lambda function with no dependencies, other than the package

> 1.  Create a folder under "infra" for the lambda function. **mkdir infra\demo-lambda-python-layer**
> 2.  Create te Layer and Code folders: **mkdir infra\demo-lambda-python-layer\layer** and ****mkdir infra\demo-lambda-python-layer\code**
> 3.  Create the code and place it in the code folder.  **infra\demo-lambda-python-layer\code\index.py**
> 3.  Install the lambda layer: **pip install requests --target infra\demo-lambda-python-layer\layer\python\lib\python3.9\site-packages**
> 4.  Add the Layer to Lambda_Stack.py, add multiple as required
> 5.  Update CDK context with layer and code path
> 6.  Import the stack into the application stage
> 6.  Commit the Code

## Creating a Lambda function with other depencies, deployed from a zip

> 1.  Prepare a zip file, or find one that has been packaged.  i.e. https://github.com/naingaungphyo/lambda_pyodbc_layer-python3.8
> 2.  Rather than point the folder, copy the zip file and update the "Lambda_zip_path" in cdk.json.
> 3.  See lambda_stack, specifically the LambdaLayerPyStackv2 class. Notice the code is pointed to a specific zip file: code = _lambda.Code.from_asset(context["lambda_zip"])