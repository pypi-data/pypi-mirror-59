# cdk-openapi

An AWS CDK construct which generates API Gateway exposed Lambda functions
from an OpenAPI specification in your stack.

## Usage

### JavaScript

Install via npm:

```shell
$ npm i @stormreply/cdk-openapi
```

Add to your CDK stack:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from stormreply.cdk_openapi import OpenAPI, OpenAPIProps

api = OpenAPI(self, "SampleAPI",
    api="api.yaml"
)
```

### Python

Install via pip:

```shell
$ pip install stormreply.cdk-openapi
```

Add to your CDK stack:

```python
from stormreply.cdk_openapi import (
    OpenAPI,
    OpenAPIProps,
)

api = OpenAPI(
    self, "SampleAPI", {
      api='api.yaml'
    }
)
```

## License

Apache 2.0
