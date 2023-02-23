
from rest_framework.parsers import JSONParser
from rest_framework import generics, filters
from django.http.response import JsonResponse

from django.http import HttpResponse, Http404

from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.db.models import Sum
import os

from FoodbankApp.models import Donor, Collection, Wholesale, Participation
from FoodbankApp.serializers import DonorSerializer, CollectionSerializer, WholesaleSerializer, ParticipationSerializer, ParticipationListSerializer

from django.core.files.storage import default_storage

# Create your views here.

class donorApiFliter(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    def get(self, request):

        donors = Donor.objects.all().order_by('FirstName')
        page = self.request.query_params.get('page')
        type = self.request.query_params.get('type')
        fullname = self.request.query_params.get('fullname')
        donId = self.request.query_params.get('donid')

        total3Month = len(donors.exclude(DonorType__icontains="0"))
        totalMonthly = len(donors.filter(DonorType__icontains="1"))
        totalOther = len(donors.filter(DonorType__icontains="0"))

        if page == "all":

            if type is not None:
                if type == "3":
                    donors = donors.exclude(DonorType__icontains="0")
                else:
                    donors = donors.filter(DonorType__icontains=type)

            if fullname is not None:
                donors = donors.filter(FullName__icontains=fullname)

            serializedDonors = DonorSerializer(donors, many=True)

            payload = {
                "data": serializedDonors.data
            }

            return JsonResponse(serializedDonors.data, safe=False)

        else:

            page = int(self.request.query_params.get('page'))

            if type is not None:
                if type == "3":
                    donors = donors.exclude(DonorType__icontains="0")
                else:
                    donors = donors.filter(DonorType__icontains=type)

            if fullname is not None:
                donors = donors.filter(FullName__icontains=fullname)

            elif donId is not None:
                donors = donors.filter(DonorID=donId)

            paginatorPre = Paginator(donors, per_page=25)
            donorsPaginated = paginatorPre.get_page(page)

            serializedDonors = DonorSerializer(donorsPaginated, many=True)

            payload = {
                "page": {
                    "current": donorsPaginated.number,
                    "has_next":donorsPaginated.has_next(),
                    "has_previous": donorsPaginated.has_previous(),
                    "total_number": paginatorPre.num_pages,
                    "TotalContacts": len(donors),
                    "3Month": total3Month,
                    "Monthly": totalMonthly,
                    "Other": totalOther
                },
                "data": serializedDonors.data
            }

            return JsonResponse(payload, safe=False)

class DonorApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        donors = Donor.objects.all().order_by('FirstName')
        donor_serializer = DonorSerializer(donors, many=True)
        return JsonResponse(donor_serializer.data, safe=False)

    def post(self, request):
        donor_data=JSONParser().parse(request)
        email = donor_data['Email']
        fullname = donor_data['FullName']
        try:
            donor = Donor.objects.get(Email=email)
            donor_serializer = DonorSerializer(donor)
            response = "{} already exists as a contact!".format(fullname)
            return JsonResponse(response, safe=False)
        except Donor.DoesNotExist:
            donor_serializer = DonorSerializer(data=donor_data)
            if donor_serializer.is_valid():
                donor_serializer.save()
                response = "{} has been added successfully as a contact!".format(fullname)
                return JsonResponse(response , safe=False)
            return JsonResponse("Failed to add new contact!",safe=False)

    def put(self, request):
        donor_data = JSONParser().parse(request)
        fullname = donor_data['FullName']
        donor = Donor.objects.get(DonorID=donor_data['DonorID'])
        donor_serializer = DonorSerializer(donor,data=donor_data)
        if donor_serializer.is_valid():
            donor_serializer.save()
            response = "{} has been updated successfully!".format(fullname)
            return JsonResponse(response, safe=False)
        return JsonResponse("Failed to update contact", safe=False)

    def delete(self, request, id=0):
        donor=Donor.objects.get(DonorID=id)
        donor.delete()
        return JsonResponse("Contact deleted successfully!", safe=False)

class collectionApiFliter(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    def get(self, request):
        collection = Collection.objects.all().order_by('-CollectionDate')
        startDate = self.request.query_params.get('startdate')
        endDate = self.request.query_params.get('enddate')
        type = self.request.query_params.get('type')
        status = self.request.query_params.get('status')
        page = self.request.query_params.get('page')

        if page == "all":

            if startDate is not None and endDate is None:
                collection = collection.filter(CollectionDate=startDate)
                serializedCollections = CollectionSerializer(collection, many=True)

                return JsonResponse(serializedCollections.data, safe=False)

            serializedCollections = CollectionSerializer(collection, many=True)
            totalWeight = collection.aggregate(Sum('TotalWeight'))
            totalCost = collection.aggregate(Sum('TotalCost'))
            payload = {
                    "page": {
                        "current": None,
                        "has_next": False,
                        "has_previous": False,
                        "total_number": None,
                        "TotalCollections": len(collection),
                        "TotalWeight": ("%.0f" % totalWeight['TotalWeight__sum']),
                        "TotalCost": ("%.0f" % totalCost['TotalCost__sum']),
                    },
                    "data": serializedCollections.data
                }
            return JsonResponse(payload, safe=False)

        page = int(page)

        if status is not None:
            if status == "ARCHIVED":
                collection = collection.filter(CollectionStatus="ARCHIVED")

                if startDate is not None and endDate is not None:
                    collection = collection.filter(CollectionDate__range=[startDate, endDate])

                elif startDate is not None and endDate is None:
                    collection = collection.filter(CollectionDate=startDate)

                if type is not None:
                    collection = collection.filter(Type=type)

                totalWeight = collection.aggregate(Sum('TotalWeight'))
                totalCost = collection.aggregate(Sum('TotalCost'))
                paginatorPre = Paginator(collection, per_page=10)
                collectionsPaginated = paginatorPre.get_page(page)

                serializedCollections = CollectionSerializer(collectionsPaginated, many=True)

                payload = {
                    "page": {
                        "current": collectionsPaginated.number,
                        "has_next":collectionsPaginated.has_next(),
                        "has_previous": collectionsPaginated.has_previous(),
                        "total_number": paginatorPre.num_pages,
                        "TotalCollections": len(collection),
                        "TotalWeight": ("%.0f" % totalWeight['TotalWeight__sum']),
                        "TotalCost": ("%.0f" % totalCost['TotalCost__sum']),
                    },
                    "data": serializedCollections.data
                }

                return JsonResponse(payload, safe=False)

            elif status == "PLANNED,ACTIVE":
                collection = collection.exclude(CollectionStatus="ARCHIVED")

                if startDate is not None and endDate is not None:
                    collection = collection.filter(CollectionDate__range=[startDate, endDate])

                elif startDate is not None and endDate is None:
                    collection = collection.filter(CollectionDate=startDate)

                if type is not None:
                    collection = collection.filter(Type=type)

                totalWeight = collection.aggregate(Sum('TotalWeight'))
                totalCost = collection.aggregate(Sum('TotalCost'))
                paginatorPre = Paginator(collection, per_page=10)
                collectionsPaginated = paginatorPre.get_page(page)

                serializedCollections = CollectionSerializer(collectionsPaginated, many=True)

                payload = {
                    "page": {
                        "current": collectionsPaginated.number,
                        "has_next":collectionsPaginated.has_next(),
                        "has_previous": collectionsPaginated.has_previous(),
                        "total_number": paginatorPre.num_pages,
                        "TotalCollections": len(collection),
                        "TotalWeight": ("%.0f" % totalWeight['TotalWeight__sum']),
                        "TotalCost": ("%.0f" % totalCost['TotalCost__sum']),
                    },
                    "data": serializedCollections.data
                }

                return JsonResponse(payload, safe=False)

        else:
            if startDate is not None and endDate is not None:
                collection = collection.filter(CollectionDate__range=[startDate, endDate])

            elif startDate is not None and endDate is None:
                collection = collection.filter(CollectionDate=startDate)

            if type is not None:
                collection = collection.filter(Type=type)

            totalWeight = collection.aggregate(Sum('TotalWeight'))
            totalCost = collection.aggregate(Sum('TotalCost'))
            paginatorPre = Paginator(collection, per_page=10)
            collectionsPaginated = paginatorPre.get_page(page)

            serializedCollections = CollectionSerializer(collectionsPaginated, many=True)

            payload = {
                "page": {
                    "current": collectionsPaginated.number,
                    "has_next":collectionsPaginated.has_next(),
                    "has_previous": collectionsPaginated.has_previous(),
                    "total_number": paginatorPre.num_pages,
                    "TotalCollections": len(collection),
                    "TotalWeight": ("%.0f" % totalWeight['TotalWeight__sum']),
                    "TotalCost": ("%.0f" % totalCost['TotalCost__sum']),
                },
                "data": serializedCollections.data
            }

            return JsonResponse(payload, safe=False)


class collectionApiStatus(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Collection.objects.all().order_by('-CollectionDate')
    serializer_class = CollectionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["CollectionStatus"]

    def get_queryset(self):
        collection = Collection.objects.all().order_by('-CollectionDate')
        status = self.request.query_params.get('status')

        if status is not None:
            collection = collection.filter(CollectionStatus=status)

            return collection

class CollectionApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        collections = Collection.objects.all().order_by('-CollectionDate')
        collections_serializer = CollectionSerializer(collections, many=True)
        return JsonResponse(collections_serializer.data, safe=False)

    def post(self, request):
        collection_data=JSONParser().parse(request)
        collections_serializer = CollectionSerializer(data=collection_data)
        if collections_serializer.is_valid():
            collections_serializer.save()
            return JsonResponse("New foodbank collection has been added Successfully!" , safe=False)
        return JsonResponse("Collection creation unsuccessful",safe=False)

    def put(self, request):
        collection_data = JSONParser().parse(request)
        collection = Collection.objects.get(CollectionID=collection_data['CollectionID'])
        collections_serializer = CollectionSerializer(collection,data=collection_data)
        if collections_serializer.is_valid():
            collections_serializer.save()
            return JsonResponse("Collection updated successfully!", safe=False)
        return JsonResponse("Failed to update collection", safe=False)

    def delete(self, request, id=0):
        collection=Collection.objects.get(CollectionID=id)
        collection.delete()
        return JsonResponse("Donor deleted successfully!", safe=False)

class wholesaleApiFliter(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Wholesale.objects.all()
    serializer_class = WholesaleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["CollectionID"]

    def get_queryset(self):
        wholesale = Wholesale.objects.all()
        collId = self.request.query_params.get('collid')

        if collId is not None:
            wholesale = wholesale.filter(CollectionID=collId)

        return wholesale


class WholesaleApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        wholesale = Wholesale.objects.all()
        collId = self.request.query_params.get('collid')
        if collId is not None:
            wholesale = wholesale.filter(CollectionID=collId)
        return wholesale

    def post(self, request):
        wholesale_data=JSONParser().parse(request)
        wholesale_serializer = WholesaleSerializer(data=wholesale_data)
        if wholesale_serializer.is_valid():
            wholesale_serializer.save()
            return JsonResponse("New foodbank wholesale has been added Successfully!" , safe=False)
        return JsonResponse("Wholesale creation unsuccessful",safe=False)

    def put(self, request):
        wholesale_data = JSONParser().parse(request)
        wholesale = Wholesale.objects.get(CollectionID=wholesale_data['CollectionID'])
        wholesale_serializer = WholesaleSerializer(wholesale,data=wholesale_data)
        if wholesale_serializer.is_valid():
            wholesale_serializer.save()
            return JsonResponse("Wholesale updated successfully!", safe=False)
        return JsonResponse("Failed to update wholesale", safe=False)

    def delete(self, request, id=0):
        wholesale=Wholesale.objects.get(WholesaleID=id)
        wholesale.delete()
        return JsonResponse("Wholesale deleted successfully!", safe=False)

class participantApiFliter(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["CollectionID", "DonorID"]

    def get_queryset(self):
        participants = Participation.objects.all()
        collId = self.request.query_params.get('collid')
        donId = self.request.query_params.get('donid')

        if donId is not None:
            participants = participants.filter(DonorID=donId)
            if collId is not None:
                participants = participants.filter(CollectionID=collId)

                return participants

            elif collId is None:

                return participants

        elif donId is None:
            if collId is not None:
                participants = participants.filter(CollectionID=collId)

                return participants

            elif collId is None:
                return participants


class ParticipantAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        participants = Participation.objects.all
        collId = self.request.query_params.get('collid')
        if collId is not None:
            participants = participants.filter(CollectionID=collId)
        return participants

    def post(self, request):
        participant_data=JSONParser().parse(request)
        participant_serializer = ParticipationSerializer(data=participant_data)
        if participant_serializer.is_valid():
            participant_serializer.save()
            return JsonResponse("New collection participant has been added Successfully!" , safe=False)
        return JsonResponse("Collection participant creation unsuccessful",safe=False)

    def put(self, request):
        participant_data = JSONParser().parse(request)
        participant = Participation.objects.get(ParticipationID=participant_data['ParticipationID'])
        participant_serializer = ParticipationSerializer(participant,data=participant_data)
        if participant_serializer.is_valid():
            participant_serializer.save()
            return JsonResponse("Collection participant updated successfully!", safe=False)
        return JsonResponse("Failed to update collection participant", safe=False)

    def delete(self, request, id=0):
        participant=Participation.objects.get(ParticipationID=id)
        participant.delete()
        return JsonResponse("Collection participant deleted successfully!", safe=False)


class ParticipantListApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    def get(self, request):
        type = self.request.query_params.get('type')
        collId = self.request.query_params.get('collid')
        fullname = self.request.query_params.get('fullname')
        page = self.request.query_params.get('page')
        per_page = self.request.query_params.get('per_page')
        parTotalLength = len(Participation.objects.filter(CollectionID=collId))
        
        if page == "coll":
            
            payload = {
                "page": {
                    "parTotalLength": parTotalLength,
                }
            }
            
            return JsonResponse(payload, safe=False)

        if collId is not None:
            if type is not None:
                if type == "1":
                    allParticipants = Participation.objects.filter(CollectionID=collId, DonationType=type).order_by('PaymentRecieved', 'DropOffTime')
                    parLength = len(allParticipants)
                elif type == "2":
                    allParticipants = Participation.objects.filter(CollectionID=collId, DonationType=type)
                    parLength = len(allParticipants)
                elif type == "4":
                    allParticipants = Participation.objects.filter(CollectionID=collId, DonationType=type).order_by('PaymentRecieved', 'DropOffTime')
                    parLength = len(allParticipants)
                else:
                    allParticipants = Participation.objects.filter(CollectionID=collId, DonationType=type)
                    parLength = len(allParticipants)
            else:
                allParticipants = Participation.objects.filter(CollectionID=collId)
                parLength = len(allParticipants)
        else:
            if type is not None:
                if type == "1":
                    allParticipants = Participation.objects.filter(DonationType=type).order_by('PaymentRecieved', 'DropOffTime')
                    parLength = len(allParticipants)
                elif type == "2":
                    allParticipants = Participation.objects.filter(DonationType=type)
                    parLength = len(allParticipants)
                elif type == "4":
                    allParticipants = Participation.objects.filter(DonationType=type).order_by('PaymentRecieved', 'DropOffTime')
                    parLength = len(allParticipants)
                else:
                    allParticipants = Participation.objects.filter(DonationType=type)
                    parLength = len(allParticipants)
            else:
                allParticipants = Participation.objects.all()
                parLength = len(allParticipants)

        if fullname is not None:
            donorsqueryset = list(Donor.objects.filter(FullName__icontains=fullname).values_list('DonorID', flat=True))
            allParticipants = allParticipants.filter(DonorID__in=donorsqueryset)

        paginatorPre = Paginator(allParticipants, per_page=int(per_page)
        participantsPaginated = paginatorPre.get_page(int(page))

        serializedParticipant = ParticipationListSerializer(participantsPaginated, many=True)

        payload = {
            "page": {
                "current": participantsPaginated.number,
                "has_next":participantsPaginated.has_next(),
                "has_previous": participantsPaginated.has_previous(),
                "total_number": paginatorPre.num_pages,
                "parLength": parLength,
                "parTotalLength": parTotalLength,
            },
            "data": serializedParticipant.data
        }

        return JsonResponse(payload, safe=False)

class PhotoAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requestbody = JSONParser().parse(request)
        fileName = requestbody['fileName']
        fileExist = default_storage.exists('photos/'+fileName)

        if fileExist == False:
            file_response="{} does not exist".format(fileName)
            return JsonResponse(file_response, safe=False)

        elif fileExist == True:
            file_response="{} found successfully".format(fileName)
            return JsonResponse(file_response, safe=False)


    def post(self, request):
        file=request.FILES['myFile']
        file_name=default_storage.save('photos/'+file.name,file)
        file_response="{} saved successfully".format(file_name)

        return JsonResponse(file_response, safe=False)

    def delete(self, request):
        requestbody = JSONParser().parse(request)
        fileName = 'photos/'+requestbody['fileName']
        default_storage.delete(fileName)
        file_response="{} deleted successfully".format(fileName)
        return JsonResponse(file_response, safe=False)

class SpreadsheetAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requestbody = JSONParser().parse(request)
        fileName = requestbody['fileName']
        fileExist = default_storage.exists('spreadsheets/'+fileName)

        if fileExist == False:
            file_response="{} does not exist".format(fileName)
            return JsonResponse(file_response, safe=False)

        elif fileExist == True:
            file_response="{} found successfully".format(fileName)
            return JsonResponse(file_response, safe=False)


    def post(self, request):
        file=request.FILES['myFile']
        file_name=default_storage.save('spreadsheets/'+file.name,file)
        file_response="{} saved successfully".format(file_name)

        return JsonResponse(file_response, safe=False)

    def delete(self, request):
        requestbody = JSONParser().parse(request)
        fileName = 'spreadsheets/'+requestbody['fileName']
        default_storage.delete(fileName)
        file_response="{} deleted successfully".format(fileName)
        return JsonResponse(file_response, safe=False)
