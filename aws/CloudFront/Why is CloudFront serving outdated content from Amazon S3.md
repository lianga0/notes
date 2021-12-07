# Why is CloudFront serving outdated content from Amazon S3

> https://aws.amazon.com/premiumsupport/knowledge-center/cloudfront-serving-outdated-content-s3/?nc1=h_ls

Last updated: 2021-01-28

I'm using Amazon CloudFront to serve objects stored in Amazon Simple Storage Service (Amazon S3). I updated my objects in S3, but my CloudFront distribution is still serving the previous versions of those files. Why isn't my Amazon S3 content updating on CloudFront? How can I fix this?

## Short description

By default, CloudFront caches a response from Amazon S3 for 24 hours (Default TTL of 86,400 seconds). If your request lands at an edge location that served the Amazon S3 response within 24 hours, then CloudFront uses the cached response even if you updated the content in Amazon S3.

Use one of the following ways to push the updated S3 content from CloudFront:

- Invalidate the S3 objects.
- Use object versioning.


Reference:

[Amazon CloudFront 使文件失效](https://docs.aws.amazon.com/zh_cn/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)

通过边缘缓存使文件失效。查看器下次请求文件时，CloudFront 将返回源以获取文件的最新版本。


[CloudFront 为什么提供来自 Amazon S3 的过时内容？](https://aws.amazon.com/cn/premiumsupport/knowledge-center/cloudfront-serving-outdated-content-s3/)

