""" Base class for exporting objects """
from __future__ import unicode_literals

from os.path import join

from django.contrib import messages
from django.shortcuts import redirect
from waves.wcore.settings import waves_settings as config
from waves.wcore.models.base import ExportAbleMixin
from waves.wcore.views.files import DownloadFileView


class ModelExportView(DownloadFileView):
    """ Enable simple model export with DRF subclasses must declare property method to set up
    serializer used for process
    """
    model = None
    _force_download = True
    serializer = None
    return_view = "admin:index"

    def get_context_data(self, **kwargs):
        context = super(ModelExportView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        from waves.wcore.models.base import ExportError
        try:
            return super(ModelExportView, self).get(request, *args, **kwargs)
        except ExportError as e:
            messages.error(self.request, 'Oops: %s' % e)
            return redirect(self.return_view)

    @property
    def file_path(self):
        return join(config.DATA_ROOT, 'export', self.file_name)

    @property
    def file_name(self):
        return self.object.export_file_name

    @property
    def file_description(self):
        return "Export file for %s " % self.model.__class__.__name__

