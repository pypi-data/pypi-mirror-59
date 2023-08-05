"""
## @aws-cdk/aws-dynamodb-global

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

Global Tables builds upon DynamoDB’s global footprint to provide you with a fully managed, multi-region, and multi-master database that provides fast, local, read and write performance for massively scaled, global applications. Global Tables replicates your Amazon DynamoDB tables automatically across your choice of AWS regions.

Here is a minimal deployable Global DynamoDB tables definition:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_dynamodb import AttributeType
from aws_cdk.aws_dynamodb_global import GlobalTable
from aws_cdk.core import App

app = App()
GlobalTable(app, "globdynamodb",
    partition_key=Attribute(name="hashKey", type=AttributeType.String),
    table_name="GlobalTable",
    regions=["us-east-1", "us-east-2", "us-west-2"]
)
app.synth()
```

## Implementation Notes

AWS Global DynamoDB Tables is an odd case currently.  The way this package works -

* Creates a DynamoDB table in a separate stack in each `DynamoDBGlobalStackProps.region` specified
* Deploys a CFN Custom Resource to your stack's specified region that calls a lambda that runs the aws cli which calls `createGlobalTable()`

### Notes

GlobalTable() will set `dynamoProps.stream` to be `NEW_AND_OLD_IMAGES` since this is a required attribute for AWS Global DynamoDB tables to work.  The package will throw an error if any other `stream` specification is set in `DynamoDBGlobalStackProps`.
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
import aws_cdk.aws_dynamodb
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-dynamodb-global", "1.20.0", __name__, "aws-dynamodb-global@1.20.0.jsii.tgz")


class GlobalTable(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dynamodb-global.GlobalTable"):
    """This class works by deploying an AWS DynamoDB table into each region specified in  GlobalTableProps.regions[], then triggering a CloudFormation Custom Resource Lambda to link them all together to create linked AWS Global DynamoDB tables.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, regions: typing.List[str], table_name: str, description: typing.Optional[str]=None, env: typing.Optional[aws_cdk.core.Environment]=None, stack_name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str,str]]=None, partition_key: aws_cdk.aws_dynamodb.Attribute, billing_mode: typing.Optional[aws_cdk.aws_dynamodb.BillingMode]=None, point_in_time_recovery: typing.Optional[bool]=None, read_capacity: typing.Optional[jsii.Number]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, server_side_encryption: typing.Optional[bool]=None, sort_key: typing.Optional[aws_cdk.aws_dynamodb.Attribute]=None, stream: typing.Optional[aws_cdk.aws_dynamodb.StreamViewType]=None, time_to_live_attribute: typing.Optional[str]=None, write_capacity: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param regions: Array of environments to create DynamoDB tables in. The tables will all be created in the same account.
        :param table_name: Name of the DynamoDB table to use across all regional tables. This is required for global tables.
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Default: - The ``default-account`` and ``default-region`` context parameters will be used. If they are undefined, it will not be possible to deploy the stack.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param partition_key: Partition key attribute definition.
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Default: Provisioned
        :param point_in_time_recovery: Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param server_side_encryption: Whether server-side encryption with an AWS managed customer master key is enabled. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param sort_key: Table sort key attribute definition. Default: no sort key
        :param stream: When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled
        :param time_to_live_attribute: The name of TTL attribute. Default: - TTL is disabled
        :param write_capacity: The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5

        stability
        :stability: experimental
        """
        props = GlobalTableProps(regions=regions, table_name=table_name, description=description, env=env, stack_name=stack_name, tags=tags, partition_key=partition_key, billing_mode=billing_mode, point_in_time_recovery=point_in_time_recovery, read_capacity=read_capacity, removal_policy=removal_policy, server_side_encryption=server_side_encryption, sort_key=sort_key, stream=stream, time_to_live_attribute=time_to_live_attribute, write_capacity=write_capacity)

        jsii.create(GlobalTable, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="regionalTables")
    def regional_tables(self) -> typing.List[aws_cdk.aws_dynamodb.Table]:
        """Obtain tables deployed in other each region.

        stability
        :stability: experimental
        """
        return jsii.get(self, "regionalTables")


@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb-global.GlobalTableProps", jsii_struct_bases=[aws_cdk.core.StackProps, aws_cdk.aws_dynamodb.TableOptions], name_mapping={'description': 'description', 'env': 'env', 'stack_name': 'stackName', 'tags': 'tags', 'partition_key': 'partitionKey', 'billing_mode': 'billingMode', 'point_in_time_recovery': 'pointInTimeRecovery', 'read_capacity': 'readCapacity', 'removal_policy': 'removalPolicy', 'server_side_encryption': 'serverSideEncryption', 'sort_key': 'sortKey', 'stream': 'stream', 'time_to_live_attribute': 'timeToLiveAttribute', 'write_capacity': 'writeCapacity', 'regions': 'regions', 'table_name': 'tableName'})
class GlobalTableProps(aws_cdk.core.StackProps, aws_cdk.aws_dynamodb.TableOptions):
    def __init__(self, *, description: typing.Optional[str]=None, env: typing.Optional[aws_cdk.core.Environment]=None, stack_name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str,str]]=None, partition_key: aws_cdk.aws_dynamodb.Attribute, billing_mode: typing.Optional[aws_cdk.aws_dynamodb.BillingMode]=None, point_in_time_recovery: typing.Optional[bool]=None, read_capacity: typing.Optional[jsii.Number]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, server_side_encryption: typing.Optional[bool]=None, sort_key: typing.Optional[aws_cdk.aws_dynamodb.Attribute]=None, stream: typing.Optional[aws_cdk.aws_dynamodb.StreamViewType]=None, time_to_live_attribute: typing.Optional[str]=None, write_capacity: typing.Optional[jsii.Number]=None, regions: typing.List[str], table_name: str):
        """Properties for the multiple DynamoDB tables to mash together into a global table.

        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Default: - The ``default-account`` and ``default-region`` context parameters will be used. If they are undefined, it will not be possible to deploy the stack.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param partition_key: Partition key attribute definition.
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Default: Provisioned
        :param point_in_time_recovery: Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param server_side_encryption: Whether server-side encryption with an AWS managed customer master key is enabled. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param sort_key: Table sort key attribute definition. Default: no sort key
        :param stream: When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled
        :param time_to_live_attribute: The name of TTL attribute. Default: - TTL is disabled
        :param write_capacity: The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param regions: Array of environments to create DynamoDB tables in. The tables will all be created in the same account.
        :param table_name: Name of the DynamoDB table to use across all regional tables. This is required for global tables.

        stability
        :stability: experimental
        """
        if isinstance(env, dict): env = aws_cdk.core.Environment(**env)
        if isinstance(partition_key, dict): partition_key = aws_cdk.aws_dynamodb.Attribute(**partition_key)
        if isinstance(sort_key, dict): sort_key = aws_cdk.aws_dynamodb.Attribute(**sort_key)
        self._values = {
            'partition_key': partition_key,
            'regions': regions,
            'table_name': table_name,
        }
        if description is not None: self._values["description"] = description
        if env is not None: self._values["env"] = env
        if stack_name is not None: self._values["stack_name"] = stack_name
        if tags is not None: self._values["tags"] = tags
        if billing_mode is not None: self._values["billing_mode"] = billing_mode
        if point_in_time_recovery is not None: self._values["point_in_time_recovery"] = point_in_time_recovery
        if read_capacity is not None: self._values["read_capacity"] = read_capacity
        if removal_policy is not None: self._values["removal_policy"] = removal_policy
        if server_side_encryption is not None: self._values["server_side_encryption"] = server_side_encryption
        if sort_key is not None: self._values["sort_key"] = sort_key
        if stream is not None: self._values["stream"] = stream
        if time_to_live_attribute is not None: self._values["time_to_live_attribute"] = time_to_live_attribute
        if write_capacity is not None: self._values["write_capacity"] = write_capacity

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the stack.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def env(self) -> typing.Optional[aws_cdk.core.Environment]:
        """The AWS environment (account/region) where this stack will be deployed.

        default
        :default:

        - The ``default-account`` and ``default-region`` context parameters will be
          used. If they are undefined, it will not be possible to deploy the stack.
        """
        return self._values.get('env')

    @builtins.property
    def stack_name(self) -> typing.Optional[str]:
        """Name to deploy the stack with.

        default
        :default: - Derived from construct path.
        """
        return self._values.get('stack_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Stack tags that will be applied to all the taggable resources and the stack itself.

        default
        :default: {}
        """
        return self._values.get('tags')

    @builtins.property
    def partition_key(self) -> aws_cdk.aws_dynamodb.Attribute:
        """Partition key attribute definition."""
        return self._values.get('partition_key')

    @builtins.property
    def billing_mode(self) -> typing.Optional[aws_cdk.aws_dynamodb.BillingMode]:
        """Specify how you are charged for read and write throughput and how you manage capacity.

        default
        :default: Provisioned
        """
        return self._values.get('billing_mode')

    @builtins.property
    def point_in_time_recovery(self) -> typing.Optional[bool]:
        """Whether point-in-time recovery is enabled.

        default
        :default: - point-in-time recovery is disabled
        """
        return self._values.get('point_in_time_recovery')

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        """The read capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        default
        :default: 5
        """
        return self._values.get('read_capacity')

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """The removal policy to apply to the DynamoDB Table.

        default
        :default: RemovalPolicy.RETAIN
        """
        return self._values.get('removal_policy')

    @builtins.property
    def server_side_encryption(self) -> typing.Optional[bool]:
        """Whether server-side encryption with an AWS managed customer master key is enabled.

        default
        :default: - server-side encryption is enabled with an AWS owned customer master key
        """
        return self._values.get('server_side_encryption')

    @builtins.property
    def sort_key(self) -> typing.Optional[aws_cdk.aws_dynamodb.Attribute]:
        """Table sort key attribute definition.

        default
        :default: no sort key
        """
        return self._values.get('sort_key')

    @builtins.property
    def stream(self) -> typing.Optional[aws_cdk.aws_dynamodb.StreamViewType]:
        """When an item in the table is modified, StreamViewType determines what information is written to the stream for this table.

        default
        :default: - streams are disabled
        """
        return self._values.get('stream')

    @builtins.property
    def time_to_live_attribute(self) -> typing.Optional[str]:
        """The name of TTL attribute.

        default
        :default: - TTL is disabled
        """
        return self._values.get('time_to_live_attribute')

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        """The write capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        default
        :default: 5
        """
        return self._values.get('write_capacity')

    @builtins.property
    def regions(self) -> typing.List[str]:
        """Array of environments to create DynamoDB tables in.

        The tables will all be created in the same account.

        stability
        :stability: experimental
        """
        return self._values.get('regions')

    @builtins.property
    def table_name(self) -> str:
        """Name of the DynamoDB table to use across all regional tables.

        This is required for global tables.

        stability
        :stability: experimental
        """
        return self._values.get('table_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GlobalTableProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["GlobalTable", "GlobalTableProps", "__jsii_assembly__"]

publication.publish()
