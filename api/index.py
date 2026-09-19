# Standard Vercel serverless function
def handler(request):
    return {
        "body": "Hello from Vercel Python!",
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain"
        }
    }