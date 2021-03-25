# MongoDB Atlas API

Examples for using python to interrogate the MongoDB Atlas Public API

## Setup

Create the following environment variables:

ATLAS_API_PUBLIC \
ATLAS_API_PRIVATE \
ATLAS_PROJECT_ID \
ATLAS_CLUSTER_NAME

These will be used by the cli commands if they exist but can also be passed in manually if required.
The usage examples assume these have been created.

## Example usage

```
get-process-measurements --process-id atlas-ct3yft-shard-00-02.bj7ub.mongodb.net:27017
```

```
get-cluster-info
```

```
get-processes
```

```
get-process-by-id --process-id atlas-ct3yft-shard-00-02.bj7ub.mongodb.net:27017
```

```
get-process-log --hostname atlas-ct3yft-shard-00-02.bj7ub.mongodb.net
```