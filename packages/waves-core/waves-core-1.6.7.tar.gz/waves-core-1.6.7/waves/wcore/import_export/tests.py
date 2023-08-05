from __future__ import unicode_literals

import json
import logging

from waves.wcore.import_export.services import ServiceSerializer
from waves.wcore.models import get_service_model, get_submission_model
from waves.wcore.tests.base import BaseTestCase

logger = logging.getLogger(__name__)
Service = get_service_model()
Submission = get_submission_model()


class SerializationTestCase(BaseTestCase):

    # @skip("Serialize / Unserialize needs code refactoring")
    def test_serialize_service(self):
        self.bootstrap_services()
        init_count = Service.objects.all().count()
        self.assertGreater(init_count, 0)
        file_paths = []
        for srv in Service.objects.all():
            file_out = srv.serialize()
            file_paths.append(file_out)
        for exp in file_paths:
            with open(exp) as fp:
                serializer = ServiceSerializer(data=json.load(fp))
                if serializer.is_valid():
                    serializer.save()
        self.assertEqual(init_count * 2, Service.objects.all().count())
