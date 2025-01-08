from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Station, Train
from .serializers import OrderSerializer

# Constants for cost calculation and caching
BASE_COST_PER_DAY = 500
COST_PER_KM = 200
AVERAGE_SPEED = 250
CACHE_TIMEOUT = 60 * 15  # Cache for 15 minutes

# Helper function to calculate the distance between two locations
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0  # Radius of the Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Order ViewSet for handling cost calculation
class OrderViewSet:

    @action(detail=False, methods=['post'])
    def cost(self, request):
        # Deserialize incoming data
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Extract validated data
        start_location_name = serializer.validated_data['start_location']['name']
        start_date = serializer.validated_data['start_date']
        count = serializer.validated_data['count']
        
        # Lookup station with caching to avoid redundant queries
        start_location = cache.get_or_set(
            f'station:{start_location_name}',
            Station.objects.filter(name=start_location_name).first(),
            CACHE_TIMEOUT
        )
        
        # Handle case if station is not found
        if not start_location:
            return Response({'error': 'Start location not found'}, status=404)
        
        # Initialize variables
        today = datetime.now()
        start_day = datetime.strptime(start_date, '%Y-%m-%d')
        best_cost = float('inf')  # Set a high initial cost

        # Cache train data to avoid repeated DB queries
        trains = cache.get_or_set('all_trains', Train.objects.all(), CACHE_TIMEOUT)

        # Iterate over each train to calculate costs
        for train in trains:
            # Calculate distance to destination
            distance = calculate_distance(
                start_location.x_axis,
                start_location.y_axis,
                train.end_location.x_axis,
                train.end_location.y_axis
            )

            # Calculate the estimated arrival day
            final_day = today + timedelta(days=train.days_until_destination)
            travel_days = distance / AVERAGE_SPEED
            estimated_arrival = final_day + timedelta(days=travel_days)

            # Skip trains that arrive after the desired start date
            if estimated_arrival > start_day:
                continue

            # Calculate the difference in days and the cost
            days_difference = (start_day - estimated_arrival).days
            current_cost = count * (days_difference * BASE_COST_PER_DAY + int(distance) * COST_PER_KM)

            # Update the best cost if the train has enough capacity
            if train.count >= count:
                best_cost = min(best_cost, current_cost)

        # Return result or error if no suitable train was found
        if best_cost == float('inf'):
            return Response({'error': 'No suitable trains found'}, status=404)
        return Response({'estimated_cost': best_cost}, status=200)
