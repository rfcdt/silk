import unittest

from app.domain.models import UnifiedHost

from .asset_merger import QualysAssetMerger


class AssetMergerTest(unittest.TestCase):
    def setUp(self):
        self.asset_merger = QualysAssetMerger()

    def test_merge(self):
        host = UnifiedHost(account_id=2)

        self.asset_merger.merge({}, host)
        print(host)
