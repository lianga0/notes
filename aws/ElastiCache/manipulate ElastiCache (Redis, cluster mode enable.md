### Manipulate Redis (cluster mode enabled) with AWS CLI in ElastiCache

You can create a **Redis (cluster mode enabled) cluster** (API/CLI: replication group) using the ElastiCache console, the AWS CLI, or the ElastiCache API. A Redis (cluster mode enabled) replication group has from 1 to 15 shards (API/CLI: node groups), a primary cluster in each shard, and up to 5 read replicas in each shard. When you use the ElastiCache console to create the cluster, the number of read replicas is the same for every shard.

##### Get information about all provisioned clusters 

```
aws elasticache describe-cache-clusters
```

##### Get information about the specific cache cluster

```
aws elasticache describe-cache-clusters --cache-cluster-id my-test-redis-0001-001
```


##### Get information about all replication groups(aka cache cluster in AWS web console).

```
aws elasticache describe-replication-groups
```

##### Get information about the specific replication group.

```
aws elasticache describe-replication-groups --replication-group-id my-test-redis
```

##### Describes one or more of your security groups

```
aws ec2 describe-security-groups
```

A  security  group  is for use with instances either in the EC2-Classic platform or in a specific VPC. A sample output is as following:

```
{
    "SecurityGroups": [
        {
            "IpPermissionsEgress": [
                {
                    "IpProtocol": "-1",
                    "PrefixListIds": [],
                    "IpRanges": [
                        {
                            "CidrIp": "0.0.0.0/0"
                        }
                    ],
                    "UserIdGroupPairs": [],
                    "Ipv6Ranges": []
                }
            ],
            "Description": "sg.ElastiCache",
            "IpPermissions": [
                {
                    "PrefixListIds": [],
                    "FromPort": 6379,
                    "IpRanges": [
                        {
                            "CidrIp": "0.0.0.0/0"
                        }
                    ],
                    "ToPort": 6379,
                    "IpProtocol": "tcp",
                    "UserIdGroupPairs": [],
                    "Ipv6Ranges": [
                        {
                            "CidrIpv6": "::/0"
                        }
                    ]
                }
            ],
            "GroupName": "sg.ElastiCache",
            "VpcId": "vpc-7b4f5f19",
            "OwnerId": "944809154377",
            "GroupId": "sg-5aa7a13d"
        },
        ......
```

##### Creating a Redis (cluster mode enabled) Cluster with Replicas from Scratch (AWS CLI)

```
aws elasticache create-replication-group --replication-group-id drs-test-redis \
--replication-group-description drs-test-redis-cluster \
--cache-node-type cache.t2.micro \
--num-node-groups 1 \
--replicas-per-node-group 0 \
--cache-parameter-group default.redis3.2.cluster.on \
--engine redis \
--engine-version 3.2.10 \
--security-group-ids sg-5aa7a13d \
--tags Key=project,Value=drs-test-liangao
```

When you create a Redis (cluster mode enabled) replication group from scratch, you create the replication group and all its nodes with a single call to the AWS CLI `create-replication-group` command. Include the following parameters.

`--replication-group-id`

    The name of the replication group you are creating.

    Redis (cluster mode enabled) Replication Group naming constraints

        > Must contain from 1 to 20 alphanumeric characters or hyphens.

        > Must begin with a letter.

        > Cannot contain two consecutive hyphens.

        > Cannot end with a hyphen.

`--replication-group-description`

    (Optional) Description of the replication group.

`--cache-node-type` The node type for each node in the replication group.

    Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts.

    All T2 instances are created in an Amazon Virtual Private Cloud (Amazon VPC).

    Redis backup and restore is not supported for T2 instances.

    Redis append-only files (AOF) are not supported for T1 or T2 instances.

    Redis Multi-AZ with automatic failover is not supported on T1 instances.

    Redis Multi-AZ with automatic failover is supported on T2 instances only when running Redis (cluster mode enabled) - version 3.2.4 or later with the default.redis3.2.cluster.on parameter group or one derived from it.

    Redis configuration variables appendonly and appendfsync are not supported on Redis version 2.8.22 and later.

`--cache-parameter-group`

    Specify the default.redis3.2.cluster.on parameter group or a parameter group derived from default.redis3.2.cluster.on to create a Redis (cluster mode enabled) replication group.

`--num-node-groups`

    The number of node groups in this replication group. Valid values are 1 to 15.

`--replicas-per-node-group`

    The number of replica nodes in each node group. Valid values are 1 to 5.

`--security-group-ids`

    One or more Amazon VPC security groups associated with this replication group.

    Use this parameter only when you are creating a replication group in an Amazon Virtual Private Cloud (Amazon VPC).

`--tags`

    A list of cost allocation tags to be added to this resource. A tag is a key-value pair. A tag key does not have to be accompanied by a tag value.


##### Add Redis Shards

```
aws elasticache modify-replication-group-shard-configuration \
    --replication-group-id my-test-redis \
    --node-group-count 2 \
    --apply-immediately
```


##### Delete Redis Shards

You can use the AWS CLI to remove one or more shards from your Redis (cluster mode enabled) cluster. You cannot remove all the shards in a replication group. Instead, you must delete the replication group.

```
aws elasticache modify-replication-group-shard-configuration \
    --replication-group-id my-test-redis \
    --node-group-count 1 \
    --node-groups-to-remove "0002"  "0003" \
    --apply-immediately     
```

`apply-immediately` is required. Specifies the shard reconfiguration operation is to be started immediately.

`replication-group-id`is required. Specifies which replication group (cluster) the shard reconfiguration operation is to be performed on.

`node-group-count` is required. Specifies the number of shards (node groups) to exist when the operation is completed. When removing shards, the value of `--node-group-count` must be less than the current number of shards.

`node-groups-to-remove`is required when `--node-group-count` is less than the current number of node groups (shards). A list of shard (node group) IDs to remove from the replication group.


##### Deletes an existing replication group.

```
aws elasticache delete-replication-group --replication-group-id <value>
```

Deletes an existing replication group. By default, this operation deletes the entire replication group, including the primary/primaries and all of the read replicas. If the replication group has only one primary, you can optionally delete only the read replicas, while retaining the primary by setting "RetainPrimaryCluster=true".

When you receive a successful response from this operation, Amazon ElastiCache immediately begins deleting the selected resources; you cannot cancel or revert this operation.

Note: This operation is valid for Redis only.

From: [Scaling for Amazon ElastiCache for Redis—Redis (cluster mode enabled)](https://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/scaling-redis-cluster-mode-enabled.html#redis-cluster-resharding-online-add-cli)