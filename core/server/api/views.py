"""

POST запросы:

"""
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from server.models import *
import redis

HOST: str = 'redis'
PORT: int = 6379


class SiteEventCreateView(generics.CreateAPIView):
    serializer_class = SiteEventSerializer

    def perform_create(self, serializer):
        return serializer.save()


class SiteCreateView(generics.CreateAPIView):
    serializer_class = SiteSerializer

    def perform_create(self, serializer):
        return serializer.save()


class WorkerCreateView(generics.CreateAPIView):
    serializer_class = WorkerSerializer

    def perform_create(self, serializer):
        return serializer.save()


class PositionView(APIView):
    def get(self, request):
        site_id = request.data.get("site_id", None)
        if site_id is None:
            return Response({"OK": "False", "Description": "site_id should not be None"})

        redis_db = redis.Redis(host=HOST, port=PORT)
        worker_ids = redis_db.smembers(str(site_id))
        workers_list = []

        for worker_id in worker_ids:
            worker = Worker.objects.filter(id=worker_id).first()
            site_id = redis_db.hget(name=worker_id, key='site_id')
            lat = redis_db.hget(name=worker_id, key='lat')
            lon = redis_db.hget(name=worker_id, key='lon')

            workers_list.append({
                'worker_id': worker_id,
                'lon': lon,
                'lat': lat,
                'site_id': site_id,
                'worker_name': worker.fio
            })
        return Response({"OK": "True", "workers_list": workers_list})

    def post(self, request):
        worker_id = request.data.get("worker_id", None)
        site_id = request.data.get("site_id", None)
        lat = request.data.get("lat", None)
        lon = request.data.get("lon", None)
        if worker_id is None or site_id is None or lat is None or lon is None:
            return Response({"OK": "False", "Description": "worker_id, site_id, lat and lon should not be None"})
        redis_db = redis.Redis(host=HOST, port=PORT)
        last_site_id = redis_db.hget(name=worker_id, key='site_id')

        if last_site_id != site_id:
            if last_site_id:
                redis_db.srem(last_site_id, worker_id)
        redis_db.sadd(site_id, worker_id)

        redis_db.hset(
            name=worker_id, mapping={'site_id': site_id, 'lat': lat, 'lon': lon}
        )

        return Response({"OK": "True"})

