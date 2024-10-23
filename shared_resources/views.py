import base64
import pandas as pd
from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Country
from .serializers import CountrySerializer


class CountryAPIView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        # Get the Base64-encoded file data
        base64_file = request.data.get("file")
        if not base64_file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Decode the Base64 string
        try:
            # The Base64 string may contain a prefix like "data:file/xlsx;base64,"; strip that off
            if base64_file.startswith("data:"):
                base64_file = base64_file.split(",")[1]
            file_data = base64.b64decode(base64_file)
            excel_file = BytesIO(file_data)
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Collect errors
        errors = []

        for _, row in df.iterrows():
            country_data = {
                "name": row["Country Name"],
                "iso_code": row["ISO Code"],
                "currecny": row["Currency"],
                "phone_code": row["Phone Code"],
                "capital": row["Capital"],
                "region": row["Region"],
            }

            serializer = CountrySerializer(data=country_data)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Countries added successfully"}, status=status.HTTP_201_CREATED
        )




class CountryByRegionAPIView(APIView):
    def get(self, request, region):
        countries = Country.objects.filter(region=region)
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DistinctRegionAPIView(APIView):
    def get(self, request):
        regions = Country.objects.values_list("region", flat=True).distinct()
        return Response(list(regions), status=status.HTTP_200_OK)
