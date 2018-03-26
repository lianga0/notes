### aws dynamodb create-table

1. 创建表命令

```
aws dynamodb create-table --table-name xx-cache-xxx --attribute-definitions AttributeName=_id,AttributeType=S --key-schema AttributeName=_id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

若创建成功，会输出刚创建的表详细信息(TableDescription)，`aws dynamodb tag-resource`命令中需要用到"TableArn"信息：

```
{
    "TableDescription": {
        "TableArn": "arn:aws:dynamodb:ap-northeast-1:944809154377:table/xx-cache-xxx",
        "AttributeDefinitions": [
            {
                "AttributeName": "_id",
                "AttributeType": "S"
            }
        ],
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "WriteCapacityUnits": 5,
            "ReadCapacityUnits": 5
        },
        "TableSizeBytes": 0,
        "TableName": "xx-cache-xxx",
        "TableStatus": "CREATING",
        "TableId": "aa4d6b6a-201b-45cd-a094-42319b34da98",
        "KeySchema": [
            {
                "KeyType": "HASH",
                "AttributeName": "_id"
            }
        ],
        "ItemCount": 0,
        "CreationDateTime": 1522030207.222
    }
}
```

2. 列出当前区域所有表名

```
aws dynamodb list-tables
```

输出信息如下：

```
{
    "TableNames": [
        "xx-cache-xxxx",
        "xx-cache-xxx"
    ]
}
```


3. 列出指定表名详细信息

```
aws dynamodb describe-table --table-name xx-cache-xxx
```

输出信息如下，其中"TableArn"信息可用于其他命令：

```
{
    "Table": {
        "TableArn": "arn:aws:dynamodb:ap-northeast-1:944809154377:table/xx-cache-xxx",
        "AttributeDefinitions": [
            {
                "AttributeName": "_id",
                "AttributeType": "S"
            }
        ],
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "WriteCapacityUnits": 5,
            "ReadCapacityUnits": 5
        },
        "TableSizeBytes": 0,
        "TableName": "xx-cache-xxx",
        "TableStatus": "ACTIVE",
        "TableId": "aa4d6b6a-201b-45cd-a094-42319b34da98",
        "KeySchema": [
            {
                "KeyType": "HASH",
                "AttributeName": "_id"
            }
        ],
        "ItemCount": 0,
        "CreationDateTime": 1522030207.222
    }
}
```

4. 为指定表创建Tag标签

```
aws dynamodb  tag-resource --resource-arn arn:aws:dynamodb:ap-northeast-1:944809154377:table/xx-cache-xxx --tags Key=Product,Value=xxx-xx
aws dynamodb  tag-resource --resource-arn arn:aws:dynamodb:ap-northeast-1:944809154377:table/xx-cache-xxx --tags Key=Project,Value=xxx-xx-xxx
```

[aws dynamodb](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/index.html#cli-aws-dynamodb)
