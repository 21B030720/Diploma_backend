import logging

from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.paybox.models import Card
from apps.paybox.serializers import CardSerializer, InitPaymentSerializer, SavedCardPaymentSerializer
from apps.paybox.services import start_init_payment, process_response, save_user_card, pay_with_saved_card
from apps.users.permissions import IsClientUser
from apps.utils.enums import TransactionStatus
from apps.utils.serializers import EmptySerializer, MessageSerializer
from apps.utils.views import BaseViewSet
from apps.paybox.tasks import delete_user_card_task


# Create your views here.
class CardViewSet(BaseViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Card.objects.order_by('id')
    serializer_class = CardSerializer
    serializers = {
        'destroy': EmptySerializer,
        'pay_with_saved_card': SavedCardPaymentSerializer
    }
    permission_classes = [IsClientUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(user=user)
        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted'])
        delete_user_card_task.apply_async(args=[self.request.user.id, instance.id])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_decorator(name='card_save',
                      decorator=swagger_auto_schema(
                          tags=['paybox'],
                          request_body=EmptySerializer(),
                          responses={
                              200: MessageSerializer()
                          }
                      ))
    @action(methods=['POST'], detail=False, url_path='save')
    def card_save(self, request):
        message, status_code = save_user_card(request.user)

        if status_code == 400:
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_code = status.HTTP_200_OK
        return Response({'message': message}, status=status_code)

    @method_decorator(name='pay_with_saved_card',
                      decorator=swagger_auto_schema(
                          tags=['paybox'],
                          responses={
                              200: MessageSerializer()
                          }
                      ))
    @action(methods=['POST'], detail=False, url_path='pay-with-saved-card')
    def pay_with_saved_card(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction_id = serializer.validated_data['transaction_id']
        card_id = serializer.validated_data['card_id']
        message = pay_with_saved_card(card_id, transaction_id)
        data = {
            'message': message
        }
        serializer = MessageSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(name='all',
                      decorator=swagger_auto_schema(
                          tags=['paybox'],
                          responses={
                              200: CardSerializer(many=True),
                          })
                      )
    @action(methods=['GET'], detail=False)
    def all(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(name='make_default',
                      decorator=swagger_auto_schema(
                          tags=['paybox'],
                          request_body=EmptySerializer(),
                          responses={
                              201: EmptySerializer(),
                          }
                      ))
    @action(methods=['PUT'], detail=True, url_path='make-default')
    def make_default(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        card = self.get_object()
        queryset.filter(default=True).update(default=False)
        card.default = True
        card.save(update_fields=['default'])
        return Response(status=status.HTTP_201_CREATED)


class InitPaymentAPI(APIView):
    permission_classes = (IsClientUser,)

    @swagger_auto_schema(tags=['paybox'],
                         request_body=InitPaymentSerializer,
                         responses={
                             200: MessageSerializer()
                         })
    def post(self, request):
        serializer = InitPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction_id = serializer.validated_data.get('transaction_id')
        message, status_code = start_init_payment(transaction_id)

        if status_code == 400:
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_code = status.HTTP_200_OK
        return Response({'message': message}, status=status_code)


class CardSaveResultAPI(APIView):

    def get(self, request):
        return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)

    def post(self, request):
        response = request.data
        pg_xml = response.get('pg_xml')
        if not pg_xml:
            logging.warning(f"Missing pg_xml field in request: {request}")
            raise ValidationError('Could not find pg_xml field')

        try:
            root = ET.fromstring(pg_xml)
            card_token = root.findtext('pg_card_token')
            user_id = root.findtext('pg_user_id')
            data = {
                'card_hash': root.findtext('pg_card_hash'),
                'card_month': root.findtext('pg_card_month'),
                'card_year': root.findtext('pg_card_year'),
                'bank': root.findtext('pg_bank'),
                'country': root.findtext('pg_country'),
                'card_3ds': root.findtext('pg_card_3ds'),
                'card_id': root.findtext('pg_card_id'),
                'card_token': card_token,
                'user_id': user_id,
                'status': root.findtext('pg_status'),
            }
            existing_card = Card.objects.filter(card_token=card_token, user_id=user_id).first()
            if existing_card:
                if existing_card.is_deleted:
                    existing_card.is_deleted = False
                    existing_card.save(update_fields=['is_deleted'])
            else:
                card = Card.objects.create(**data)
                logging.info(f"Card saved successfully: {card}")
            return Response({'message': 'OK'})
        except ET.ParseError:
            logging.exception(f"Parse error in CardSaveResultAPI: {request}")
        except Exception as e:
            logging.error(f"Unhandled exception in CardSaveResultAPI: {request}", exc_info=True)

        raise ValidationError("FAILURE", code=500)


class PaymentResultAPI(APIView):

    def post(self, request):
        response = request.data
        response = response.urlencode()
        process_response(response)
        return Response({'message': 'OK'})


class PaymentResultSuccessAPI(APIView):

    def post(self, request):
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def get(self, request):
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class PaymentResultFailureAPI(APIView):

    def post(self, request):
        return Response({'message': 'FAIL'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({'message': 'FAIL'}, status=status.HTTP_400_BAD_REQUEST)
