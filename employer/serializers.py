# serializers.py

import os
import base64
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework import serializers
from .models import (
    EmployerProfile,
    EmployerContacts,
    EmployerHRContacts,
    EmployerDocuments,
)


class EmployerContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerContacts
        exclude = ["employer_id"]


class EmployerHRContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerHRContacts
        exclude = ["employer_id"]


class EmployerDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerDocuments
        fields = "__all__"

    def create(self, validated_data):
        return EmployerDocuments.objects.create(**validated_data)


class EmployerProfileSerializer(serializers.ModelSerializer):
    contacts = EmployerContactsSerializer(many=True, required=False)
    hr_contacts = EmployerHRContactsSerializer(many=True, required=False)
    documents = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = EmployerProfile
        fields = "__all__"

    def create(self, validated_data):
        contacts_data = validated_data.pop("contacts", [])
        hr_contacts_data = validated_data.pop("hr_contacts", [])
        documents_data = validated_data.pop("documents", [])

        profile = EmployerProfile.objects.create(**validated_data)

        for contact_data in contacts_data:
            contact_data["employer_id"] = profile
            EmployerContacts.objects.create(**contact_data)

        for hr_contact_data in hr_contacts_data:
            hr_contact_data["employer_id"] = profile
            EmployerHRContacts.objects.create(**hr_contact_data)

        # Save documents separately
        self.save_documents(documents_data, profile)

        return profile

    def save_documents(self, documents_data, profile):
        for document_data in documents_data:
            for field in [
                "incorporation_document",
                "business_license",
                "insurance_document",
            ]:
                if field in document_data:
                    if (
                        isinstance(document_data[field], str)
                        and ";base64," in document_data[field]
                    ):
                        try:
                            format, imgstr = document_data[field].split(";base64,")
                            missing_padding = len(imgstr) % 4
                            if missing_padding:
                                imgstr += "=" * (4 - missing_padding)

                            # Validate if the string is a valid base64
                            if not all(
                                c
                                in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
                                for c in imgstr
                            ):
                                raise ValueError("Invalid base64 string")

                            ext = format.split("/")[-1]
                            file_name = f"{field}_{profile.employer_id}.{ext}"
                            file_path = os.path.join(
                                settings.MEDIA_ROOT, "EmployerDocuments", file_name
                            )

                            # Create directory if it doesn't exist
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)

                            # Save the file
                            with open(file_path, "wb") as f:
                                f.write(base64.b64decode(imgstr))

                            # Store the relative file path in the database
                            document_data[field] = f"EmployerDocuments/{file_name}"

                        except Exception as e:
                            raise serializers.ValidationError(
                                {field: f"Error processing {field}: {str(e)}"}
                            )
                    else:
                        raise serializers.ValidationError(
                            {field: "Invalid data format. Expected base64 format."}
                        )

            document_data["employer_id"] = profile
            EmployerDocuments.objects.create(**document_data)


class GetEmployerProfileSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()
    hr_contacts = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    class Meta:
        model = EmployerProfile
        fields = [
            "employer_id",
            "user_id",
            "company_name",
            "company_description",
            "website",
            "business_registration_number",
            "tax_identification_number",
            "industry",
            "size",
            "country_id",
            "headquarter_address",
            "created_at",
            "updated_at",
            "contacts",
            "hr_contacts",
            "documents",
        ]

    def get_contacts(self, obj):
        contacts = EmployerContacts.objects.filter(employer_id=obj)
        return EmployerContactsSerializer(contacts, many=True).data

    def get_hr_contacts(self, obj):
        hr_contacts = EmployerHRContacts.objects.filter(employer_id=obj)
        return EmployerHRContactsSerializer(hr_contacts, many=True).data

    def get_documents(self, obj):
        documents = EmployerDocuments.objects.filter(employer_id=obj)
        return EmployerDocumentsSerializer(documents, many=True).data
