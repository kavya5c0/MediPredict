def handler(request):
    return {
        "statusCode": 200,
        "body": '{"message": "MediPredict API", "status": "working"}',
        "headers": {
            "Content-Type": "application/json"
        }
    }