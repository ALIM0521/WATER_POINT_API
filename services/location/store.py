class LocationStore:
    # Demonstration seed data only; replace with field-verified data.
    def __init__(self):
        self.regions = [
            {"id": "REG-LT", "name": "Littoral"},
            {"id": "REG-CE", "name": "Centre"},
        ]
        self.villages = [
            {"id": "VIL-001", "name": "Sample Village A", "region_id": "REG-LT",
             "latitude": 4.0511, "longitude": 9.7679},
            {"id": "VIL-002", "name": "Sample Village B", "region_id": "REG-LT",
             "latitude": 4.0600, "longitude": 9.7500},
            {"id": "VIL-003", "name": "Sample Village C", "region_id": "REG-CE",
             "latitude": 3.8667, "longitude": 11.5167},
        ]

    def list_regions(self):
        return [x.copy() for x in self.regions]

    def villages_for_region(self, region_id):
        if not any(x["id"] == region_id for x in self.regions):
            raise KeyError(region_id)
        return [x.copy() for x in self.villages if x["region_id"] == region_id]

    def get_village(self, village_id):
        for village in self.villages:
            if village["id"] == village_id:
                return village.copy()
        raise KeyError(village_id)

    def map_locations(self):
        return [{"id": x["id"], "name": x["name"], "category": "village",
                 "latitude": x["latitude"], "longitude": x["longitude"]}
                for x in self.villages]
