from localstack.aws.api.lambda_ import EventSourceMappingConfiguration
from localstack.services.lambda_.invocation.lambda_models import CodeSigningConfig, Function, Layer
from localstack.services.stores import AccountRegionBundle, BaseStore, LocalAttribute
from localstack.utils.tagging import TaggingService


class LambdaStore(BaseStore):
    # maps function names to the respective Function
    functions: dict[str, Function] = LocalAttribute(default=dict)

    # maps EventSourceMapping UUIDs to the respective EventSourceMapping
    event_source_mappings: dict[str, EventSourceMappingConfiguration] = LocalAttribute(default=dict)

    # maps CodeSigningConfig ARNs to the respective CodeSigningConfig
    code_signing_configs: dict[str, CodeSigningConfig] = LocalAttribute(default=dict)

    # maps layer names to Layers
    layers: dict[str, Layer] = LocalAttribute(default=dict)

    # maps resource ARNs for EventSourceMappings and CodeSigningConfiguration to tags
    TAGS = LocalAttribute(default=TaggingService)


lambda_stores = AccountRegionBundle("lambda", LambdaStore)
