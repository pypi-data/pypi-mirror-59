from os.path import abspath, dirname

from setuptools import setup


LONG_DESCRIPTION = open(dirname(abspath(__file__)) + "/README.md", "r").read()


def install_master():
    try:
        from pip._internal import main as pip_main

        pip_main.main(["install", "mypy-boto3==1.10.48.0"])
    except Exception as e:
        print("Installation of mypy-boto3==1.10.48.0 failed", e)


install_master()


setup(
    name="boto3-stubs",
    version="1.10.48.0",
    packages=["boto3-stubs"],
    url="https://github.com/vemel/mypy_boto3",
    license="MIT License",
    author="Vlad Emelianov",
    author_email="vlad.emelianov.nz@gmail.com",
    description="Type annotations for boto3 1.10.48.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Typed",
    ],
    keywords="boto3 type-annotations boto3-stubs mypy mypy-stubs typeshed autocomplete auto-generated",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    package_data={"boto3-stubs": ["py.typed", "*.pyi", "*/*.pyi"]},
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://mypy-boto3.readthedocs.io/en/latest/",
        "Source": "https://github.com/vemel/mypy_boto3",
        "Tracker": "https://github.com/vemel/mypy_boto3/issues",
    },
    install_requires=["typing_extensions; python_version < '3.8'", "mypy-boto3==1.10.48.0",],
    extras_require={
        "essential": [
            "mypy-boto3-cloudformation==1.10.48.0",
            "mypy-boto3-dynamodb==1.10.48.0",
            "mypy-boto3-ec2==1.10.48.0",
            "mypy-boto3-lambda==1.10.48.0",
            "mypy-boto3-rds==1.10.48.0",
            "mypy-boto3-s3==1.10.48.0",
            "mypy-boto3-sqs==1.10.48.0",
        ],
        "accessanalyzer": ["mypy-boto3-accessanalyzer==1.10.48.0"],
        "acm": ["mypy-boto3-acm==1.10.48.0"],
        "acm-pca": ["mypy-boto3-acm-pca==1.10.48.0"],
        "alexaforbusiness": ["mypy-boto3-alexaforbusiness==1.10.48.0"],
        "amplify": ["mypy-boto3-amplify==1.10.48.0"],
        "apigateway": ["mypy-boto3-apigateway==1.10.48.0"],
        "apigatewaymanagementapi": ["mypy-boto3-apigatewaymanagementapi==1.10.48.0"],
        "apigatewayv2": ["mypy-boto3-apigatewayv2==1.10.48.0"],
        "appconfig": ["mypy-boto3-appconfig==1.10.48.0"],
        "application-autoscaling": ["mypy-boto3-application-autoscaling==1.10.48.0"],
        "application-insights": ["mypy-boto3-application-insights==1.10.48.0"],
        "appmesh": ["mypy-boto3-appmesh==1.10.48.0"],
        "appstream": ["mypy-boto3-appstream==1.10.48.0"],
        "appsync": ["mypy-boto3-appsync==1.10.48.0"],
        "athena": ["mypy-boto3-athena==1.10.48.0"],
        "autoscaling": ["mypy-boto3-autoscaling==1.10.48.0"],
        "autoscaling-plans": ["mypy-boto3-autoscaling-plans==1.10.48.0"],
        "backup": ["mypy-boto3-backup==1.10.48.0"],
        "batch": ["mypy-boto3-batch==1.10.48.0"],
        "budgets": ["mypy-boto3-budgets==1.10.48.0"],
        "ce": ["mypy-boto3-ce==1.10.48.0"],
        "chime": ["mypy-boto3-chime==1.10.48.0"],
        "cloud9": ["mypy-boto3-cloud9==1.10.48.0"],
        "clouddirectory": ["mypy-boto3-clouddirectory==1.10.48.0"],
        "cloudformation": ["mypy-boto3-cloudformation==1.10.48.0"],
        "cloudfront": ["mypy-boto3-cloudfront==1.10.48.0"],
        "cloudhsm": ["mypy-boto3-cloudhsm==1.10.48.0"],
        "cloudhsmv2": ["mypy-boto3-cloudhsmv2==1.10.48.0"],
        "cloudsearch": ["mypy-boto3-cloudsearch==1.10.48.0"],
        "cloudsearchdomain": ["mypy-boto3-cloudsearchdomain==1.10.48.0"],
        "cloudtrail": ["mypy-boto3-cloudtrail==1.10.48.0"],
        "cloudwatch": ["mypy-boto3-cloudwatch==1.10.48.0"],
        "codebuild": ["mypy-boto3-codebuild==1.10.48.0"],
        "codecommit": ["mypy-boto3-codecommit==1.10.48.0"],
        "codedeploy": ["mypy-boto3-codedeploy==1.10.48.0"],
        "codeguru-reviewer": ["mypy-boto3-codeguru-reviewer==1.10.48.0"],
        "codeguruprofiler": ["mypy-boto3-codeguruprofiler==1.10.48.0"],
        "codepipeline": ["mypy-boto3-codepipeline==1.10.48.0"],
        "codestar": ["mypy-boto3-codestar==1.10.48.0"],
        "codestar-connections": ["mypy-boto3-codestar-connections==1.10.48.0"],
        "codestar-notifications": ["mypy-boto3-codestar-notifications==1.10.48.0"],
        "cognito-identity": ["mypy-boto3-cognito-identity==1.10.48.0"],
        "cognito-idp": ["mypy-boto3-cognito-idp==1.10.48.0"],
        "cognito-sync": ["mypy-boto3-cognito-sync==1.10.48.0"],
        "comprehend": ["mypy-boto3-comprehend==1.10.48.0"],
        "comprehendmedical": ["mypy-boto3-comprehendmedical==1.10.48.0"],
        "compute-optimizer": ["mypy-boto3-compute-optimizer==1.10.48.0"],
        "config": ["mypy-boto3-config==1.10.48.0"],
        "connect": ["mypy-boto3-connect==1.10.48.0"],
        "connectparticipant": ["mypy-boto3-connectparticipant==1.10.48.0"],
        "cur": ["mypy-boto3-cur==1.10.48.0"],
        "dataexchange": ["mypy-boto3-dataexchange==1.10.48.0"],
        "datapipeline": ["mypy-boto3-datapipeline==1.10.48.0"],
        "datasync": ["mypy-boto3-datasync==1.10.48.0"],
        "dax": ["mypy-boto3-dax==1.10.48.0"],
        "detective": ["mypy-boto3-detective==1.10.48.0"],
        "devicefarm": ["mypy-boto3-devicefarm==1.10.48.0"],
        "directconnect": ["mypy-boto3-directconnect==1.10.48.0"],
        "discovery": ["mypy-boto3-discovery==1.10.48.0"],
        "dlm": ["mypy-boto3-dlm==1.10.48.0"],
        "dms": ["mypy-boto3-dms==1.10.48.0"],
        "docdb": ["mypy-boto3-docdb==1.10.48.0"],
        "ds": ["mypy-boto3-ds==1.10.48.0"],
        "dynamodb": ["mypy-boto3-dynamodb==1.10.48.0"],
        "dynamodbstreams": ["mypy-boto3-dynamodbstreams==1.10.48.0"],
        "ebs": ["mypy-boto3-ebs==1.10.48.0"],
        "ec2": ["mypy-boto3-ec2==1.10.48.0"],
        "ec2-instance-connect": ["mypy-boto3-ec2-instance-connect==1.10.48.0"],
        "ecr": ["mypy-boto3-ecr==1.10.48.0"],
        "ecs": ["mypy-boto3-ecs==1.10.48.0"],
        "efs": ["mypy-boto3-efs==1.10.48.0"],
        "eks": ["mypy-boto3-eks==1.10.48.0"],
        "elastic-inference": ["mypy-boto3-elastic-inference==1.10.48.0"],
        "elasticache": ["mypy-boto3-elasticache==1.10.48.0"],
        "elasticbeanstalk": ["mypy-boto3-elasticbeanstalk==1.10.48.0"],
        "elastictranscoder": ["mypy-boto3-elastictranscoder==1.10.48.0"],
        "elb": ["mypy-boto3-elb==1.10.48.0"],
        "elbv2": ["mypy-boto3-elbv2==1.10.48.0"],
        "emr": ["mypy-boto3-emr==1.10.48.0"],
        "es": ["mypy-boto3-es==1.10.48.0"],
        "events": ["mypy-boto3-events==1.10.48.0"],
        "firehose": ["mypy-boto3-firehose==1.10.48.0"],
        "fms": ["mypy-boto3-fms==1.10.48.0"],
        "forecast": ["mypy-boto3-forecast==1.10.48.0"],
        "forecastquery": ["mypy-boto3-forecastquery==1.10.48.0"],
        "frauddetector": ["mypy-boto3-frauddetector==1.10.48.0"],
        "fsx": ["mypy-boto3-fsx==1.10.48.0"],
        "gamelift": ["mypy-boto3-gamelift==1.10.48.0"],
        "glacier": ["mypy-boto3-glacier==1.10.48.0"],
        "globalaccelerator": ["mypy-boto3-globalaccelerator==1.10.48.0"],
        "glue": ["mypy-boto3-glue==1.10.48.0"],
        "greengrass": ["mypy-boto3-greengrass==1.10.48.0"],
        "groundstation": ["mypy-boto3-groundstation==1.10.48.0"],
        "guardduty": ["mypy-boto3-guardduty==1.10.48.0"],
        "health": ["mypy-boto3-health==1.10.48.0"],
        "iam": ["mypy-boto3-iam==1.10.48.0"],
        "imagebuilder": ["mypy-boto3-imagebuilder==1.10.48.0"],
        "importexport": ["mypy-boto3-importexport==1.10.48.0"],
        "inspector": ["mypy-boto3-inspector==1.10.48.0"],
        "iot": ["mypy-boto3-iot==1.10.48.0"],
        "iot-data": ["mypy-boto3-iot-data==1.10.48.0"],
        "iot-jobs-data": ["mypy-boto3-iot-jobs-data==1.10.48.0"],
        "iot1click-devices": ["mypy-boto3-iot1click-devices==1.10.48.0"],
        "iot1click-projects": ["mypy-boto3-iot1click-projects==1.10.48.0"],
        "iotanalytics": ["mypy-boto3-iotanalytics==1.10.48.0"],
        "iotevents": ["mypy-boto3-iotevents==1.10.48.0"],
        "iotevents-data": ["mypy-boto3-iotevents-data==1.10.48.0"],
        "iotsecuretunneling": ["mypy-boto3-iotsecuretunneling==1.10.48.0"],
        "iotthingsgraph": ["mypy-boto3-iotthingsgraph==1.10.48.0"],
        "kafka": ["mypy-boto3-kafka==1.10.48.0"],
        "kendra": ["mypy-boto3-kendra==1.10.48.0"],
        "kinesis": ["mypy-boto3-kinesis==1.10.48.0"],
        "kinesis-video-archived-media": ["mypy-boto3-kinesis-video-archived-media==1.10.48.0"],
        "kinesis-video-media": ["mypy-boto3-kinesis-video-media==1.10.48.0"],
        "kinesis-video-signaling": ["mypy-boto3-kinesis-video-signaling==1.10.48.0"],
        "kinesisanalytics": ["mypy-boto3-kinesisanalytics==1.10.48.0"],
        "kinesisanalyticsv2": ["mypy-boto3-kinesisanalyticsv2==1.10.48.0"],
        "kinesisvideo": ["mypy-boto3-kinesisvideo==1.10.48.0"],
        "kms": ["mypy-boto3-kms==1.10.48.0"],
        "lakeformation": ["mypy-boto3-lakeformation==1.10.48.0"],
        "lambda": ["mypy-boto3-lambda==1.10.48.0"],
        "lex-models": ["mypy-boto3-lex-models==1.10.48.0"],
        "lex-runtime": ["mypy-boto3-lex-runtime==1.10.48.0"],
        "license-manager": ["mypy-boto3-license-manager==1.10.48.0"],
        "lightsail": ["mypy-boto3-lightsail==1.10.48.0"],
        "logs": ["mypy-boto3-logs==1.10.48.0"],
        "machinelearning": ["mypy-boto3-machinelearning==1.10.48.0"],
        "macie": ["mypy-boto3-macie==1.10.48.0"],
        "managedblockchain": ["mypy-boto3-managedblockchain==1.10.48.0"],
        "marketplace-catalog": ["mypy-boto3-marketplace-catalog==1.10.48.0"],
        "marketplace-entitlement": ["mypy-boto3-marketplace-entitlement==1.10.48.0"],
        "marketplacecommerceanalytics": ["mypy-boto3-marketplacecommerceanalytics==1.10.48.0"],
        "mediaconnect": ["mypy-boto3-mediaconnect==1.10.48.0"],
        "mediaconvert": ["mypy-boto3-mediaconvert==1.10.48.0"],
        "medialive": ["mypy-boto3-medialive==1.10.48.0"],
        "mediapackage": ["mypy-boto3-mediapackage==1.10.48.0"],
        "mediapackage-vod": ["mypy-boto3-mediapackage-vod==1.10.48.0"],
        "mediastore": ["mypy-boto3-mediastore==1.10.48.0"],
        "mediastore-data": ["mypy-boto3-mediastore-data==1.10.48.0"],
        "mediatailor": ["mypy-boto3-mediatailor==1.10.48.0"],
        "meteringmarketplace": ["mypy-boto3-meteringmarketplace==1.10.48.0"],
        "mgh": ["mypy-boto3-mgh==1.10.48.0"],
        "migrationhub-config": ["mypy-boto3-migrationhub-config==1.10.48.0"],
        "mobile": ["mypy-boto3-mobile==1.10.48.0"],
        "mq": ["mypy-boto3-mq==1.10.48.0"],
        "mturk": ["mypy-boto3-mturk==1.10.48.0"],
        "neptune": ["mypy-boto3-neptune==1.10.48.0"],
        "networkmanager": ["mypy-boto3-networkmanager==1.10.48.0"],
        "opsworks": ["mypy-boto3-opsworks==1.10.48.0"],
        "opsworkscm": ["mypy-boto3-opsworkscm==1.10.48.0"],
        "organizations": ["mypy-boto3-organizations==1.10.48.0"],
        "outposts": ["mypy-boto3-outposts==1.10.48.0"],
        "personalize": ["mypy-boto3-personalize==1.10.48.0"],
        "personalize-events": ["mypy-boto3-personalize-events==1.10.48.0"],
        "personalize-runtime": ["mypy-boto3-personalize-runtime==1.10.48.0"],
        "pi": ["mypy-boto3-pi==1.10.48.0"],
        "pinpoint": ["mypy-boto3-pinpoint==1.10.48.0"],
        "pinpoint-email": ["mypy-boto3-pinpoint-email==1.10.48.0"],
        "pinpoint-sms-voice": ["mypy-boto3-pinpoint-sms-voice==1.10.48.0"],
        "polly": ["mypy-boto3-polly==1.10.48.0"],
        "pricing": ["mypy-boto3-pricing==1.10.48.0"],
        "qldb": ["mypy-boto3-qldb==1.10.48.0"],
        "qldb-session": ["mypy-boto3-qldb-session==1.10.48.0"],
        "quicksight": ["mypy-boto3-quicksight==1.10.48.0"],
        "ram": ["mypy-boto3-ram==1.10.48.0"],
        "rds": ["mypy-boto3-rds==1.10.48.0"],
        "rds-data": ["mypy-boto3-rds-data==1.10.48.0"],
        "redshift": ["mypy-boto3-redshift==1.10.48.0"],
        "rekognition": ["mypy-boto3-rekognition==1.10.48.0"],
        "resource-groups": ["mypy-boto3-resource-groups==1.10.48.0"],
        "resourcegroupstaggingapi": ["mypy-boto3-resourcegroupstaggingapi==1.10.48.0"],
        "robomaker": ["mypy-boto3-robomaker==1.10.48.0"],
        "route53": ["mypy-boto3-route53==1.10.48.0"],
        "route53domains": ["mypy-boto3-route53domains==1.10.48.0"],
        "route53resolver": ["mypy-boto3-route53resolver==1.10.48.0"],
        "s3": ["mypy-boto3-s3==1.10.48.0"],
        "s3control": ["mypy-boto3-s3control==1.10.48.0"],
        "sagemaker": ["mypy-boto3-sagemaker==1.10.48.0"],
        "sagemaker-a2i-runtime": ["mypy-boto3-sagemaker-a2i-runtime==1.10.48.0"],
        "sagemaker-runtime": ["mypy-boto3-sagemaker-runtime==1.10.48.0"],
        "savingsplans": ["mypy-boto3-savingsplans==1.10.48.0"],
        "schemas": ["mypy-boto3-schemas==1.10.48.0"],
        "sdb": ["mypy-boto3-sdb==1.10.48.0"],
        "secretsmanager": ["mypy-boto3-secretsmanager==1.10.48.0"],
        "securityhub": ["mypy-boto3-securityhub==1.10.48.0"],
        "serverlessrepo": ["mypy-boto3-serverlessrepo==1.10.48.0"],
        "service-quotas": ["mypy-boto3-service-quotas==1.10.48.0"],
        "servicecatalog": ["mypy-boto3-servicecatalog==1.10.48.0"],
        "servicediscovery": ["mypy-boto3-servicediscovery==1.10.48.0"],
        "ses": ["mypy-boto3-ses==1.10.48.0"],
        "sesv2": ["mypy-boto3-sesv2==1.10.48.0"],
        "shield": ["mypy-boto3-shield==1.10.48.0"],
        "signer": ["mypy-boto3-signer==1.10.48.0"],
        "sms": ["mypy-boto3-sms==1.10.48.0"],
        "sms-voice": ["mypy-boto3-sms-voice==1.10.48.0"],
        "snowball": ["mypy-boto3-snowball==1.10.48.0"],
        "sns": ["mypy-boto3-sns==1.10.48.0"],
        "sqs": ["mypy-boto3-sqs==1.10.48.0"],
        "ssm": ["mypy-boto3-ssm==1.10.48.0"],
        "sso": ["mypy-boto3-sso==1.10.48.0"],
        "sso-oidc": ["mypy-boto3-sso-oidc==1.10.48.0"],
        "stepfunctions": ["mypy-boto3-stepfunctions==1.10.48.0"],
        "storagegateway": ["mypy-boto3-storagegateway==1.10.48.0"],
        "sts": ["mypy-boto3-sts==1.10.48.0"],
        "support": ["mypy-boto3-support==1.10.48.0"],
        "swf": ["mypy-boto3-swf==1.10.48.0"],
        "textract": ["mypy-boto3-textract==1.10.48.0"],
        "transcribe": ["mypy-boto3-transcribe==1.10.48.0"],
        "transfer": ["mypy-boto3-transfer==1.10.48.0"],
        "translate": ["mypy-boto3-translate==1.10.48.0"],
        "waf": ["mypy-boto3-waf==1.10.48.0"],
        "waf-regional": ["mypy-boto3-waf-regional==1.10.48.0"],
        "wafv2": ["mypy-boto3-wafv2==1.10.48.0"],
        "workdocs": ["mypy-boto3-workdocs==1.10.48.0"],
        "worklink": ["mypy-boto3-worklink==1.10.48.0"],
        "workmail": ["mypy-boto3-workmail==1.10.48.0"],
        "workmailmessageflow": ["mypy-boto3-workmailmessageflow==1.10.48.0"],
        "workspaces": ["mypy-boto3-workspaces==1.10.48.0"],
        "xray": ["mypy-boto3-xray==1.10.48.0"],
    },
    zip_safe=False,
)
