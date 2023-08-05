# -*- coding: utf-8 -*-
""" Job tool WAVES admin dedicated views """
from __future__ import unicode_literals

from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from waves.wcore.exceptions import WavesException
from waves.wcore.models import Job
from waves.wcore.adaptors.const import JobStatus


class JobCancelView(View):
    """ View after cancel a job, if possible """

    def get(self, request):
        """ Try to cancel specified job (in kwargs), redirect to current job page """
        try:
            job = get_object_or_404(Job, id=self.kwargs['job_id'])
            runner = job.adaptor
            if runner is not None:
                runner.cancel_job(job)
            else:
                job.status = JobStatus.JOB_CANCELLED
                job.save()
            messages.add_message(request, level=messages.SUCCESS, message="Job cancelled")
        except WavesException as e:
            messages.add_message(request, level=messages.ERROR, message=e.message)
        return redirect(reverse('admin:wcore_job_change', args=[self.kwargs['job_id']]))


class JobRerunView(View):
    def get(self, request):
        job = get_object_or_404(Job, id=self.kwargs['job_id'])
        if job.allow_rerun:
            try:
                job.re_run()
                messages.success(request, message="Job '%s' successfully marked for re-run" % job.title)
            except WavesException as exc:
                messages.error(request, message="Error occured %s " % exc.message)
        else:
            messages.error(request, message="You can't rerun this job")
        return redirect(reverse('admin:wcore_job_changelist'))
