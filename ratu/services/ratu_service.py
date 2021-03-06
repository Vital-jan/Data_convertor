import config
from ratu.models.ratu_models import Region, District, City, Citydistrict, Street
from ratu.services.main import Converter, BulkCreateManager

class RatuConverter(Converter):
    
    #paths for remote and local source files
    FILE_URL = config.FILE_URL
    LOCAL_FILE_NAME = config.LOCAL_FILE_NAME
    LOCAL_FOLDER = config.LOCAL_FOLDER
    CHUNK_SIZE = 200

    #list of models for clearing DB
    tables=[
        Region,
        District,
        City,
        Citydistrict,
        Street
    ]
    
    #format record's data 
    record={
        'RECORD': '',
        'OBL_NAME': '',
        'REGION_NAME': '',
        'CITY_NAME': '',
        'CITY_REGION_NAME': '',
        'STREET_NAME': ''
    }
 
    #creating dictionary & lists for registration items that had writed to db 
    region_dict = {} # dictionary uses for keeping whole model class objects
    district_list = list() # lists use for keeping cells content
    city_list = list()
    citydistrict_list = list()

    bulk_manager = BulkCreateManager(CHUNK_SIZE)
    
    #writing entry to db
    def save_to_db(self, record):
        region=self.save_to_region_table(record)
        district=self.save_to_district_table(record, region)
        city=self.save_to_city_table(record,region, district)
        citydistrict=self.save_to_citydistrict_table(record, region, district, city)
        self.save_to_street_table(record,region, district, city, citydistrict)
        print('saved')
    
    #writing entry to region table           
    def save_to_region_table(self, record):
        if not record['OBL_NAME'] in self.region_dict:
            region = Region(
                name=record['OBL_NAME']
                )
            region.save()
            self.region_dict[record['OBL_NAME']]=region
            return region
        region=self.region_dict[record['OBL_NAME']]
        return region
    
    #writing entry to district table    
    def save_to_district_table(self, record, region):
        if record['REGION_NAME']:
            district_name=record['REGION_NAME']
        else:
            district_name=District.EMPTY_FIELD
        if not [region.id, district_name] in self.district_list:
            district = District(
                region=region, 
                name=district_name
                )
            district.save()
            self.district_list.insert(0, [region.id, district_name])
        district=District.objects.get(
            name=district_name,
            region=region.id
            )
        return district

    #writing entry to city table    
    def save_to_city_table(self, record, region, district):
        if record['CITY_NAME']:
            city_name=record['CITY_NAME']
        else:
            city_name=City.EMPTY_FIELD 
        if not [region.id, district.id, city_name] in self.city_list:
            city = City(
                region=region, 
                district=district,
                name=city_name
                )
            city.save()
            self.city_list.insert(0, [region.id, district.id, city_name])
        city=City.objects.get(
            name=city_name,
            region=region.id,
            district=district.id
            )
        return city
    
    #writing entry to citydistrict table
    def save_to_citydistrict_table(self, record, region, district, city):
        if record['CITY_REGION_NAME']:
            citydistrict_name=record['CITY_REGION_NAME']
        else:
            citydistrict_name=Citydistrict.EMPTY_FIELD
        if not [region.id, district.id, city.id, citydistrict_name] in self.citydistrict_list:
            citydistrict = Citydistrict(
                region=region, 
                district=district,
                city=city,
                name=citydistrict_name
                )
            citydistrict.save()
            self.citydistrict_list.insert(0, [region.id, district.id, city.id, citydistrict_name])
        citydistrict=Citydistrict.objects.get(
            name=citydistrict_name,
            region=region.id,
            district=district.id,
            city=city.id
            )
        return citydistrict
    
    #writing entry to street table
    def save_to_street_table(self, record, region, district, city, citydistrict):    
        if record['STREET_NAME']:
            street = Street(
                region=region, 
                district=district,
                city=city,
                citydistrict=citydistrict,
                name=record['STREET_NAME']
                )
            self.bulk_manager.add(street)
       
    print(
        'Ratu already imported. For start rewriting RATU to the DB run > RatuConverter().process()\n',
        'For clear all RATU tables run > RatuConverter().clear_db()'
        )