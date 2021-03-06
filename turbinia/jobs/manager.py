# -*- coding: utf-8 -*-
# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This file contains a class for managing jobs."""

from __future__ import unicode_literals


class JobsManager(object):
  """The jobs manager."""

  _job_classes = {}

  @classmethod
  def DeregisterJob(cls, job_class):
    """Deregisters a job class.

    The job classes are identified based on their lower case name.

    Args:
      job_class (type): class object of the job.

    Raises:
      KeyError: if job class is not set for the corresponding name.
    """
    job_name = job_class.NAME.lower()
    if job_name not in cls._job_classes:
      raise KeyError('job class not set for name: {0:s}'.format(
          job_class.NAME))

    del cls._job_classes[job_name]

  @classmethod
  def GetJobInstance(cls, job_name):
    """Retrieves an instance of a specific job.

    Args:
      job_name (str): name of the job to retrieve.

    Returns:
      BaseJob: job instance.

    Raises:
      KeyError: if job class is not set for the corresponding name.
    """
    job_name = job_name.lower()
    if job_name not in cls._job_classes:
      raise KeyError(
          'job class not set for name: {0:s}.'.format(job_name))

    job_class = cls._job_classes[job_name]
    return job_class()

  @classmethod
  def GetJobInstances(cls, job_names):
    """Retrieves instances for all the specified jobs.

    Args:
      job_names (list[str]): names of the jobs to retrieve.

    Returns:
      list[BaseJob]: job instances.
    """
    job_instances = []
    for job_name, job_class in iter(cls.GetJobs()):
      if job_name in job_names:
        job_instances.append(job_class())

    return job_instances

  @classmethod
  def GetJobNames(cls):
    """Retrieves the names of all loaded jobs.

    Returns:
      list[str]: of job names.
    """
    return cls._job_classes.keys()

  @classmethod
  def GetJobs(cls):
    """Retrieves the registered jobs.

    Yields:
      tuple: containing:

        str: the uniquely identifying name of the job
        type: the job class.
    """
    for job_name, job_class in iter(cls._job_classes.items()):
      yield job_name, job_class

  @classmethod
  def RegisterJob(cls, job_class):
    """Registers a job class.

    The job classes are identified by their lower case name.

    Args:
      job_class (type): the job class to register.

    Raises:
      KeyError: if job class is already set for the corresponding name.
    """
    job_name = job_class.NAME.lower()
    if job_name in cls._job_classes:
      raise KeyError('job class already set for name: {0:s}.'.format(
          job_class.NAME))

    cls._job_classes[job_name] = job_class

  @classmethod
  def RegisterJobs(cls, job_classes):
    """Registers a job class.

    The job classes are identified by their lower case name.

    Args:
      job_classes (list[type]): the job classes to register.

    Raises:
      KeyError: if job class is already set for the corresponding name.
    """
    for job_class in job_classes:
      cls.RegisterJob(job_class)
