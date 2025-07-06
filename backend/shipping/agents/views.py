# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404
# from .models import Agent
# from shipments.models import Shipment
# from .serializers import AgentSerializer, ShipmentSerializer
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_earnings(request):
#     try:
#         agent = request.user.agent
#         serializer = AgentSerializer(agent)
#         return Response({'earnings': agent.total_earnings, 'agent': serializer.data})
#     except Agent.DoesNotExist:
#         return Response({'error': 'You are not an agent'}, status=status.HTTP_404_NOT_FOUND)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def available_shipments(request):
#     try:
#         agent = Agent.objects.get(user=request.user)
#     except Agent.DoesNotExist:
#         return Response({'error': 'You are not an agent'}, status=status.HTTP_404_NOT_FOUND)
#
#     shipments = Shipment.objects.filter(
#         status="PENDING",
#         origin=agent.city,
#         assigned_agent__isnull=True
#     )
#     serializer = ShipmentSerializer(shipments, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_shipments(request):
#     try:
#         agent = Agent.objects.get(user=request.user)
#     except Agent.DoesNotExist:
#         return Response({'error': 'You are not an agent'}, status=status.HTTP_404_NOT_FOUND)
#
#     shipments = Shipment.objects.filter(assigned_agent=agent).order_by('-created_at')
#     serializer = ShipmentSerializer(shipments, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def claim_shipment(request, shipment_id):
#     shipment = get_object_or_404(Shipment, id=shipment_id)
#
#     if shipment.status != 'PENDING':
#         return Response({'error': 'This shipment is not available'},
#                         status=status.HTTP_400_BAD_REQUEST)
#
#     try:
#         agent = Agent.objects.get(user=request.user)
#     except Agent.DoesNotExist:
#         return Response({'error': 'You are not an agent'},
#                         status=status.HTTP_404_NOT_FOUND)
#
#     if shipment.origin != agent.city:
#         return Response({'error': 'You can only deliver shipments from your city'},
#                         status=status.HTTP_400_BAD_REQUEST)
#
#     in_transit_count = Shipment.objects.filter(
#         assigned_agent=agent,
#         status='IN_TRANSIT'
#     ).count()
#
#     if in_transit_count >= 2:
#         return Response({'error': 'You cannot have more than 2 active shipments'},
#                         status=status.HTTP_400_BAD_REQUEST)
#
#     shipment.assigned_agent = agent
#     shipment.status = 'IN_TRANSIT'
#     shipment.save()
#
#     serializer = ShipmentSerializer(shipment)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def confirm_delivery(request, shipment_id):
#     shipment = get_object_or_404(Shipment, id=shipment_id)
#
#     try:
#         agent = Agent.objects.get(user=request.user)
#     except Agent.DoesNotExist:
#         return Response({'error': 'You are not an agent'},
#                         status=status.HTTP_404_NOT_FOUND)
#
#     if shipment.assigned_agent != agent:
#         return Response({'error': 'This shipment is not assigned to you'},
#                         status=status.HTTP_400_BAD_REQUEST)
#
#     if shipment.status == 'DELIVERED':
#         return Response({'error': 'This shipment has already been delivered'},
#                         status=status.HTTP_400_BAD_REQUEST)
#     # print(shipment.status)
#     shipment.status = 'DELIVERED'
#     shipment.save()
#     # print(agent)
#     agent.total_earnings = (agent.total_earnings or 0) + shipment.cost * 0.7
#     agent.save()
#
#     serializer = ShipmentSerializer(shipment)
#     return Response(serializer.data)

import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Agent
from shipments.models import Shipment
from .serializers import AgentSerializer, ShipmentSerializer

# admin controls delivery request
from rest_framework import viewsets, permissions
from .models import DeliveryRequest
from .serializers import DeliveryRequestSerializer

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_earnings(request):
    try:
        agent = request.user.agent
        serializer = AgentSerializer(agent)
        return Response({'earnings': agent.total_earnings, 'agent': serializer.data})
    except Agent.DoesNotExist:
        logger.error(f"Agent not found for user: {request.user.username}")
        return Response({'error': 'You are not an agent'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error in my_earnings: {str(e)}", exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_shipments(request):
    try:
        agent = Agent.objects.get(user=request.user)
        if not agent.city:
            logger.warning(f"Agent city not set for user: {request.user.username}")
            return Response({'error': 'Agent city not set'}, status=status.HTTP_400_BAD_REQUEST)
        logger.info(f"Fetching available shipments for agent: {agent.user.username}, city: {agent.city}")
        shipments = Shipment.objects.filter(
            status="PENDING",
            origin=agent.city,
            assigned_agent__isnull=True
        )
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)
    except Agent.DoesNotExist:
        logger.error(f"Agent not found for user: {request.user.username}")
        return Response({'error': 'You are not an agent'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error in available_shipments: {str(e)}", exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_shipments(request):
    try:
        agent = Agent.objects.get(user=request.user)
        logger.info(f"Fetching shipments for agent: {agent.user.username}")
        shipments = Shipment.objects.filter(assigned_agent=agent).order_by('-created_at')
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)
    except Agent.DoesNotExist:
        logger.error(f"Agent not found for user: {request.user.username}")
        return Response({'error': 'You are not an agent'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error in my_shipments: {str(e)}", exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def claim_shipment(request, shipment_id):
    try:
        shipment = get_object_or_404(Shipment, id=shipment_id)
        if shipment.status != 'PENDING':
            return Response({'error': 'This shipment is not available'}, status=status.HTTP_400_BAD_REQUEST)
        agent = Agent.objects.get(user=request.user)
        if shipment.origin != agent.city:
            return Response({'error': 'You can only deliver shipments from your city'}, status=status.HTTP_400_BAD_REQUEST)
        in_transit_count = Shipment.objects.filter(assigned_agent=agent, status='IN_TRANSIT').count()
        if in_transit_count >= 2:
            return Response({'error': 'You cannot have more than 2 active shipments'}, status=status.HTTP_400_BAD_REQUEST)
        shipment.assigned_agent = agent
        shipment.status = 'IN_TRANSIT'
        shipment.save()
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)
    except Agent.DoesNotExist:
        logger.error(f"Agent not found for user: {request.user.username}")
        return Response({'error': 'You are not an agent'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error in claim_shipment: {str(e)}", exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_delivery(request, shipment_id):
    try:
        shipment = get_object_or_404(Shipment, id=shipment_id)
        agent = Agent.objects.get(user=request.user)
        if shipment.assigned_agent != agent:
            return Response({'error': 'This shipment is not assigned to you'}, status=status.HTTP_400_BAD_REQUEST)
        if shipment.status == 'DELIVERED':
            return Response({'error': 'This shipment has already been delivered'}, status=status.HTTP_400_BAD_REQUEST)
        shipment.status = 'DELIVERED'
        shipment.save()
        agent.total_earnings = (agent.total_earnings or 0) + shipment.cost * 0.7
        agent.save()
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)
    except Agent.DoesNotExist:
        logger.error(f"Agent not found for user: {request.user.username}")
        return Response({'error': 'You are not an agent'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error in confirm_delivery: {str(e)}", exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# admindashborad agents list

class DeliveryRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeliveryRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'agent'):
            agent = user.agent
            return DeliveryRequest.objects.filter(agent=agent)
        else:
            return DeliveryRequest.objects.none()