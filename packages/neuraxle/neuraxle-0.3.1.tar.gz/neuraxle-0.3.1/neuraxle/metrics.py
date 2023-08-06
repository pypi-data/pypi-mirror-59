"""
Neuraxle's metrics classes
=================================================
The neuraxle classes to track metrics results.

..
    Copyright 2019, Neuraxio Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
from typing import Dict, List

from neuraxle.base import MetaStepMixin, BaseStep, ExecutionContext
from neuraxle.data_container import DataContainer


class MetricsWrapper(MetaStepMixin, BaseStep):
    """
    Add metrics calculation to a step. Calculates metrics after each fit, fit_transform, or even transform if there is an expected outputs.

    Example usage :

    .. code-block:: python

        wrapped = MetricsWrapper(wrapped=wrapped, metrics=self.batch_metrics, name=BATCH_METRICS_STEP_NAME)
        wrapped = MiniBatchSequentialPipeline(
            [wrapped],
            batch_size=self.batch_size
        )


    .. seealso::
        :class:`DeepLearningPipeline`,
        :class:`MetaStepMixin`,
        :class:`BaseStep`
    """
    def __init__(
            self,
            wrapped: BaseStep,
            metrics: Dict,
            name: str = None,
            print_metrics=False,
            print_fun=print
    ):
        BaseStep.__init__(self, name=name)
        MetaStepMixin.__init__(self, wrapped)

        self.metrics: Dict = metrics
        self._initialize_metrics(metrics)

        self.print_metrics = print_metrics
        self.print_fun = print_fun
        self.enabled = True

    def _initialize_metrics(self, metrics):
        """
        Initialize metrics results dict for train, and validation using the metrics function dict.

        :param metrics: metrics function dict
        :type metrics: dict
        :return:
        """
        self.metrics_results_train = {}
        self.metrics_results_validation = {}

        for m in metrics:
            self.metrics_results_train[m] = []
            self.metrics_results_validation[m] = []

    def _did_transform(self, data_container: DataContainer, context: ExecutionContext) -> DataContainer:
        """
        Calculate metrics results after transform if there is an expected outputs in the data container.

        :param data_container: data container to calculate metrics for
        :type data_container: DataContainer
        :param context: execution context
        :return: data container
        :rtype: DataContainer
        """
        if data_container.expected_outputs is not None and len(data_container.expected_outputs) > 0:
            self._calculate_metrics_results(data_container)

        return data_container

    def _did_fit_transform(self, data_container: DataContainer, context: ExecutionContext) -> DataContainer:
        """
        Calculate metrics results after fit_transform if there is an expected outputs in the data container.

        :param data_container: data container to calculate metrics for
        :type data_container: DataContainer
        :param context: execution context
        :return: data container
        :rtype: DataContainer
        """
        if data_container.expected_outputs is not None and len(data_container.expected_outputs) > 0:
            self._calculate_metrics_results(data_container)

        return data_container

    def _calculate_metrics_results(self, data_container: DataContainer):
        """
        Calculate metrics results using the transformed data container, and the metrics function dict.

        :param data_container: transformed data container
        :type data_container: DataContainer
        :return:
        """
        if not self.enabled:
            return

        result = {}
        for metric_name, metric_fun in self.metrics.items():
            result_metric = metric_fun(data_container.data_inputs, data_container.expected_outputs)
            result[metric_name] = result_metric

            if self.is_train:
                self.metrics_results_train[metric_name].append(result_metric)
            else:
                self.metrics_results_validation[metric_name].append(result_metric)

        if self.print_metrics:
            self.print_fun(result)

    def get_all_metrics_train(self):
        """
        Get all train metrics results.

        :return: dict of all train metrics results
        :rtype: Dict[List]
        """
        return self.metrics_results_train

    def get_all_metrics_validation(self):
        """
        Get all validation metrics results.

        :return: dict of all validation metrics results
        :rtype: Dict[List]
        """
        return self.metrics_results_validation

    def get_metric_validation(self, metric_name) -> List:
        """
        Get validation result for a given metric name.

        :return: list of results
        """
        return self.metrics_results_validation[metric_name]

    def get_metric_train(self, metric_name) -> List:
        """
        Get train result for a given metric name.

        :return: list of results
        """
        return self.metrics_results_train[metric_name]

    def toggle_metrics(self):
        """
        Toggle metrics wrapper on and off to temporarily disable metrics if needed..

        :return:
        """
        self.enabled = not self.enabled
