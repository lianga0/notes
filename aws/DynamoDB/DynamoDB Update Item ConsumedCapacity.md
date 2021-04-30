## DynamoDB Update Item ConsumedCapacity

> 2021.04.26

最近DynamoDB每月账单异常的高，老板出来打人了。所以检查下原因：

DynamoDB Item支持TTL过期，如果你想维持项目不过期，那么每次读之后，自然会想到顺便更新下TTL。
在DynamoDB中TTL为你指定的某个属性，其值为一个整数。但是更新TTL操作需要消耗的ConsumedCapacity和直接重新写入整个Item的开销是一致的。
从DynamoDB内部来看，更新Item任何一个属性，DynamoDB都会消耗重新写入整个Item的ConsumedCapacity。

> Reference: https://stackoverflow.com/questions/60373531/how-does-dynamodb-consume-capacity-when-updating-item-in-tables

> To modify an item, DynamoDB internally needs to read the entire item, modify it and write it back to disk, so you pay for the entire item, not the small part which you modified.

> Also, DynamoDB writes are significantly more expensive than reads, and their price already includes the (strongly-consistent) read involved: You don't pay extra if you have condition expressions or any ReturnValues option (but note that even if a condition expression caused a write not to be done, you still pay for it).

Here are some relevant quotes from the official documentation:

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html

UpdateItem—Modifies a single item in the table. DynamoDB considers the size of the item as it appears before and after the update. The provisioned throughput consumed reflects the larger of these item sizes. Even if you update just a subset of the item's attributes, UpdateItem will still consume the full amount of provisioned throughput (the larger of the "before" and "after" item sizes).

https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ReturnValues

There is no additional cost associated with requesting a return value aside from the small network and processing overhead of receiving a larger response. No read capacity units are consumed.

TEST CODE

```
'use strict';

const AWS = require('aws-sdk');
const attr = require('dynamodb-data-types').AttributeValue;

let fs = require('fs')

fs.readFile('88-6A-E3-3A-40-6B_cache.txt', (err, data) => {
    let jsonString = data.toString("utf-8")
    let dynamodb = new AWS.DynamoDB({endpoint: null, region: "us-west-1"});

    /*
    var paramss = {
        Item: attr.wrap(JSON.parse(jsonString)),
        ReturnConsumedCapacity: "TOTAL",
        TableName: "test"
    };
    dynamodb.putItem(paramss, function(err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else     console.log(data);           // successful response

        //data = { ConsumedCapacity: { TableName: 'test', CapacityUnits: 73 } }

    });
*/

    const expressionAttributeValues = {
        ":val": {
            N: "1631144574"
        }
    };
    let params = {
        Key: {
            _id: {
                S: "88:6A:E3:3A:40:6B",
            },
        },
        ExpressionAttributeValues: expressionAttributeValues,
        UpdateExpression: 'set expireTTL=:val',
        ReturnConsumedCapacity: "TOTAL",
        TableName: "test"
    }

    dynamodb.updateItem(params, function (err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else console.log(data);           // successful response
        // { ConsumedCapacity: { TableName: 'test', CapacityUnits: 73 } }
    });
});
```
