import json
import requests 

from datetime import datetime
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from .serializers import PaymentSerializer
# Create your views here.

class ProcessPayment(APIView):

	def get(self, request):

		try:
			if int(request.query_params['amount']) < 0:
				return Response(status= status.HTTP_400_BAD_REQUEST)
			elif int(request.query_params['amount']) > 0 and int(request.query_params['amount']) < 20:
				return self.CheapPaymentGateway(request)
			elif int(request.query_params['amount']) > 20 and int(request.query_params['amount']) < 500:
				try:
					return self.ExpensivePaymentGateway(request)
				except:
					return self.CheapPaymentGateway(request)
			elif int(request.query_params['amount']) > 500:
				count = 0
				return self.PremiumPaymentGateway(request, count)
		except:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def CheckData(self, request):

		data = {}
		if len(request.query_params['credit_card_number']) == 16:
			data['credit_card_number'] = request.query_params['credit_card_number'] 
		else: 
			return Response(status= status.HTTP_400_BAD_REQUEST)

		if len(request.query_params['credit_card_holder']) > 0:
			data['card_holder'] = request.query_params['credit_card_holder']
		else:
			return Response(status= status.HTTP_400_BAD_REQUEST)

		expiration_date = datetime.strptime(request.query_params['credit_card_expiration_date'], "%Y-%m-%d")
		current_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'),('%Y-%m-%d'))
		
		if (expiration_date-current_date).days >= 0:
			data['expiration_date'] = request.query_params['credit_card_expiration_date']
		else:
			return Response(status= status.HTTP_400_BAD_REQUEST)

		if len(request.query_params['credit_card_security_code']) == 3:
			data['security_code'] = request.query_params['credit_card_security_code']
		else:
			return Response(status= status.HTTP_400_BAD_REQUEST)

		data['amount'] = request.query_params['amount']

		return Response(status= status.HTTP_200_OK)


	def PremiumPaymentGateway(self, request, count):
		response = self.CheckData(request)
		
		if response.status_code != 200:
			while count < 2:
				count += 1
				self.PremiumPaymentGateway(request, count)
		
		return response

	def ExpensivePaymentGateway(self, request):
		response = self.CheckData(request)

		return response

	def CheapPaymentGateway(self, request):
		response = self.CheckData(request)
		
		return response




class EstimatePrice(APIView):

	def get(self, request):
		try:

			data = {'date': request.query_params['date']}

			estimate_price_data = json.dumps({"signature_name": "predict","instances":[data]})
			estimate_price_data = str(estimate_price_data).replace("'",'"')
		except:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		try:
			r = requests.post("http://localhost:8501/v1/models/model/versions/1:predict", data=estimate_price_data)

			result = r.json()

			response = {'estimated_price': result['predictions'][0][0]}
		except:
			return Response(status= status.HTTP_400_BAD_REQUEST)
			
		return Response(response,status= status.HTTP_200_OK)
