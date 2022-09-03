# data_pipeline_api


### AWS Lambda Deployment Package

`pip3 install requests -t .`


### Lambda Handler
https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html

When Lambda invokes your function handler, the Lambda runtime passes two arguments to the function handler:

The first argument is the event object. An event is a JSON-formatted document that contains data for a Lambda function to process. The Lambda runtime converts the event to an object and passes it to your function code. It is usually of the Python dict type. It can also be list, str, int, float, or the NoneType type.

The event object contains information from the invoking service. When you invoke a function, you determine the structure and contents of the event. When an AWS service invokes your function, the service defines the event structure. For more information about events from AWS services, see Using AWS Lambda with other services.

The second argument is the context object. A context object is passed to your function by Lambda at runtime. This object provides methods and properties that provide information about the invocation, function, and runtime environment.

