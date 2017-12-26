### The Elastic Beanstalk Command Line Interface (EB CLI)

The EB CLI is a command line interface for Elastic Beanstalk that provides interactive commands that simplify creating, updating and monitoring environments from a local repository. Use the EB CLI as part of your everyday development and testing cycle as an alternative to the AWS Management Console.

##### EB CLI is more friendly than AWS CLI to operate Elastic Beanstalk

Previously, Elastic Beanstalk supported a separate CLI that provided direct access to API operations called the Elastic Beanstalk API CLI. This has been replaced with the AWS CLI, which provides the same functionality but for all AWS services' APIs.

With the AWS CLI you have direct access to the Elastic Beanstalk API. The AWS CLI is great for scripting, but is not as easy to use from the command line because of the number of commands that you need to run and the number of parameters on each command.

##### Install the Elastic Beanstalk Command Line Interface (EB CLI)

```
pip install awsebcli --upgrade
```

The --upgrade option tells pip to upgrade any requirements that are already installed.

##### Configure the EB CLI

After installing the EB CLI, you are ready to configure your project folder with `eb init`.

Run `eb init` in your application's project directory to configure the EB CLI and your project.

The following example shows the configuration steps when running `eb init` for the first time in a project folder named `eb`:

1.First, the EB CLI prompts you to select a region. Type the number that corresponds to the region that you would like to use and press **Enter**.

```
$ eb init

Select a default region
1) us-east-1 : US East (N. Virginia)
2) us-west-1 : US West (N. California)
3) us-west-2 : US West (Oregon)
4) eu-west-1 : EU (Ireland)
5) eu-central-1 : EU (Frankfurt)
6) ap-south-1 : Asia Pacific (Mumbai)
7) ap-southeast-1 : Asia Pacific (Singapore)
8) ap-southeast-2 : Asia Pacific (Sydney)
9) ap-northeast-1 : Asia Pacific (Tokyo)
10) ap-northeast-2 : Asia Pacific (Seoul)
11) sa-east-1 : South America (Sao Paulo)
12) cn-north-1 : China (Beijing)
13) us-east-2 : US East (Ohio)
14) ca-central-1 : Canada (Central)
15) eu-west-2 : EU (London)
(default is 3): 2
```

2.If you don't set up the credentials before(I have set credentials in AWS CLI, so eb skipped step 2), provide your access key and secret key so that the EB CLI can manage resources for you. 

```
You have not yet set up your credentials or your credentials are incorrect
You must provide your credentials.
(aws-access-id): AKIAJOUAASEXAMPLE
(aws-secret-key): 5ZRIrtTM4ciIAvd4EXAMPLEDtm+PiPSzpoK
```

3.An application in Elastic Beanstalk is a resource that contains a set of application versions (source), environments, and saved configurations that are associated with a single web application. Each time you deploy your source code to Elastic Beanstalk using the EB CLI, a new application version is created and added to the list.

```
Enter Application Name
(default is "eb"): DRS
Application DRS has been created.
```

4.Select a platform that matches the language or framework that your web application is developed in.

```
Select a platform.
1) Multi-container Docker
2) Node.js
3) PHP
4) Python
5) Ruby
6) Tomcat
7) IIS
8) Docker
9) GlassFish
10) Go
11) Java
12) Packer
(default is 1): 4

Select a platform version.
1) Python 3.6
2) Python 3.4
3) Python
4) Python 2.7
5) Python 3.4 (Preconfigured - Docker)
(default is 1): 4
Cannot setup CodeCommit because there is no Source Control setup, continuing with initialization
```

5.Choose yes to assign an SSH key pair to the instances in your Elastic Beanstalk environment, allowing you to connect directly to them for troubleshooting.

```
Do you want to set up SSH for your instances?
(Y/n): Y

Select a keypair.
1) airsupport_test
2) DiamondRing
3) DiamondRing-Scanner
4) DiamondRing-Speedtest
5) Diamondring_staging
6) ITIS_KEY_zabbix
7) ITIS_team_key
8) ITIS_team_key#2
9) wcc_server_key_nc
10) www.drcleaner.com
11) [ Create new KeyPair ]
(default is 10): 5
```

Your EB CLI installation is now configured and ready to use. The configure information is saved in the file `eb/.elasticbeanstalk/config.yml`.

##### eb create

To create your first environment, run `eb create` and follow the prompts. If your project directory has source code in it, the EB CLI will bundle it up and deploy it to your environment. Otherwise, a sample application will be used.

```
$ eb create -﻿-﻿tags project=drs-test-liangao --instance_profile aws-elasticbeanstalk-ec2-role-liangao --instance_type t2.micro

Enter Environment Name
(default is DRS-dev): DRS-dev
Enter DNS CNAME prefix
(default is DRS-dev): drs-dev

Select a load balancer type
1) classic
2) application
3) network
(default is 1):1
Creating application version archive "app-171226_094610".
Uploading DRS/app-171226_094610.zip to S3. This may take a while.
Upload Complete.
Environment details for: DRS-dev
  Application name: DRS
  Region: us-west-1
  Deployed Version: app-171226_094610
  Environment ID: e-fapk3p2ywr
  Platform: arn:aws:elasticbeanstalk:us-west-1::platform/Python 2.7 running on 64bit Amazon Linux/2.6.1
  Tier: WebServer-Standard-1.0
  CNAME: drs-dev.us-west-1.elasticbeanstalk.com
  Updated: 2017-12-26 01:46:18.084000+00:00
Printing Status:
INFO: createEnvironment is starting.
INFO: Using elasticbeanstalk-us-west-1-944809154377 as Amazon S3 storage bucket for environment data.
INFO: Created security group named: sg-7f708506
INFO: Created load balancer named: awseb-e-f-AWSEBLoa-1OUSZRQNMGE9Q
INFO: Created security group named: awseb-e-fapk3p2ywr-stack-AWSEBSecurityGroup-1N6EJHSBRIJRN
INFO: Created Auto Scaling launch configuration named: awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingLaunchConfiguration-1C2INMQ8G2XMY
INFO: Created Auto Scaling group named: awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingGroup-11UYGBJYFI2E7
INFO: Waiting for EC2 instances to launch. This may take a few minutes.
INFO: Created Auto Scaling group policy named: arn:aws:autoscaling:us-west-1:944809154377:scalingPolicy:8c6c3eb0-1aec-4af9-98f5-ba6a8e842c21:autoScalingGroupName/awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingGroup-11UYGBJYFI2E7:policyName/awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingScaleUpPolicy-17V6YH94RDFW5
INFO: Created Auto Scaling group policy named: arn:aws:autoscaling:us-west-1:944809154377:scalingPolicy:aa111af8-f0bc-47a3-9c50-4d77f079ce7c:autoScalingGroupName/awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingGroup-11UYGBJYFI2E7:policyName/awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingScaleDownPolicy-158UOJCR87F6O
INFO: Created CloudWatch alarm named: awseb-e-fapk3p2ywr-stack-AWSEBCloudwatchAlarmHigh-DP4G4M4KERYH
INFO: Created CloudWatch alarm named: awseb-e-fapk3p2ywr-stack-AWSEBCloudwatchAlarmLow-1WMY6DBZ9FL77
INFO: Successfully launched environment: DRS-dev
```

`--instance_type`: The type of Amazon EC2 instance to use in the environment.

The instance types available depend on platform, solution stack (configuration) and region. To get a list of available instance types for your solution stack of choice, use the `DescribeConfigurationOptions` action in the API, `describe-configuration-options` command in the `AWS CLI`. For example:

```
aws elasticbeanstalk describe-configuration-options --environment-name DRS-dev
```



```
{
            "Name": "InstanceType",
            "UserDefined": false,
            "DefaultValue": "t1.micro",
            "ChangeSeverity": "RestartEnvironment",
            "Namespace": "aws:autoscaling:launchconfiguration",
            "ValueType": "Scalar",
            "ValueOptions": [
                "t2.micro",
                "t2.small",
                "t2.medium",
                "t2.large",
                "t2.xlarge",
                "t2.2xlarge",
                "m3.medium",
                "m3.large",
                "m3.xlarge",
                "m3.2xlarge",
                "c3.large",
                "c3.xlarge",
                "c3.2xlarge",
                "c3.4xlarge",
                "c3.8xlarge",
                "t1.micro",
                "t2.nano",
                "m1.small",
                "m1.medium",
                "m1.large",
                "m1.xlarge",
                "c1.medium",
                "c1.xlarge",
                .........
```


##### eb status
Run `eb status` to see the current status of your environment. When the status is ready, the sample application is available at elasticbeanstalk.com and the environment is ready to be updated.

```
$ eb status
Environment details for: DRS-dev
  Application name: DRS
  Region: us-west-1
  Deployed Version: app-171226_094610
  Environment ID: e-fapk3p2ywr
  Platform: arn:aws:elasticbeanstalk:us-west-1::platform/Python 2.7 running on 64bit Amazon Linux/2.6.1
  Tier: WebServer-Standard-1.0
  CNAME: drs-dev.us-west-1.elasticbeanstalk.com
  Updated: 2017-12-26 01:49:37.243000+00:00
  Status: Ready
  Health: Green
```

##### eb health

Use the `eb health` command to view health information about the instances in your environment and the state of your environment overall. Use the `--refresh` option to view health in an interactive view that updates every 10 seconds.

```
 DRS-dev                                               Ok                                              2017-12-26 10:23:00
WebServer                                                                   Python 2.7 running on 64bit Amazon Linux/2.6.1
  total      ok    warning  degraded  severe    info   pending  unknown
    1        1        0        0        0        0        0        0

  instance-id           status     cause                                                                          health
    Overall             Ok
  i-0d13f635d685804d7   Ok

  instance-id           r/sec    %2xx   %3xx   %4xx   %5xx      p99      p90      p75     p50     p10           requests
    Overall             0.0         -      -      -      -         -        -       -       -       -
  i-0d13f635d685804d7   0.0         -      -      -      -         -        -       -       -       -

  instance-id           type       az   running     load 1  load 5      user%  nice%  system%  idle%   iowait%       cpu
  i-0d13f635d685804d7   t2.micro   1c   36 mins        0.0     0.0        0.0    0.0      0.0  100.0       0.0

  instance-id           status     id   version             ago                                              deployments
  i-0d13f635d685804d7   Deployed   1    app-171226_094610   34 mins
```

##### eb events

Use `eb events` to see a list of events output by Elastic Beanstalk.

```
eb events
2017-12-26 01:46:17    INFO    createEnvironment is starting.
2017-12-26 01:46:18    INFO    Using elasticbeanstalk-us-west-1-944809154377 as Amazon S3 storage bucket for environment data.
2017-12-26 01:46:26    INFO    Environment health has transitioned to Pending. Initialization in progress (running for 5 seconds). There are no instances.
2017-12-26 01:46:39    INFO    Created security group named: sg-7f708506
2017-12-26 01:46:39    INFO    Created load balancer named: awseb-e-f-AWSEBLoa-1OUSZRQNMGE9Q
2017-12-26 01:46:40    INFO    Created security group named: awseb-e-fapk3p2ywr-stack-AWSEBSecurityGroup-1N6EJHSBRIJRN
2017-12-26 01:46:56    INFO    Created Auto Scaling launch configuration named: awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingLaunchConfiguration-1C2INMQ8G2XMY
2017-12-26 01:47:58    INFO    Created Auto Scaling group named: awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingGroup-11UYGBJYFI2E7
2017-12-26 01:47:58    INFO    Waiting for EC2 instances to launch. This may take a few minutes.
2017-12-26 01:47:58    INFO    Created Auto Scaling group policy named: arn:aws:autoscaling:us-west-1:944809154377:scalingPolicy:8c6c3eb0-1aec-4af9-98f5-ba6a8e842c21:autoScalingGroupName/awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingGroup-11UYGBJYFI2E7:policyName/awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingScaleUpPolicy-17V6YH94RDFW5
2017-12-26 01:47:58    INFO    Created Auto Scaling group policy named: arn:aws:autoscaling:us-west-1:944809154377:scalingPolicy:aa111af8-f0bc-47a3-9c50-4d77f079ce7c:autoScalingGroupName/awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingGroup-11UYGBJYFI2E7:policyName/awseb-e-fapk3p2ywr-stack-AWSEBAutoScalingScaleDownPolicy-158UOJCR87F6O
2017-12-26 01:47:58    INFO    Created CloudWatch alarm named: awseb-e-fapk3p2ywr-stack-AWSEBCloudwatchAlarmHigh-DP4G4M4KERYH
2017-12-26 01:47:58    INFO    Created CloudWatch alarm named: awseb-e-fapk3p2ywr-stack-AWSEBCloudwatchAlarmLow-1WMY6DBZ9FL77
2017-12-26 01:48:26    INFO    Added instance [i-0d13f635d685804d7] to your environment.
2017-12-26 01:49:26    INFO    Environment health has transitioned from Pending to Ok. Initialization completed 47 seconds ago and took 2 minutes.
2017-12-26 01:49:37    INFO    Successfully launched environment: DRS-dev
```

##### eb logs

Use `eb logs` to pull logs from an instance in your environment. By default, `eb logs` pull logs from the first instance launched and displays them in standard output. You can specify an instance ID with the `--instance` option to get logs from a specific instance.

The `--all` option pulls logs from all instances and saves them to subdirectories under `.elasticbeanstalk/logs`.

##### eb open

When the environment creation process completes, open your web site with `eb open`.

##### eb deploy

Once the environment is up and ready, you can update it using `eb deploy`.

This command works better with some source code to bundle up and deploy. When you run eb deploy, the EB CLI bundles up the contents of your project directory and deploys it to your environment.

Note

> If you have initialized a git repository in your project folder, the EB CLI will always deploy the latest commit, even if you have pending changes. Commit your changes prior to running eb deploy to deploy them to your environment.

##### eb tags

Add, delete, update, and list Elastic Beanstalk environment tags. For details about environment tagging, see [Tagging Resources in Your Elastic Beanstalk Environment](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.tagging.html).

```
eb tags [environment-name] -l|--list

eb tags [environment-name] -a|--add key1=value1[,key2=value2 ...]

eb tags [environment-name] -u|--update key1=value1[,key2=value2 ...]

eb tags [environment-name] -d|--delete key1[,key2 ...]
```

You can combine the --add, --update, and --delete subcommand options in a single command. At least one of them is required. You can't combined any of these three subcommand options with --list.

If you use the EB CLI to create environments, use the `--tags` option with `eb create` to add tags.

```
$ eb create --tags mytag1=value1,mytag2=value2
```

With the AWS CLI or other API-based clients, use the `--tags` parameter on the create-environment command.

or you can add a tag with the key tag1 and the value value1 with `eb tags` command.

```
$ eb tags --add project=drs-test-liangao
```


##### eb terminate
If you are done using the environment for now, use `eb terminate` to terminate it.

For a full list of available EB CLI commands, check out the [EB CLI Command Reference](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-cmd-commands.html).


Reference: 

[The Elastic Beanstalk Command Line Interface (EB CLI)](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html)

[Install the Elastic Beanstalk Command Line Interface (EB CLI)](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)


[Configure the EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-configuration.html)

[Deploying a Flask Application to AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)

[General Options for All Environments](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-general.html)
