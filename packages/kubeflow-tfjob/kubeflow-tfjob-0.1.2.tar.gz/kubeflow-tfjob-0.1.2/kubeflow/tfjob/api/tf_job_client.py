# Copyright 2019 The Kubeflow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import multiprocessing
import time

from kubernetes import client, config

from kubeflow.tfjob.constants import constants
from kubeflow.tfjob.utils import utils

from .tf_job_watch import watch as tfjob_watch

class TFJobClient(object):

  def __init__(self, config_file=None, context=None, # pylint: disable=too-many-arguments
               client_configuration=None, persist_config=True):
    """
    TFJob client constructor
    :param config_file: kubeconfig file, defaults to ~/.kube/config
    :param context: kubernetes context
    :param client_configuration: kubernetes configuration object
    :param persist_config:
    """
    if config_file or not utils.is_running_in_k8s():
      config.load_kube_config(
        config_file=config_file,
        context=context,
        client_configuration=client_configuration,
        persist_config=persist_config)
    else:
      config.load_incluster_config()

    self.api_instance = client.CustomObjectsApi()


  def create(self, tfjob, namespace=None):
    """
    Create the TFJob
    :param tfjob: tfjob object
    :param namespace: defaults to current or default namespace
    :return: created tfjob
    """

    if namespace is None:
      namespace = utils.set_tfjob_namespace(tfjob)

    try:
      outputs = self.api_instance.create_namespaced_custom_object(
        constants.TFJOB_GROUP,
        constants.TFJOB_VERSION,
        namespace,
        constants.TFJOB_PLURAL,
        tfjob)
    except client.rest.ApiException as e:
      raise RuntimeError(
        "Exception when calling CustomObjectsApi->create_namespaced_custom_object:\
         %s\n" % e)

    return outputs

  def get(self, name=None, namespace=None, watch=False, timeout_seconds=600): #pylint: disable=inconsistent-return-statements
    """
    Get the tfjob
    :param name: existing tfjob name, if not defined, the get all tfjobs in the namespace.
    :param namespace: defaults to current or default namespace
    :param watch: Watch the TFJob if `True`.
    :param timeout_seconds: How long to watch the job..
    :return: tfjob
    """
    if namespace is None:
      namespace = utils.get_default_target_namespace()

    if name:
      if watch:
        tfjob_watch(
          name=name,
          namespace=namespace,
          timeout_seconds=timeout_seconds)
      else:
        thread = self.api_instance.get_namespaced_custom_object(
          constants.TFJOB_GROUP,
          constants.TFJOB_VERSION,
          namespace,
          constants.TFJOB_PLURAL,
          name,
          async_req=True)

        tfjob = None
        try:
          tfjob = thread.get(constants.APISERVER_TIMEOUT)
        except multiprocessing.TimeoutError:
          raise RuntimeError("Timeout trying to get TFJob.")
        except client.rest.ApiException as e:
          raise RuntimeError(
            "Exception when calling CustomObjectsApi->get_namespaced_custom_object:\
            %s\n" % e)
        except Exception as e:
          raise RuntimeError(
            "There was a problem to get TFJob {0} in namespace {1}. Exception: \
            {2} ".format(name, namespace, e))
        return tfjob
    else:
      if watch:
        tfjob_watch(
            namespace=namespace,
            timeout_seconds=timeout_seconds)
      else:
        thread = self.api_instance.list_namespaced_custom_object(
          constants.TFJOB_GROUP,
          constants.TFJOB_VERSION,
          namespace,
          constants.TFJOB_PLURAL,
          async_req=True)

        tfjobs = None
        try:
          tfjobs = thread.get(constants.APISERVER_TIMEOUT)
        except multiprocessing.TimeoutError:
          raise RuntimeError("Timeout trying to get TFJob.")
        except client.rest.ApiException as e:
          raise RuntimeError(
            "Exception when calling CustomObjectsApi->list_namespaced_custom_object:\
            %s\n" % e)
        except Exception as e:
          raise RuntimeError(
            "There was a problem to list TFJobs in namespace {0}. \
            Exception: {1} ".format(namespace, e))
        return tfjobs


  def patch(self, name, tfjob, namespace=None):
    """
    Patch existing tfjob
    :param name: existing tfjob name
    :param tfjob: patched tfjob
    :param namespace: defaults to current or default namespace
    :return: patched tfjob
    """
    if namespace is None:
      namespace = utils.set_tfjob_namespace(tfjob)

    try:
      outputs = self.api_instance.patch_namespaced_custom_object(
        constants.TFJOB_GROUP,
        constants.TFJOB_VERSION,
        namespace,
        constants.TFJOB_PLURAL,
        name,
        tfjob)
    except client.rest.ApiException as e:
      raise RuntimeError(
        "Exception when calling CustomObjectsApi->patch_namespaced_custom_object:\
         %s\n" % e)

    return outputs


  def delete(self, name, namespace=None):
    """
    Delete the tfjob
    :param name: tfjob name
    :param namespace: defaults to current or default namespace
    :return:
    """
    if namespace is None:
      namespace = utils.get_default_target_namespace()

    try:
      return self.api_instance.delete_namespaced_custom_object(
        constants.TFJOB_GROUP,
        constants.TFJOB_VERSION,
        namespace,
        constants.TFJOB_PLURAL,
        name,
        client.V1DeleteOptions())
    except client.rest.ApiException as e:
      raise RuntimeError(
        "Exception when calling CustomObjectsApi->delete_namespaced_custom_object:\
         %s\n" % e)


  def wait_for_job(self, name, #pylint: disable=inconsistent-return-statements
                   namespace=None,
                   timeout_seconds=600,
                   polling_interval=30,
                   watch=False,
                   status_callback=None):
    """Wait for the specified job to finish.

    :param name: Name of the TfJob.
    :param namespace: defaults to current or default namespace.
    :param timeout_seconds: How long to wait for the job.
    :param polling_interval: How often to poll for the status of the job.
    :param watch: Watch the TFJob if `True`.
    :param status_callback: (Optional): Callable. If supplied this callable is
           invoked after we poll the job. Callable takes a single argument which
           is the job.
    :return:
    """
    if namespace is None:
      namespace = utils.get_default_target_namespace()

    if watch:
      tfjob_watch(
        name=name,
        namespace=namespace,
        timeout_seconds=timeout_seconds)
    else:
      return self.wait_for_condition(
        name,
        ["Succeeded", "Failed"],
        namespace=namespace,
        timeout_seconds=timeout_seconds,
        polling_interval=polling_interval,
        status_callback=status_callback)


  def wait_for_condition(self, name,
                         expected_condition,
                         namespace=None,
                         timeout_seconds=600,
                         polling_interval=30,
                         status_callback=None):
    """Waits until any of the specified conditions occur.

    :param name: Name of the job.
    :param expected_condition: A list of conditions. Function waits until any of the
           supplied conditions is reached.
    :param namespace: defaults to current or default namespace.
    :param timeout_seconds: How long to wait for the job.
    :param polling_interval: How often to poll for the status of the job.
    :param status_callback: (Optional): Callable. If supplied this callable is
           invoked after we poll the job. Callable takes a single argument which
           is the job.
    :return: Object TFJob status
    """

    if namespace is None:
      namespace = utils.get_default_target_namespace()

    for _ in range(round(timeout_seconds/polling_interval)):

      tfjob = None
      tfjob = self.get(name, namespace=namespace)

      if tfjob:
        if status_callback:
          status_callback(tfjob)

        # If we poll the CRD quick enough status won't have been set yet.
        conditions = tfjob.get("status", {}).get("conditions", [])
        # Conditions might have a value of None in status.
        conditions = conditions or []
        for c in conditions:
          if c.get("type", "") in expected_condition:
            return tfjob

      time.sleep(polling_interval)

    raise RuntimeError(
      "Timeout waiting for TFJob {0} in namespace {1} to enter one of the "
      "conditions {2}.".format(name, namespace, expected_condition), tfjob)


  def get_job_status(self, name, namespace=None):
    """Returns TFJob status, such as Running, Failed or Succeeded.

    :param name: The TFJob name.
    :param namespace: defaults to current or default namespace.
    :return: Object TFJob status
    """
    if namespace is None:
      namespace = utils.get_default_target_namespace()

    tfjob = self.get(name, namespace=namespace)
    last_condition = tfjob.get("status", {}).get("conditions", [])[-1]
    return last_condition.get("type", "")


  def is_job_running(self, name, namespace=None):
    """Returns true if the TFJob running; false otherwise.

    :param name: The TFJob name.
    :param namespace: defaults to current or default namespace.
    :return: True or False
    """
    tfjob_status = self.get_job_status(name, namespace=namespace)
    return tfjob_status.lower() == "running"


  def is_job_succeeded(self, name, namespace=None):
    """Returns true if the TFJob succeeded; false otherwise.

    :param name: The TFJob name.
    :param namespace: defaults to current or default namespace.
    :return: True or False
    """
    tfjob_status = self.get_job_status(name, namespace=namespace)
    return tfjob_status.lower() == "succeeded"
