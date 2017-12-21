### AWS Command Line Interface installation and configuration.

The AWS CLI is an open source tool built on top of the AWS SDK for Python (Boto) that provides commands for interacting with AWS services. With minimal configuration, you can start using all of the functionality provided by the AWS Management Console from your favorite terminal program.

##### Install

Your can install the AWS CLI with pip

```
pip install awscli
```

##### Configure

After you have installed the AWS CLI, you can run the `aws configure` commond to interactively configure your credential, default region and output format.

The command `aws configure list` shows current configuration.

```
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************WP6Q shared-credentials-file
secret_key     ****************YJk+ shared-credentials-file
    region                us-west-1      config-file    ~/.aws/config
```

From [What Is the AWS Command Line Interface?](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

