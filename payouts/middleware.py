import json
from django.http import JsonResponse
from .models_idempotency import IdempotencyKey


class IdempotencyKeyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != "POST":
            return self.get_response(request)

        key = request.headers.get("Idempotency-Key")
        if not key:
            return self.get_response(request)

        record = IdempotencyKey.objects.filter(key=key).first()
        if record:
            return JsonResponse(
                record.response_body,
                status=record.response_status,
            )

        response = self.get_response(request)

        if response.status_code in (200, 201):
            IdempotencyKey.objects.create(
                key=key,
                response_status=response.status_code,
                response_body=json.loads(response.content),
            )

        return response
