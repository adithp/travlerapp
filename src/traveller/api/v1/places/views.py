import datetime

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated,AllowAny

from api.v1.places.serializers import PlaceSerializer,PlaceDetailSerializer,CommentsSerializer
from places.models import Place,Comments
from django.db.models import Q
from places.models import Place

from api.v1.places.pagination import StandardResultSetPagination


@permission_classes([AllowAny])
@api_view(["GET"])
def places(request):
    instances = Place.objects.filter(is_deleted=False)
    q = request.GET.get("q")
    if q:
        ids = q.split(",")
        instances = instances.filter(category__in=ids)
    paginator = StandardResultSetPagination()
    paginated_result = paginator.paginate_queryset(instances,request)
    context = {
        "request":request
    }
    serializer = PlaceSerializer(paginated_result,many=True,context=context)
    response_data = {
        "status-code" : 6000,
        "count" : paginator.page.paginator.count,
        "links" : {
            "next" : paginator.get_next_link(),
            "previous" : paginator.get_previous_link()
        },
        "data" : serializer.data
    }
    return Response(response_data)


@permission_classes([AllowAny])
@api_view(["GET"])
def place(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instance = Place.objects.get(pk=pk)
        context = {
            "request":request
        }
        serializer = PlaceDetailSerializer(instance,context=context)
        response_data = {
            "status-code" : 6000,
            "data" : serializer.data
        }
        return Response(response_data)
    else:
        response_data = {
            "status-code" : 6001,
            "message" : "Place Not Found"
        }
        return Response(response_data)
    
    
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instance = Place.objects.get(pk=pk)
        context = {
            "request":request
        }
        serializer = PlaceDetailSerializer(instance,context=context)
        response_data = {
            "status-code" : 6000,
            "data" : serializer.data
        }
        return Response(response_data)
    else:
        response_data = {
            "status-code" : 6001,
            "message" : "Place Not Found"
        }
        return Response(response_data)
    
    
@permission_classes([AllowAny])
@api_view(["GET"])
def comments(request,pk):
    if Place.objects.filter(pk=pk).exists():
        place= Place.objects.get(pk=pk)
        instances = Comments.objects.filter(place=place)
        context = {
            "request":request
        }
        serializer = CommentsSerializer(instances,many=True,context=context)
        response_data = {
            "status-code" : 6000,
            "data" : serializer.data
        }
    
    else:
        response_data = {
            "status-code" : 6000,
            "message" : "Place not found"
        }
    return Response(response_data)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_create(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instance = Place.objects.get(pk=pk)
        description = request.data["description"]
        
        Comments.objects.create(
            author=request.user,
            description=description,
            place=instance,
            published_date=datetime.datetime.now()
        )
   
        response_data = {
            "status-code" : 6000,
            "message" : "Comment Created Succsesfully"
        }

    else:
        response_data = {
            "status-code" : 6001,
            "message" : "Author Not exists"
            }
    return Response(response_data)