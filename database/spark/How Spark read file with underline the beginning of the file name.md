# How Spark read file with underline the beginning of the file name?

> 2016.06

> https://stackoverflow.com/questions/38477630/how-spark-read-file-with-underline-the-beginning-of-the-file-name/38479545


When I use Spark to parse log files, I notice that if the first character of filename is `_` , the result will be empty. Here is my test code:

```
SparkSession spark = SparkSession
  .builder()
  .appName("TestLog")
  .master("local")
  .getOrCreate();
JavaRDD<String> input = spark.read().text("D:\\_event_2.log").javaRDD();
System.out.println("size : " + input.count());
```

If I modify the file name to `event_2.log`, the code will run it correctly. I found that the text function is defined as:

```
@scala.annotation.varargs
def text(paths: String*): Dataset[String] = {
  format("text").load(paths : _*).as[String](sparkSession.implicits.newStringEncoder)
}
```

I think it could be due to `_` being scala's placeholder. How can I avoid this problem?


## Answer

This has nothing to do with Scala. Spark uses Hadoop Input API to read file, which ignore every file that starts with underscore(_) or dot (.)

I don't know how to disable this in Spark though.

> Thanks , I find the code where ignore file with `_` . It's overwritable using HadoopRDD with a custom PathFilter. The following question would make a good answer!

# Which files are ignored as input by mapper?

> https://stackoverflow.com/questions/19830264/which-files-are-ignored-as-input-by-mapper/19832011#19832011

I'm chaining multiple MapReduce jobs and want to pass along/store some meta information (e.g. configuration or name of original input) with the results. At least the file "_SUCCESS" and also anything in the directory "_logs" seams to be ignored.

Are there any filename patterns which are by default ignored by the InputReader? Or is this just a fixed limited list?

## Answer

The `FileInputFormat` uses the following hiddenFileFilter by default:

```
  private static final PathFilter hiddenFileFilter = new PathFilter(){
      public boolean accept(Path p){
        String name = p.getName(); 
        return !name.startsWith("_") && !name.startsWith("."); 
      }
    }; 
```

So if you uses any `FileInputFormat` (such as `TextInputFormat`, `KeyValueTextInputFormat`, `SequenceFileInputFormat`), the hidden files (the file name starts with "_" or ".") will be ignored.

You can use `FileInputFormat.setInputPathFilter` to set your custom `PathFilter`. Remember that the `hiddenFileFilter` is always active.
