### Creating an Amazon Kinesis Data Firehose Delivery Stream

You can use the AWS Management Console or an AWS SDK to create a Kinesis Data Firehose delivery stream to your chosen destination. 

You can update the configuration of your Kinesis Data Firehose delivery stream at any time after it’s created, using the Kinesis Data Firehose console or UpdateDestination. Your Kinesis Data Firehose delivery stream remains in the **ACTIVE** state while your configuration is updated, and you can continue to send data. The updated configuration normally takes effect within a few minutes. **The version number of a Kinesis Data Firehose delivery stream is increased by a value of 1 after you update the configuration, and it is reflected in the delivered Amazon S3 object name.** For more information, see [Amazon S3 Object Name Format](https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html#s3-object-name).

Open the Kinesis Firehose console at https://console.aws.amazon.com/firehose/.

##### Delivery stream name
The name of your Kinesis Data Firehose delivery stream.

##### Source

- Direct PUT or other sources: Choose this option to create a Kinesis Data Firehose delivery stream that producer applications write directly to.

- Kinesis stream: Choose this option to configure a Kinesis Data Firehose delivery stream that uses a Kinesis stream as a data source. You can then use Amazon Kinesis Data Firehose to read data easily from an existing Kinesis stream and load it into destinations. 

##### Transform records

On the Transform records with AWS Lambda page, enter values for the fields 'Record transformation'

> Choose Disabled to create a Kinesis Data Firehose delivery stream that does not transform incoming data. Choose Enabled to specify a Lambda function that Kinesis Data Firehose can invoke to transform incoming data before delivering it. 

##### Choose Amazon S3 for Your Destination

Amazon Kinesis Data Firehose can send records to Amazon S3, Amazon Redshift, or Amazon Elasticsearch Service.

To choose Amazon S3 for your destination, on the Choose destination page, enter values for the following fields:

- Destination

> Choose Amazon S3.

- Destination S3 bucket

> Choose an S3 bucket that you own where the streaming data should be delivered. You can create a new S3 bucket or choose an existing one.

- Destination S3 bucket prefix

> (Optional) To use the default prefix for S3 objects, leave this option blank. Kinesis Data Firehose automatically uses a prefix in "YYYY/MM/DD/HH" UTC time format for delivered S3 objects. You can add to the start of this prefix. For more information, see [Amazon S3 Object Name Format](https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html#s3-object-name).

- Source record S3 backup

> Choose Disabled to disable source record backup. If you enable data transformation with Lambda, you can enable source record backup to deliver untransformed incoming data to a separate S3 bucket. You can add to the start of the "YYYY/MM/DD/HH" UTC time prefix generated by Kinesis Data Firehose. **You cannot disable source record backup after you enable it.**

#### Configure settings

On the Configure settings page, enter values for the following fields:

- Buffer size, Buffer interval

> Kinesis Data Firehose buffers incoming data before delivering it to Amazon S3. You can choose a buffer size (1–128 MBs) or buffer interval (60–900 seconds); whichever condition is satisfied first triggers data delivery to Amazon S3. If you enable data transformation, the buffer interval applies from the time transformed data is received by Kinesis Data Firehose to the data delivery to Amazon S3. In circumstances where data delivery to the destination falls behind data writing to the delivery stream, Kinesis Data Firehose raises the buffer size dynamically to catch up and ensure that all data is delivered to the destination.

- Compression

> Choose GZIP, Snappy, or Zip data compression, or no data compression. Snappy or Zip compression are not available for delivery streams with Amazon Redshift as the destination.
> We can use GZIP here.

- Encryption

> Kinesis Data Firehose supports Amazon S3 server-side encryption with AWS Key Management Service (AWS KMS) for encrypting delivered data in Amazon S3. You can choose to not encrypt the data or to encrypt with a key from the list of AWS KMS keys that you own. For more information, see [Protecting Data Using Server-Side Encryption with AWS KMS–Managed Keys (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html).

- Error logging

> Kinesis Data Firehose can log the Lambda invocation, if data transformation is enabled, and send data delivery errors to CloudWatch Logs so that you can view the specific error logs if the Lambda invocation or data delivery fails. For more information, see [Monitoring with Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html).

- IAM role

> You can choose to create a new role where required permissions are assigned automatically, or choose an existing role created for Kinesis Data Firehose. The role is used to grant Kinesis Data Firehose access to your S3 bucket, AWS KMS key (if data encryption is enabled), and Lambda function (if data transformation is enabled). The console might create a role with placeholders. You can safely ignore or safely delete lines with %FIREHOSE_BUCKET_NAME%, %FIREHOSE_DEFAULT_FUNCTION%, or %FIREHOSE_DEFAULT_VERSION%. For more information, see [Grant Kinesis Data Firehose Access to an Amazon S3 Destination](https://docs.aws.amazon.com/firehose/latest/dev/monitoring-with-cloudwatch-logs.html).

The new Kinesis Data Firehose delivery stream takes a few moments in the Creating state before it is available. After your Kinesis Data Firehose delivery stream is in an Active state, you can start sending data to it from your producer.

##### Amazon S3 Object Name Format

Kinesis Data Firehose adds a UTC time prefix in the format YYYY/MM/DD/HH before writing objects to Amazon S3. This prefix creates a logical hierarchy in the bucket, where each forward slash (/) creates a level in the hierarchy. You can modify this structure by adding to the start of the prefix when you create the Kinesis Data Firehose delivery stream. For example, add myApp/ to use the myApp/YYYY/MM/DD/HH prefix or myApp to use the myApp YYYY/MM/DD/HH prefix.

The S3 object name follows the pattern

DeliveryStreamName-DeliveryStreamVersion-YYYY-MM-DD-HH-MM-SS-RandomString, where DeliveryStreamVersion begins with 1 and increases by 1 for every configuration change of the Kinesis Data Firehose delivery stream. You can change Kinesis Data Firehose delivery stream configurations (for example, the name of the S3 bucket, buffering hints, compression, and encryption) using the Kinesis Data Firehose console, or by using the [UpdateDestination](https://docs.aws.amazon.com/firehose/latest/APIReference/API_UpdateDestination.html) API operation.


From: [Creating an Amazon Kinesis Data Firehose Delivery Stream](https://docs.aws.amazon.com/firehose/latest/dev/basic-create.html)

[使用 AWS 开发工具包对Kinesis 数据传输流进行写入操作](https://docs.aws.amazon.com/zh_cn/firehose/latest/dev/writing-with-sdk.html)

[aws firehose  create-delivery-stream](https://docs.aws.amazon.com/cli/latest/reference/firehose/create-delivery-stream.html)
