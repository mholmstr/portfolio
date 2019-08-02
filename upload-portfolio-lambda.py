import boto3
import StringIO
import zipfile
import datetime

def lambda_handler(event, context):

    s3 = boto3.resource('s3')

    portfolio_bucket = s3.Bucket('portfolio.whata.guru')
    build_bucket = s3.Bucket('portfoliobuild.whata.guru')

    portfolio_zip = StringIO.StringIO()
    build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

    with zipfile.ZipFile(portfolio_zip) as myzip:
         for nm in myzip.namelist():
                 obj = myzip.open(nm)
                 portfolio_bucket.upload_fileobj(obj, nm)


    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:eu-north-1:539076042504:deployPortfolioTopic')
    now = datetime.now()

    topic.publish(Subject="Portfolio deployed", Message="Portofolio deployed (%s)" % now)

    return 'Hello from lambda'
