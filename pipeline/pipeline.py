# Copyright 2019 Google LLC
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
"""
DLaaS

Run this script to compile pipeline
"""

import kfp.dsl as dsl
import kfp.gcp as gcp
import kfp.onprem as onprem

platform = 'GCP'

@dsl.pipeline(
  name='DLaaS',
  description='Deep Learning as a Service'
)
def body_parts_pipeline(model_dir='gs://your-bucket/export', 
		   model_name='dummy',
		   server_name='dummy'):
		   

  serve_args = [
      '--model_path', model_dir,
      '--model_name', model_name,
      '--server_name', server_name
  ]

  serve = dsl.ContainerOp(
      name='serve',
      image='gcr.io/bigdata-2020/dlaas/body:latest',
      arguments=serve_args
  )

  steps = [serve]
  for step in steps:
    if platform == 'GCP':
      step.apply(gcp.use_gcp_secret('user-gcp-sa'))
    else:
      step.apply(onprem.mount_pvc(pvc_name, 'local-storage', '/mnt'))


if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(body_parts_pipeline, __file__ + '.tar.gz')

