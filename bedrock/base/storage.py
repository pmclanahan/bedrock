# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This is here so that we can mix storages as we need. We'll do this for pipeline
# and whitenoise with hashing and gzip when we get those both working.
import os

from pipeline.storage import PipelineMixin
from whitenoise.django import GzipManifestStaticFilesStorage


class ManifestPipelineStorage(PipelineMixin, GzipManifestStaticFilesStorage):
    def post_process(self, paths, dry_run=False, **options):
        files = super(ManifestPipelineStorage, self).post_process(paths, dry_run, **options)
        to_link = {}

        for name, hashed_name, processed in files:
            if name != hashed_name:
                to_link[name] = hashed_name

            yield name, hashed_name, processed

        if dry_run:
            return

        for name, hashed_name in to_link.iteritems():
            name_path = self.path(name)
            os.unlink(name_path)
            os.symlink(self.path(hashed_name), name_path)
            yield name, hashed_name, True
