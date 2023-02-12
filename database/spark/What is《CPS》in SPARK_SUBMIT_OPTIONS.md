# What is <CPS> in SPARK_SUBMIT_OPTIONS?

> https://stackoverflow.com/questions/50259794/what-is-cps-in-spark-submit-options

> 2018-05-09T18:20:27

AWS EMR `/etc/zeppelin/conf/zeppelin-env.sh`, it has this

```
export SPARK_SUBMIT_OPTIONS="$SPARK_SUBMIT_OPTIONS \
--conf 'spark.executorEnv.PYTHONPATH=/usr/lib/spark/python/lib/py4j-src.zip:/usr/lib/spark/python/:<CPS>{{PWD}}/pyspark.zip<CPS>{{PWD}}/py4j-src.zip' \
--conf spark.yarn.isPython=true"
```

what is this <CPS> in spark.executorEnv.PYTHONPATH?

## <CPS> classpath separator

CPS = "classpath separator" (e.g., ':' on Linux and ';' on Windows)

See [ResourceManagerRest.md should document <CPS> and "{{", "}}" meanings](https://issues.apache.org/jira/browse/YARN-6554) for a reference.

It's a little odd that this setting you see is mixing both <CPS> and ':'. Really, it should probably use <CPS> in place of all of the ':'s in order to be platform independent. However, since EMR only supports running on AmazonLinux, it does not need to be as platform independent.


## ResourceManagerRest.md should document <CPS> and "{{", "}}" meanings

The docs should mention the meaning of <CPS>, "" and "". These are explained fully in the code.

```
063      /**
064       * This constant is used to construct class path and it will be replaced with
065       * real class path separator(':' for Linux and ';' for Windows) by
066       * NodeManager on container launch. User has to use this constant to construct
067       * class path if user wants cross-platform practice i.e. submit an application
068       * from a Windows client to a Linux/Unix server or vice versa.
069       */
070      @Public
071      @Unstable
072      public static final String CLASS_PATH_SEPARATOR= "<CPS>";
073    
074      /**
075       * The following two constants are used to expand parameter and it will be
076       * replaced with real parameter expansion marker ('%' for Windows and '$' for
077       * Linux) by NodeManager on container launch. For example: {{VAR}} will be
078       * replaced as $VAR on Linux, and %VAR% on Windows. User has to use this
079       * constant to construct class path if user wants cross-platform practice i.e.
080       * submit an application from a Windows client to a Linux/Unix server or vice
081       * versa.
082       */
083      @Public
084      @Unstable
085      public static final String PARAMETER_EXPANSION_LEFT="{{";
086    
087      /**
088       * User has to use this constant to construct class path if user wants
089       * cross-platform practice i.e. submit an application from a Windows client to
090       * a Linux/Unix server or vice versa.
091       */
092      @Public
093      @Unstable
094      public static final String PARAMETER_EXPANSION_RIGHT="}}";
095    
```