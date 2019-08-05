import boto3
import StringIO
import zipfile
import mimetypes
from datetime import datetime

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:eu-north-1:539076042504:deployPortfolioTopic')

    try:
        s3 = boto3.resource('s3')

        portfolio_bucket = s3.Bucket('portfolio.whata.guru')
        build_bucket = s3.Bucket('portfoliobuild.whata.guru')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
             for nm in myzip.namelist():
                     obj = myzip.open(nm)
                     portfolio_bucket.upload_fileobj(obj, nm,
                       ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})

        print "Job done!"
        now = datetime.now()
        topic.publish(Subject="Portfolio deployed", Message="Portofolio deployed (%s)" % now)
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="Not deployed successfully")
        raise



    return 'Hello from lambda'
