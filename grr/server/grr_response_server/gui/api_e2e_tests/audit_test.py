#!/usr/bin/env python
"""Tests for API client and flows-related API calls."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals


from absl import app

from grr_response_server import data_store
from grr_response_server.gui import api_e2e_test_lib
from grr.test_lib import db_test_lib
from grr.test_lib import test_lib


class AuditTest(db_test_lib.RelationalDBEnabledMixin,
                api_e2e_test_lib.ApiE2ETest):

  def testFlowIsAudited(self):
    self.assertTrue(data_store.RelationalDBEnabled())
    self.assertTrue(data_store.RelationalDBEnabled())

    self.api.SearchClients(query=".")

    entries = data_store.REL_DB.ReadAPIAuditEntries()
    self.assertNotEmpty(entries)
    entry = entries[-1]

    self.assertEqual(entry.http_request_path,
                     "/api/v2/clients?count=50&offset=0&query=.")
    self.assertEqual(entry.response_code, "OK")
    self.assertEqual(entry.router_method_name, "SearchClients")
    self.assertEqual(entry.username, "api_test_robot_user")


def main(argv):
  test_lib.main(argv)


if __name__ == "__main__":
  app.run(main)
