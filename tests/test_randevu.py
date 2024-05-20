import unittest
from datetime import datetime, timezone

from randevu import rdv, rdvt

class TestRdv(unittest.TestCase):
    def test_rdv0(self):
        self.assertEqual(rdv("COREJOURNEY", datetime(2024, 5, 10, tzinfo=timezone.utc)), 0)
    
    def test_rdv7(self):
        self.assertEqual(rdv("GTA_V_FLYING_MUSIC_Z7RfRLsqECI", datetime(2024, 5, 10, tzinfo=timezone.utc)), 7)
    
    def test_rdv8(self):
        self.assertEqual(rdv("THE_COVENANT_2023", datetime(2024, 5, 10, tzinfo=timezone.utc)), 8)
    
    def test_rdv9(self):
        self.assertEqual(rdv("NO_BOILERPLATE", datetime(2024, 5, 10, tzinfo=timezone.utc)), 9)

class TestRdvt(unittest.TestCase):
    def test_rdvt0(self):
        self.assertEqual(rdvt(0, "COREJOURNEY", datetime(2024, 5, 10, tzinfo=timezone.utc)), datetime(2024, 5, 10, 8, 34, 51, 226747, tzinfo=timezone.utc))
    
    def test_rdvt1(self):
        self.assertEqual(rdvt(1, "GTA_V_FLYING_MUSIC_Z7RfRLsqECI", datetime(2024, 5, 10, tzinfo=timezone.utc)), datetime(2024, 5, 10, 19, 33, 44, 824030, tzinfo=timezone.utc))
    
    def test_rdvt10(self):
        self.assertEqual(rdvt(10, "THE_COVENANT_2023", datetime(2024, 5, 10, tzinfo=timezone.utc)), datetime(2024, 5, 10, 16, 58, 30, 927007, tzinfo=timezone.utc))
    
    def test_rdvt100(self):
        self.assertEqual(rdvt(100, "NO_BOILERPLATE", datetime(2024, 5, 10, tzinfo=timezone.utc)), datetime(2024, 5, 10, 0, 27, 37, 142724, tzinfo=timezone.utc))

if __name__ == "__main__":
    unittest.main()
