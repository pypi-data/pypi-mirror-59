# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================
"""HDF5Dataset"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import uuid

import tensorflow as tf
from tensorflow_io.core.python.ops import core_ops

class HDF5IODataset(tf.data.Dataset):
  """HDF5IODataset"""

  def __init__(self,
               filename,
               dataset,
               internal=True):
    """HDF5IODataset."""
    with tf.name_scope("HDF5IODataset") as scope:
      assert internal

      # TODO: unique shared_name might be removed if HDF5 is thead-safe?
      resource, _ = core_ops.io_hdf5_readable_init(
          filename,
          container=scope,
          shared_name="%s/%s" % (filename, uuid.uuid4().hex))
      shape, dtype = core_ops.io_hdf5_readable_spec(resource, dataset)
      dtype = tf.as_dtype(dtype.numpy())

      self._resource = resource
      self._component = dataset
      self._shape = shape
      self._dtype = dtype

      step = 1024
      indices_start = tf.data.Dataset.range(0, shape[0], step)
      indices_stop = indices_start.skip(1).concatenate(
          tf.data.Dataset.from_tensor_slices([shape[0]]))
      dataset = tf.data.Dataset.zip((indices_start, indices_stop))
      def f(start, stop):
        shape = tf.concat(
            [tf.convert_to_tensor([stop - start], tf.int64), self._shape[1:]],
            axis=0)
        return core_ops.io_hdf5_readable_read(
            self._resource, start=start, shape=shape,
            component=self._component, dtype=self._dtype)
      dataset = dataset.map(f)
      dataset = dataset.unbatch()

      self._dataset = dataset
      super(HDF5IODataset, self).__init__(self._dataset._variant_tensor) # pylint: disable=protected-access

  def _inputs(self):
    return []

  @property
  def element_spec(self):
    return self._dataset.element_spec
