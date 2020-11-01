import redis
import base64
from uuid import UUID

from django.http import QueryDict
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from server.models import *

HOST: str = 'redis'
PORT: int = 6379


def to_site_key(id_):
    return f'site:{id_}'


def to_worker_key(id_):
    return f'worker:{id_}'


class SiteEventCreateView(generics.CreateAPIView):
    serializer_class = SiteEventSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.get('data', None)
        if data is not None and 'site_id' in data:
            request.data['site_id'] = data.pop('site_id')

        return super().post(request, *args, **kwargs)


class SiteCreateView(generics.CreateAPIView):
    serializer_class = SiteSerializer


class WorkerCreateView(generics.CreateAPIView):
    serializer_class = WorkerSerializer


class WorkerView(generics.RetrieveAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class ShortSiteView(generics.RetrieveAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteShortSerializer


class SiteView(generics.RetrieveAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class ShortSiteListView(generics.ListAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteShortSerializer


class PositionView(APIView):
    def get(self, request):
        site_id = request.GET.get('site_id', None)
        if site_id is None:
            return Response({'ok': False, 'Description': 'site_id should not be None'})

        redis_db = redis.Redis(host=HOST, port=PORT)

        site_key = to_site_key(site_id)
        worker_ids = redis_db.smembers(site_key)
        workers_list = []

        for worker_id in worker_ids:
            worker = Worker.objects.filter(id=worker_id).first()
            if worker is None:
                continue

            worker_key = to_worker_key(worker_id.decode())
            site_id = redis_db.hget(name=worker_key, key='site_id')
            lat = redis_db.hget(name=worker_key, key='lat')
            lon = redis_db.hget(name=worker_key, key='lon')

            workers_list.append({
                'worker_id': worker_id,
                'lon': lon,
                'lat': lat,
                'site_id': site_id,
                'worker_name': worker.fio
            })

        return Response({'ok': True, 'workers_list': workers_list})

    def post(self, request):
        redis_db = redis.Redis(host=HOST, port=PORT)

        worker_id = request.data.get("worker_id", None)
        site_id = request.data.get("site_id", None)
        lat = request.data.get("lat", None)
        lon = request.data.get("lon", None)
        if worker_id is None or site_id is None or lat is None or lon is None:
            return Response({"ok": False, "Description": "worker_id, site_id, lat and lon should not be None"})

        worker_key = to_worker_key(worker_id)
        site_key = to_site_key(site_id)

        last_site_id = redis_db.hget(name=worker_id, key='site_id')
        if last_site_id != site_id:
            redis_db.sadd(site_key, worker_id)
            if last_site_id is not None:
                last_site_key = to_site_key(last_site_id)
                redis_db.srem(last_site_key, worker_id)

        redis_db.hset(
            name=worker_key, mapping={'site_id': site_id, 'lat': lat, 'lon': lon}
        )

        return Response({'ok': True})


from rest_framework.parsers import BaseParser
from rest_framework import renderers
from rest_framework.settings import api_settings
from django.conf import settings
from rest_framework.utils import json
import codecs
class MJSONParser(BaseParser):
    media_type = 'application/json'
    renderer_class = renderers.JSONRenderer
    strict = api_settings.STRICT_JSON

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as JSON and returns the resulting data.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            decoded_stream = codecs.getreader(encoding)(stream)
            parse_constant = json.strict_constant if self.strict else None
            return json.load(decoded_stream, parse_constant=parse_constant)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % str(exc))


class SensorReportView(APIView):
    queryset = SensorReport.objects.all()
    parser_classes = [MJSONParser]

    def post(self, request):
        if isinstance(request.data, QueryDict):
            request_data = dict(request.data.iterlists())
        else:
            request_data = request.data

        uuid = request_data.pop('uuid', None)
        site_id = request_data.pop('site', None)

        if uuid is None or site_id is None:
            return Response({'ok': False, "Description": "uuid and site should not be None"})
        uuid = UUID(bytes=base64.urlsafe_b64decode(uuid.encode('ascii')+'=='.encode('ascii')))
        data = {
            'site': site_id,
            'uid': uuid.hex,
            'data': request_data
        }

        serializer = SensorReportSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'ok': True})
        return Response({'ok': False})

    def get(self, request):
        site_id = request.GET.get('site_id', None)
        if site_id is None:
            return Response({'ok': False, 'error': 'Provide site_id'})

        reports = SensorReport.objects.raw("""
        select data, created_at, uid, site_id, id from (
            select
                data,
                created_at,
                uid,
                site_id,
                id,
                row_number() over(partition by uid order by created_at desc) as rn
            from
                server_sensorreport
        ) t
        where t.rn = 1
        """)

        data = []
        for report in reports:
            data.append(SensorReportSerializer(instance=report).data)

        return Response(data)
