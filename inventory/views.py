import logging
from django.core.cache import cache  
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated

# Creating a logger 
logger = logging.getLogger('inventory')  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    """
    Method for creating new items in the inventory
    """
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        # Save the new item
        serializer.save()
        logger.info(f'Item created: {serializer.data}')  
        
        # Updating the cached item list
        cache_key = 'item_list' 
        items = cache.get(cache_key)  
        
        if items is not None:
            # Appending the new item to the cached list
            items.append(serializer.data)
            cache.set(cache_key, items, timeout=60 * 15) 
            logger.info('Added new item to the cached item list.')  
        else:
            # If the cache is empty, fetching from the database and updating the cache
            items = Item.objects.all()
            items_serializer = ItemSerializer(items, many=True)
            cache.set(cache_key, items_serializer.data, timeout=60 * 15)  
            logger.info('Fetched item list from database and cached it with the new item.')

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    logger.error(f'Item creation failed: {serializer.errors}')
    return Response({"error": "Item already exists."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_item_list(request):
    """
    Method for getting all items in the inventory
    """
    cache_key = 'item_list' 
    items = cache.get(cache_key)  
    
    # If not found in cache, fetching from the database
    if items is None:  
        items = Item.objects.all()
        # Checking if the queryset is empty
        if not items.exists():  
            logger.warning('No items found when fetching item list.')  
            return Response({"error": "No items found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(items, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 15)  
        logger.info('Fetched item list successfully and cached it.')  
    else:
        logger.info('Fetched item list from cache.')  

    return Response(items)  


@api_view(['GET', 'PUT', 'DELETE'])  
@permission_classes([IsAuthenticated])
def item_detail(request, item_id):
    """
    Method for getting, updating, and deleting items by item's id in the inventory
    """
    cache_key = f'item_{item_id}'
    item = cache.get(cache_key)  

    # If not found in cache, fetching from the database
    if not item:  
        try:
            item = Item.objects.get(id=item_id)
            cache.set(cache_key, item, timeout=60 * 15)  
        except Item.DoesNotExist:
            logger.error(f'Item not found with id: {item_id}')  
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    # For GET item details by ID 
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        logger.info(f'Item details fetched for id: {item_id}')  
        return Response(serializer.data)

    # For Updating Item details by ID 
    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Item updated: {serializer.data}')  
            cache.set(cache_key, serializer.instance, timeout=60 * 15)  
            logger.info(f'Item updated in cache for id: {item_id} {serializer.instance} {cache_key}')  
            return Response(serializer.data)
        logger.error(f'Item update failed for id {item_id}: {serializer.errors}')  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # For Deleting Item by ID 
    elif request.method == 'DELETE':
        item.delete()
        logger.info(f'Item deleted with id: {item_id}')  
        # Removing the item list from the cache
        cache.delete(cache_key)  
        return Response({"message": "Item deleted"}, status=status.HTTP_204_NO_CONTENT)

