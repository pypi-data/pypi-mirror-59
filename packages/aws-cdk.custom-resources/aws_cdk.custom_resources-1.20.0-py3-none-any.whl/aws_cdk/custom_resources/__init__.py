"""
# AWS CDK Custom Resources

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module. Releases might lack important features and might have
> future breaking changes.**
>
> This API is still under active development and subject to non-backward
> compatible changes or removal in any future version. Use of the API is not recommended in production
> environments. Experimental APIs are not subject to the Semantic Versioning model.

---
<!--END STABILITY BANNER-->

## Provider Framework

AWS CloudFormation [custom resources]((https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html).) are extension points to the provisioning
engine. When CloudFormation needs to create, update or delete a custom resource,
it sends a lifecycle event notification to a **custom resource provider**. The provider
handles the event (e.g. creates a resource) and sends back a response to CloudFormation.

The `@aws-cdk/custom-resources.Provider` construct is a "mini-framework" for
implementing providers for AWS CloudFormation custom resources. The framework offers a high-level API which makes it easier to implement robust
and powerful custom resources and includes the following capabilities:

* Handles responses to AWS CloudFormation and protects against blocked
  deployments
* Validates handler return values to help with correct handler implementation
* Supports asynchronous handlers to enable long operations which can exceed the AWS Lambda timeout
* Implements default behavior for physical resource IDs.

The following code shows how the `Provider` construct is used in conjunction
with `cfn.CustomResource` and a user-provided AWS Lambda function which
implements the actual handler.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.custom_resources as cr
import aws_cdk.aws_cloudformation as cfn

on_event = lambda.Function(self, "MyHandler")

my_provider = cr.Provider(self, "MyProvider",
    on_event_handler=on_event,
    is_complete_handler=is_complete
)

cfn.CustomResource(self, "Resource1", provider=my_provider)
cfn.CustomResource(self, "Resource2", provider=my_provider)
```

Providers are implemented through AWS Lambda functions that are triggered by the
provider framework in response to lifecycle events.

At the minimum, users must define the `onEvent` handler, which is invoked by the
framework for all resource lifecycle events (`Create`, `Update` and `Delete`)
and returns a result which is then submitted to CloudFormation.

The following example is a skeleton for a Python implementation of `onEvent`:

```py
def on_event(event, context):
  print(event)
  request_type = event['RequestType']
  if request_type == 'Create': return on_create(event)
  if request_type == 'Update': return on_update(event)
  if request_type == 'Delete': return on_delete(event)
  raise Exception("Invalid request type: %s" % request_type)

def on_create(event):
  props = event["ResourceProperties"]
  print("create new resource with props %s" % props)

  # add your create code here...
  physical_id = ...

  return { 'PhysicalResourceId': physical_id }

def on_update(event):
  physical_id = event["PhysicalResourceId"]
  props = event["ResourceProperties"]
  print("update resource %s with props %s" % (physical_id, props))
  # ...

def on_delete(event):
  physical_id = event["PhysicalResourceId"]
  print("delete resource %s" % physical_id)
  # ...
```

Users may also provide an additional handler called `isComplete`, for cases
where the lifecycle operation cannot be completed immediately. The
`isComplete` handler will be retried asynchronously after `onEvent` until it
returns `IsComplete: true`, or until the total provider timeout has expired.

The following example is a skeleton for a Python implementation of `isComplete`:

```py
def is_complete(event, context):
  physical_id = event["PhysicalResourceId"]
  request_type = event["RequestType"]

  # check if resource is stable based on request_type
  is_ready = ...

  return { 'IsComplete': is_ready }
```

### Handling Lifecycle Events: onEvent

The user-defined `onEvent` AWS Lambda function is invoked whenever a resource
lifecycle event occurs. The function is expected to handle the event and return
a response to the framework that, at least, includes the physical resource ID.

If `onEvent` returns successfully, the framework will submit a "SUCCESS" response
to AWS CloudFormation for this resource operation.  If the provider is
[asynchronous](#asynchronous-providers-iscomplete) (`isCompleteHandler` is
defined), the framework will only submit a response based on the result of
`isComplete`.

If `onEvent` throws an error, the framework will submit a "FAILED" response to
AWS CloudFormation.

The input event includes the following fields derived from the [Custom Resource
Provider Request](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requests.html#crpg-ref-request-fields):

|Field|Type|Description
|-----|----|----------------
|`RequestType`|String|The type of lifecycle event: `Create`, `Update` or `Delete`.
|`LogicalResourceId`|String|The template developer-chosen name (logical ID) of the custom resource in the AWS CloudFormation template.
|`PhysicalResourceId`|String|This field will only be present for `Update` and `Delete` events and includes the value returned in `PhysicalResourceId` of the previous operation.
|`ResourceProperties`|JSON|This field contains the properties defined in the template for this custom resource.
|`OldResourceProperties`|JSON|This field will only be present for `Update` events and contains the resource properties that were declared previous to the update request.
|`ResourceType`|String|The resource type defined for this custom resource in the template. A provider may handle any number of custom resource types.
|`RequestId`|String|A unique ID for the request.
|`StackId`|String|The ARN that identifies the stack that contains the custom resource.

The return value from `onEvent` must be a JSON object with the following fields:

|Field|Type|Required|Description
|-----|----|--------|-----------
|`PhysicalResourceId`|String|No|The allocated/assigned physical ID of the resource. If omitted for `Create` events, the event's `RequestId` will be used. For `Update`, the current physical ID will be used. If a different value is returned, CloudFormation will follow with a subsequent `Delete` for the previous ID (resource replacement). For `Delete`, it will always return the current physical resource ID, and if the user returns a different one, an error will occur.
|`Data`|JSON|No|Resource attributes, which can later be retrieved through `Fn::GetAtt` on the custom resource object.

### Asynchronous Providers: isComplete

It is not uncommon for the provisioning of resources to be an asynchronous
operation, which means that the operation does not immediately finish, and we
need to "wait" until the resource stabilizes.

The provider framework makes it easy to implement "waiters" by allowing users to
specify an additional AWS Lambda function in `isCompleteHandler`.

The framework will repeatedly invoke the handler every `queryInterval`. When
`isComplete` returns with `IsComplete: true`, the framework will submit a
"SUCCESS" response to AWS CloudFormation. If `totalTimeout` expires and the
operation has not yet completed, the framework will submit a "FAILED" response
with the message "Operation timed out".

If an error is thrown, the framework will submit a "FAILED" response to AWS
CloudFormation.

The input event to `isComplete` is similar to
[`onEvent`](#handling-lifecycle-events-onevent), with an additional guarantee
that `PhysicalResourceId` is defines and contains the value returned from
`onEvent` or the described default. At any case, it is guaranteed to exist.

The return value must be a JSON object with the following fields:

|Field|Type|Required|Description
|-----|----|--------|-----------
|`IsComplete`|Boolean|Yes|Indicates if the operation has finished or not.
|`Data`|JSON|No|May only be sent if `IsComplete` is `true` and includes additional resource attributes. These attributes will be **merged** with the ones returned from `onEvent`

### Physical Resource IDs

Every resource in CloudFormation has a physical resource ID. When a resource is
created, the `PhysicalResourceId` returned from the `Create` operation is stored
by AWS CloudFormation and assigned to the logical ID defined for this resource
in the template. If a `Create` operation returns without a `PhysicalResourceId`,
the framework will use `RequestId` as the default. This is sufficient for
various cases such as "pseudo-resources" which only query data.

For `Update` and `Delete` operations, the resource event will always include the
current `PhysicalResourceId` of the resource.

When an `Update` operation occurs, the default behavior is to return the current
physical resource ID. if the `onEvent` returns a `PhysicalResourceId` which is
different from the current one, AWS CloudFormation will treat this as a
**resource replacement**, and it will issue a subsequent `Delete` operation for
the old resource.

As a rule of thumb, if your custom resource supports configuring a physical name
(e.g. you can specify a `BucketName` when you define an `AWS::S3::Bucket`), you
must return this name in `PhysicalResourceId` and make sure to handle
replacement properly. The `S3File` example demonstrates this
through the `objectKey` property.

### Error Handling

As mentioned above, if any of the user handlers fail (i.e. throws an exception)
or times out (due to their AWS Lambda timing out), the framework will trap these
errors and submit a "FAILED" response to AWS CloudFormation, along with the error
message.

Since errors can occur in multiple places in the provider (framework, `onEvent`,
`isComplete`), it is important to know that there could situations where a
resource operation fails even though the operation technically succeeded (i.e.
isComplete throws an error).

When AWS CloudFormation receives a "FAILED" response, it will attempt to roll
back the stack to it's last state. This has different meanings for different
lifecycle events:

* If a `Create` event fails, the resource provider framework will automatically
  ignore the subsequent `Delete` operation issued by AWS CloudFormation. The
  framework currently does not support customizing this behavior (see
  https://github.com/aws/aws-cdk/issues/5524).
* If an `Update` event fails, CloudFormation will issue an additional `Update`
  with the previous properties.
* If a `Delete` event fails, CloudFormation will abandon this resource.

### Execution Policy

Similarly to any AWS Lambda function, if the user-defined handlers require
access to AWS resources, you will have to define these permissions
by calling "grant" methods such as `myBucket.grantRead(myHandler)`), using `myHandler.addToRolePolicy`
or specifying an `initialPolicy` when defining the function.

Bear in mind that in most cases, a single provider will be used for multiple
resource instances. This means that the execution policy of the provider must
have the appropriate privileges.

The following example grants the `onEvent` handler `s3:GetObject*` permissions
to all buckets:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda.Function(self, "OnEventHandler",
    # ...
    initial_policy=[
        iam.PolicyStatement(actions=["s3:GetObject*"], resources=["*"])
    ]
)
```

### Timeouts

Users are responsible to define the timeouts for the AWS Lambda functions for
user-defined handlers. It is recommended not to exceed a **14 minutes** timeout,
since all framework functions are configured to time out after 15 minutes, which
is the maximal AWS Lambda timeout.

If your operation takes over **14 minutes**, the recommended approach is to
implement an [asynchronous provider](#asynchronous-providers-iscomplete), and
then configure the timeouts for the asynchronous retries through the
`queryInterval` and the `totalTimeout` options.

### Examples

This module includes a few examples for custom resource implementations:

#### S3File

Provisions an object in an S3 bucket with textual contents. See the source code
for the
[construct](test/provider-framework/integration-test-fixtures/s3-file.ts) and
[handler](test/provider-framework/integration-test-fixtures/s3-file-handler/index.ts).

The following example will create the file `folder/file1.txt` inside `myBucket`
with the contents `hello!`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
S3File(self, "MyFile",
    bucket=my_bucket,
    object_key="folder/file1.txt", # optional
    content="hello!",
    public=True
)
```

This sample demonstrates the following concepts:

* Synchronous implementation (`isComplete` is not defined)
* Automatically generates the physical name if `objectKey` is not defined
* Handles physical name changes
* Returns resource attributes
* Handles deletions
* Implemented in TypeScript

#### S3Assert

Checks that the textual contents of an S3 object matches a certain value. The check will be retried for 5 minutes as long as the object is not found or the value is different. See the source code for the [construct](test/provider-framework/integration-test-fixtures/s3-assert.ts) and [handler](test/provider-framework/integration-test-fixtures/s3-assert-handler/index.py).

The following example defines an `S3Assert` resource which waits until
`myfile.txt` in `myBucket` exists and includes the contents `foo bar`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
S3Assert(self, "AssertMyFile",
    bucket=my_bucket,
    object_key="myfile.txt",
    expected_content="foo bar"
)
```

This sample demonstrates the following concepts:

* Asynchronous implementation
* Non-intrinsic physical IDs
* Implemented in Python

## Custom Resources for AWS APIs

Sometimes a single API call can fill the gap in the CloudFormation coverage. In
this case you can use the `AwsCustomResource` construct. This construct creates
a custom resource that can be customized to make specific API calls for the
`CREATE`, `UPDATE` and `DELETE` events. Additionally, data returned by the API
call can be extracted and used in other constructs/resources (creating a real
CloudFormation dependency using `Fn::GetAtt` under the hood).

The physical id of the custom resource can be specified or derived from the data
returned by the API call.

The `AwsCustomResource` uses the AWS SDK for JavaScript. Services, actions and
parameters can be found in the [API documentation](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html).

Path to data must be specified using a dot notation, e.g. to get the string value
of the `Title` attribute for the first item returned by `dynamodb.query` it should
be `Items.0.Title.S`.

### Execution Policy

IAM policy statements required to make the API calls are derived from the calls
and allow by default the actions to be made on all resources (`*`). You can
restrict the permissions by specifying your own list of statements with the
`policyStatements` prop. The custom resource also implements `iam.IGrantable`,
making it possible to use the `grantXxx()` methods.

As this custom resource uses a singleton Lambda function, it's important to note
that the function's role will eventually accumulate the permissions/grants from all
resources.

Chained API calls can be achieved by creating dependencies:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
aws_custom1 = AwsCustomResource(self, "API1",
    on_create={
        "service": "...",
        "action": "...",
        "physical_resource_id": "..."
    }
)

aws_custom2 = AwsCustomResource(self, "API2",
    on_create={
        "service": "...",
        "action": "...",
        "parameters": {
            "text": aws_custom1.get_data_string("Items.0.text")
        },
        "physical_resource_id": "..."
    }
)
```

### Examples

#### Verify a domain with SES

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
verify_domain_identity = AwsCustomResource(self, "VerifyDomainIdentity",
    on_create={
        "service": "SES",
        "action": "verifyDomainIdentity",
        "parameters": {
            "Domain": "example.com"
        },
        "physical_resource_id_path": "VerificationToken"
    }
)

route53.TxtRecord(self, "SESVerificationRecord",
    zone=zone,
    record_name="_amazonses.example.com",
    values=[verify_domain_identity.get_data_string("VerificationToken")]
)
```

#### Get the latest version of a secure SSM parameter

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
get_parameter = AwsCustomResource(self, "GetParameter",
    on_update={# will also be called for a CREATE event
        "service": "SSM",
        "action": "getParameter",
        "parameters": {
            "Name": "my-parameter",
            "WithDecryption": True
        },
        "physical_resource_id": Date.now().to_string()}
)

# Use the value in another construct with
get_parameter.get_data("Parameter.Value")
```

---


This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_cloudformation
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.aws_stepfunctions
import aws_cdk.aws_stepfunctions_tasks
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/custom-resources", "1.20.0", __name__, "custom-resources@1.20.0.jsii.tgz")


@jsii.implements(aws_cdk.aws_iam.IGrantable)
class AwsCustomResource(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/custom-resources.AwsCustomResource"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, on_create: typing.Optional["AwsSdkCall"]=None, on_delete: typing.Optional["AwsSdkCall"]=None, on_update: typing.Optional["AwsSdkCall"]=None, policy_statements: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, resource_type: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param on_create: The AWS SDK call to make when the resource is created. At least onCreate, onUpdate or onDelete must be specified. Default: - the call when the resource is updated
        :param on_delete: The AWS SDK call to make when the resource is deleted. Default: - no call
        :param on_update: The AWS SDK call to make when the resource is updated. Default: - no call
        :param policy_statements: The IAM policy statements to allow the different calls. Use only if resource restriction is needed. The custom resource also implements ``iam.IGrantable``, making it possible to use the ``grantXxx()`` methods. As this custom resource uses a singleton Lambda function, it's important to note the that function's role will eventually accumulate the permissions/grants from all resources. Default: - extract the permissions from the calls
        :param resource_type: Cloudformation Resource type. Default: - Custom::AWS
        :param role: The execution role for the Lambda function implementing this custom resource provider. This role will apply to all ``AwsCustomResource`` instances in the stack. The role must be assumable by the ``lambda.amazonaws.com`` service principal. Default: - a new role is created
        :param timeout: The timeout for the Lambda function implementing this custom resource. Default: Duration.minutes(2)

        stability
        :stability: experimental
        """
        props = AwsCustomResourceProps(on_create=on_create, on_delete=on_delete, on_update=on_update, policy_statements=policy_statements, resource_type=resource_type, role=role, timeout=timeout)

        jsii.create(AwsCustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="getData")
    def get_data(self, data_path: str) -> aws_cdk.core.Reference:
        """Returns response data for the AWS SDK call.

        Example for S3 / listBucket : 'Buckets.0.Name'

        Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getDataString`` for string attributes.

        :param data_path: the path to the data.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getData", [data_path])

    @jsii.member(jsii_name="getDataString")
    def get_data_string(self, data_path: str) -> str:
        """Returns response data for the AWS SDK call as string.

        Example for S3 / listBucket : 'Buckets.0.Name'

        :param data_path: the path to the data.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getDataString", [data_path])

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")


@jsii.data_type(jsii_type="@aws-cdk/custom-resources.AwsCustomResourceProps", jsii_struct_bases=[], name_mapping={'on_create': 'onCreate', 'on_delete': 'onDelete', 'on_update': 'onUpdate', 'policy_statements': 'policyStatements', 'resource_type': 'resourceType', 'role': 'role', 'timeout': 'timeout'})
class AwsCustomResourceProps():
    def __init__(self, *, on_create: typing.Optional["AwsSdkCall"]=None, on_delete: typing.Optional["AwsSdkCall"]=None, on_update: typing.Optional["AwsSdkCall"]=None, policy_statements: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, resource_type: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None):
        """
        :param on_create: The AWS SDK call to make when the resource is created. At least onCreate, onUpdate or onDelete must be specified. Default: - the call when the resource is updated
        :param on_delete: The AWS SDK call to make when the resource is deleted. Default: - no call
        :param on_update: The AWS SDK call to make when the resource is updated. Default: - no call
        :param policy_statements: The IAM policy statements to allow the different calls. Use only if resource restriction is needed. The custom resource also implements ``iam.IGrantable``, making it possible to use the ``grantXxx()`` methods. As this custom resource uses a singleton Lambda function, it's important to note the that function's role will eventually accumulate the permissions/grants from all resources. Default: - extract the permissions from the calls
        :param resource_type: Cloudformation Resource type. Default: - Custom::AWS
        :param role: The execution role for the Lambda function implementing this custom resource provider. This role will apply to all ``AwsCustomResource`` instances in the stack. The role must be assumable by the ``lambda.amazonaws.com`` service principal. Default: - a new role is created
        :param timeout: The timeout for the Lambda function implementing this custom resource. Default: Duration.minutes(2)

        stability
        :stability: experimental
        """
        if isinstance(on_create, dict): on_create = AwsSdkCall(**on_create)
        if isinstance(on_delete, dict): on_delete = AwsSdkCall(**on_delete)
        if isinstance(on_update, dict): on_update = AwsSdkCall(**on_update)
        self._values = {
        }
        if on_create is not None: self._values["on_create"] = on_create
        if on_delete is not None: self._values["on_delete"] = on_delete
        if on_update is not None: self._values["on_update"] = on_update
        if policy_statements is not None: self._values["policy_statements"] = policy_statements
        if resource_type is not None: self._values["resource_type"] = resource_type
        if role is not None: self._values["role"] = role
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def on_create(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is created.

        At least onCreate, onUpdate or onDelete must be specified.

        default
        :default: - the call when the resource is updated

        stability
        :stability: experimental
        """
        return self._values.get('on_create')

    @builtins.property
    def on_delete(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is deleted.

        default
        :default: - no call

        stability
        :stability: experimental
        """
        return self._values.get('on_delete')

    @builtins.property
    def on_update(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is updated.

        default
        :default: - no call

        stability
        :stability: experimental
        """
        return self._values.get('on_update')

    @builtins.property
    def policy_statements(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """The IAM policy statements to allow the different calls. Use only if resource restriction is needed.

        The custom resource also implements ``iam.IGrantable``, making it possible
        to use the ``grantXxx()`` methods.

        As this custom resource uses a singleton Lambda function, it's important
        to note the that function's role will eventually accumulate the
        permissions/grants from all resources.

        default
        :default: - extract the permissions from the calls

        stability
        :stability: experimental
        """
        return self._values.get('policy_statements')

    @builtins.property
    def resource_type(self) -> typing.Optional[str]:
        """Cloudformation Resource type.

        default
        :default: - Custom::AWS

        stability
        :stability: experimental
        """
        return self._values.get('resource_type')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The execution role for the Lambda function implementing this custom resource provider.

        This role will apply to all ``AwsCustomResource``
        instances in the stack. The role must be assumable by the
        ``lambda.amazonaws.com`` service principal.

        default
        :default: - a new role is created

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The timeout for the Lambda function implementing this custom resource.

        default
        :default: Duration.minutes(2)

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsCustomResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/custom-resources.AwsSdkCall", jsii_struct_bases=[], name_mapping={'action': 'action', 'service': 'service', 'api_version': 'apiVersion', 'catch_error_pattern': 'catchErrorPattern', 'output_path': 'outputPath', 'parameters': 'parameters', 'physical_resource_id': 'physicalResourceId', 'physical_resource_id_path': 'physicalResourceIdPath', 'region': 'region'})
class AwsSdkCall():
    def __init__(self, *, action: str, service: str, api_version: typing.Optional[str]=None, catch_error_pattern: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Any=None, physical_resource_id: typing.Optional[str]=None, physical_resource_id_path: typing.Optional[str]=None, region: typing.Optional[str]=None):
        """An AWS SDK call.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param output_path: Restrict the data returned by the custom resource to a specific path in the API response. Use this to limit the data returned by the custom resource if working with API calls that could potentially result in custom response objects exceeding the hard limit of 4096 bytes. Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent' Default: - return all data
        :param parameters: The parameters for the service action.
        :param physical_resource_id: The physical resource id of the custom resource for this call. Either ``physicalResourceId`` or ``physicalResourceIdPath`` must be specified for onCreate or onUpdate calls. Default: - no physical resource id
        :param physical_resource_id_path: The path to the data in the API call response to use as the physical resource id. Either ``physicalResourceId`` or ``physicalResourceIdPath`` must be specified for onCreate or onUpdate calls. Default: - no path
        :param region: The region to send service requests to. **Note: Cross-region operations are generally considered an anti-pattern.** **Consider first deploying a stack in that region.** Default: - the region where this custom resource is deployed

        stability
        :stability: experimental
        """
        self._values = {
            'action': action,
            'service': service,
        }
        if api_version is not None: self._values["api_version"] = api_version
        if catch_error_pattern is not None: self._values["catch_error_pattern"] = catch_error_pattern
        if output_path is not None: self._values["output_path"] = output_path
        if parameters is not None: self._values["parameters"] = parameters
        if physical_resource_id is not None: self._values["physical_resource_id"] = physical_resource_id
        if physical_resource_id_path is not None: self._values["physical_resource_id_path"] = physical_resource_id_path
        if region is not None: self._values["region"] = region

    @builtins.property
    def action(self) -> str:
        """The service action to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('action')

    @builtins.property
    def service(self) -> str:
        """The service to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('service')

    @builtins.property
    def api_version(self) -> typing.Optional[str]:
        """API version to use for the service.

        default
        :default: - use latest available API version

        see
        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        stability
        :stability: experimental
        """
        return self._values.get('api_version')

    @builtins.property
    def catch_error_pattern(self) -> typing.Optional[str]:
        """The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        default
        :default: - do not catch errors

        stability
        :stability: experimental
        """
        return self._values.get('catch_error_pattern')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """Restrict the data returned by the custom resource to a specific path in the API response.

        Use this to limit the data returned by the custom
        resource if working with API calls that could potentially result in custom
        response objects exceeding the hard limit of 4096 bytes.

        Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent'

        default
        :default: - return all data

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def physical_resource_id(self) -> typing.Optional[str]:
        """The physical resource id of the custom resource for this call.

        Either
        ``physicalResourceId`` or ``physicalResourceIdPath`` must be specified for
        onCreate or onUpdate calls.

        default
        :default: - no physical resource id

        stability
        :stability: experimental
        """
        return self._values.get('physical_resource_id')

    @builtins.property
    def physical_resource_id_path(self) -> typing.Optional[str]:
        """The path to the data in the API call response to use as the physical resource id.

        Either ``physicalResourceId`` or ``physicalResourceIdPath``
        must be specified for onCreate or onUpdate calls.

        default
        :default: - no path

        stability
        :stability: experimental
        """
        return self._values.get('physical_resource_id_path')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region to send service requests to.

        **Note: Cross-region operations are generally considered an anti-pattern.**
        **Consider first deploying a stack in that region.**

        default
        :default: - the region where this custom resource is deployed

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsSdkCall(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_cloudformation.ICustomResourceProvider)
class Provider(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/custom-resources.Provider"):
    """Defines an AWS CloudFormation custom resource provider.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, on_event_handler: aws_cdk.aws_lambda.IFunction, is_complete_handler: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, query_interval: typing.Optional[aws_cdk.core.Duration]=None, total_timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param on_event_handler: The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE). This function is responsible to begin the requested resource operation (CREATE/UPDATE/DELETE) and return any additional properties to add to the event, which will later be passed to ``isComplete``. The ``PhysicalResourceId`` property must be included in the response.
        :param is_complete_handler: The AWS Lambda function to invoke in order to determine if the operation is complete. This function will be called immediately after ``onEvent`` and then periodically based on the configured query interval as long as it returns ``false``. If the function still returns ``false`` and the alloted timeout has passed, the operation will fail. Default: - provider is synchronous. This means that the ``onEvent`` handler is expected to finish all lifecycle operations within the initial invocation.
        :param query_interval: Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized. The first ``isComplete`` will be called immediately after ``handler`` and then every ``queryInterval`` seconds, and until ``timeout`` has been reached or until ``isComplete`` returns ``true``. Default: Duration.seconds(5)
        :param total_timeout: Total timeout for the entire operation. The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes) Default: Duration.minutes(30)

        stability
        :stability: experimental
        """
        props = ProviderProps(on_event_handler=on_event_handler, is_complete_handler=is_complete_handler, query_interval=query_interval, total_timeout=total_timeout)

        jsii.create(Provider, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _: aws_cdk.core.Construct) -> aws_cdk.aws_cloudformation.CustomResourceProviderConfig:
        """Called by ``CustomResource`` which uses this provider.

        :param _: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_])

    @builtins.property
    @jsii.member(jsii_name="onEventHandler")
    def on_event_handler(self) -> aws_cdk.aws_lambda.IFunction:
        """The user-defined AWS Lambda function which is invoked for all resource lifecycle operations (CREATE/UPDATE/DELETE).

        stability
        :stability: experimental
        """
        return jsii.get(self, "onEventHandler")

    @builtins.property
    @jsii.member(jsii_name="isCompleteHandler")
    def is_complete_handler(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """The user-defined AWS Lambda function which is invoked asynchronously in order to determine if the operation is complete.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isCompleteHandler")


@jsii.data_type(jsii_type="@aws-cdk/custom-resources.ProviderProps", jsii_struct_bases=[], name_mapping={'on_event_handler': 'onEventHandler', 'is_complete_handler': 'isCompleteHandler', 'query_interval': 'queryInterval', 'total_timeout': 'totalTimeout'})
class ProviderProps():
    def __init__(self, *, on_event_handler: aws_cdk.aws_lambda.IFunction, is_complete_handler: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, query_interval: typing.Optional[aws_cdk.core.Duration]=None, total_timeout: typing.Optional[aws_cdk.core.Duration]=None):
        """Initialization properties for the ``Provider`` construct.

        :param on_event_handler: The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE). This function is responsible to begin the requested resource operation (CREATE/UPDATE/DELETE) and return any additional properties to add to the event, which will later be passed to ``isComplete``. The ``PhysicalResourceId`` property must be included in the response.
        :param is_complete_handler: The AWS Lambda function to invoke in order to determine if the operation is complete. This function will be called immediately after ``onEvent`` and then periodically based on the configured query interval as long as it returns ``false``. If the function still returns ``false`` and the alloted timeout has passed, the operation will fail. Default: - provider is synchronous. This means that the ``onEvent`` handler is expected to finish all lifecycle operations within the initial invocation.
        :param query_interval: Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized. The first ``isComplete`` will be called immediately after ``handler`` and then every ``queryInterval`` seconds, and until ``timeout`` has been reached or until ``isComplete`` returns ``true``. Default: Duration.seconds(5)
        :param total_timeout: Total timeout for the entire operation. The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes) Default: Duration.minutes(30)

        stability
        :stability: experimental
        """
        self._values = {
            'on_event_handler': on_event_handler,
        }
        if is_complete_handler is not None: self._values["is_complete_handler"] = is_complete_handler
        if query_interval is not None: self._values["query_interval"] = query_interval
        if total_timeout is not None: self._values["total_timeout"] = total_timeout

    @builtins.property
    def on_event_handler(self) -> aws_cdk.aws_lambda.IFunction:
        """The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE).

        This function is responsible to begin the requested resource operation
        (CREATE/UPDATE/DELETE) and return any additional properties to add to the
        event, which will later be passed to ``isComplete``. The ``PhysicalResourceId``
        property must be included in the response.

        stability
        :stability: experimental
        """
        return self._values.get('on_event_handler')

    @builtins.property
    def is_complete_handler(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """The AWS Lambda function to invoke in order to determine if the operation is complete.

        This function will be called immediately after ``onEvent`` and then
        periodically based on the configured query interval as long as it returns
        ``false``. If the function still returns ``false`` and the alloted timeout has
        passed, the operation will fail.

        default
        :default:

        - provider is synchronous. This means that the ``onEvent`` handler
          is expected to finish all lifecycle operations within the initial invocation.

        stability
        :stability: experimental
        """
        return self._values.get('is_complete_handler')

    @builtins.property
    def query_interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized.

        The first ``isComplete`` will be called immediately after ``handler`` and then
        every ``queryInterval`` seconds, and until ``timeout`` has been reached or until
        ``isComplete`` returns ``true``.

        default
        :default: Duration.seconds(5)

        stability
        :stability: experimental
        """
        return self._values.get('query_interval')

    @builtins.property
    def total_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Total timeout for the entire operation.

        The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes)

        default
        :default: Duration.minutes(30)

        stability
        :stability: experimental
        """
        return self._values.get('total_timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["AwsCustomResource", "AwsCustomResourceProps", "AwsSdkCall", "Provider", "ProviderProps", "__jsii_assembly__"]

publication.publish()
