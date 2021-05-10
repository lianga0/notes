## Elasticsearch Mapping

Mapping is the process of defining how a document, and the fields it contains, are stored and indexed. For instance, use mappings to define:

- which string fields should be treated as full text fields.
- which fields contain numbers, dates, or geolocations.
- the format of date values.
- custom rules to control the mapping for dynamically added fields.

### Dynamic mapping

Fields and mapping types do not need to be defined before being used. Thanks to dynamic mapping, new field names will be added automatically, just by indexing a document. New fields can be added both to the top-level mapping type, and to inner object and nested fields.

The dynamic mapping rules can be configured to customise the mapping that is used for new fields.

### Explicit mappings

You know more about your data than Elasticsearch can guess, so while dynamic mapping can be useful to get started, at some point you will want to specify your own explicit mappings.

You can create field mappings when you create an index and add fields to an existing index.

### Create an index with an explicit mapping

You can use the create index API to create a new index with an explicit mapping.

```
curl -X PUT "http://vpc-drs-es-service-ige5u5edk3kcizlpwbgxsg4pe4.ap-northeast-1.es.amazonaws.com/extender?pretty" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "mac" : {
          "type" : "keyword"
        } 
    }
  }
}
'
```



Reference: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html

