from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from api.serializers import PaymentSerializer
from payments.models import *


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def payment_list(request, company_id):
    if request.method == 'GET':
        payments = Payment.objects.filter(company__id=company_id).all()

        title = request.query_params.get('title', None)
        if title is not None:
            payments = payments.filter(title__icontains=title)

        serializer = PaymentSerializer(payments, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        payment_data = JSONParser().parse(request)
        serializer = PaymentSerializer(data=payment_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Payment.objects.all().delete()
        return JsonResponse(
            {
                'message': '{count} Tutorials were deleted successfully!'.format(count=count[0])
            },
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET', 'PUT', 'DELETE'])
def payment_detail(request, company_id, payment_id):
    try:
        payment = Payment.objects.get(company__pk=company_id, pk=payment_id)
    except Payment.DoesNotExist:
        return JsonResponse(
            {'message': 'The Payment ({payment_id}) does not exist'.format(payment_id=payment_id)},
            status=status.HTTP_404_NOT_FOUND
        )

    # return payment information
    if request.method == 'GET':
        serializer = PaymentSerializer(payment)
        return JsonResponse(serializer.data)

    # Save/Update Payment
    elif request.method == 'PUT':
        payment_data = JSONParser().parse(request)
        serializer = PaymentSerializer(payment, data=payment_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete Payment
    elif request.method == 'DELETE':
        payment.delete()
        return JsonResponse(
            {
                'message': 'Payment ({payment_id}) was deleted successfully!'.format(payment_id=payment_id)
            },
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET', 'PUT'])
def subscription(request, company_id):
    try:
        company = Company.objects.get(pk=company_id, is_active=True)
    except Company.DoesNotExist:
        return JsonResponse({'message': 'The Company does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Subscribe/unsubscribe
    if request.method == 'PUT':
        company.is_email_subscribed = not company.is_email_subscribed
        company.save()
    return JsonResponse({'Subscribed': company.is_email_subscribed})


@api_view(['POST', 'PUT'])
def email(request, company_id):
    try:
        company = Company.objects.get(pk=company_id, is_active=True)
    except Company.DoesNotExist:
        return JsonResponse({'message': 'The Company does not exist'}, status=status.HTTP_404_NOT_FOUND)
    print(u'Sender called!! ;)')
    return JsonResponse({'sent_to': company.name}, safe=False)


@api_view(['GET'])
def email_list(request):
    companies = Company.objects.filter(is_active=True).all()
    # TODO call the sender queue or API
    print(u'Sender called!! ;)')
    return JsonResponse({'sent_to': ', '.join([company.name for company in companies])}, safe=False)
