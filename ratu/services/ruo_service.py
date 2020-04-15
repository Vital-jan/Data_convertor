import config
from ratu.models.ruo_models import Founders, Kved, Ruo, State
from ratu.services.main import Converter

class RuoConverter(Converter):
    
    #paths for remote and local source files
    FILE_URL = ""
    LOCAL_FILE_NAME = "uo.xml"

    #list of models for clearing DB
    tables=[
        Founders,
        Ruo,     
    ]
    
    #format record's data
    record={
        'RECORD': '',
        'NAME': '',
        'SHORT_NAME': '',
        'EDRPOU': '',
        'ADDRESS': '',
        'BOSS': '',
        'KVED': '',
        'STAN': '',
        'FOUNDING_DOCUMENT_NUM': '',
        'FOUNDERS': '',
        'FOUNDER': []
    }

    #creating dictionaries for registration items that had writed to db
    state_dict={} # dictionary uses for keeping whole model class objects
    kved_dict={}

    for state in State.objects.all():
        state_dict[state.name]=state
    for kved in Kved.objects.all():
        kved_dict[kved.name]=kved
    
    def unzip_file(self): # empty function, because unzipping process executes in rfop module
        return

    #writing entry to db 
    def save_to_db(self, record):
        state=self.save_to_state_table(record)
        kved=self.save_to_kved_table(record)
        ruo=self.save_to_ruo_table(record, state, kved)
        self.save_to_founders_table(record, ruo)
        print('saved')
        
    #writing entry to state table       
    def save_to_state_table(self, record):
        if record['STAN']:
            state_name=record['STAN']
        else:
            state_name=State.EMPTY_FIELD
        if not state_name in self.state_dict:
            state = State(
                name=state_name
                )
            state.save()
            self.state_dict[state_name]=state
            return state
        state=self.state_dict[state_name]
        return state
    
    #writing entry to kved table       
    def save_to_kved_table(self, record):
        if record['KVED']:
            kved_name=record['KVED']
        else:
            kved_name=Kved.EMPTY_FIELD
        if not kved_name in self.kved_dict:
            kved = Kved(
                name=kved_name
                )
            kved.save()
            self.kved_dict[kved_name]=kved
            return kved
        kved=self.kved_dict[kved_name]
        return kved
    
    #writing entry to ruo table
    def save_to_ruo_table(self, record, state, kved):
        ruo = Ruo.objects.filter(
            state=state.id,
            kved=kved.id,
            name=record['NAME'],
            short_name=record['SHORT_NAME'],
            edrpou=record['EDRPOU'],
            address=record['ADDRESS'],
            boss=record['BOSS']  
        )
        if ruo.exists():  
            return ruo
        ruo = Ruo(
            state=state,
            kved=kved,
            name=record['NAME'],
            short_name=record['SHORT_NAME'],
            edrpou=record['EDRPOU'],
            address=record['ADDRESS'],
            boss=record['BOSS'] 
        )
        ruo.save()
        return ruo

    #writing entry to founder table
    def save_to_founders_table(self, record, ruo):
        _create_queues=list()          
        for founder in record['FOUNDER']:
            founders = Founders(
                company=ruo,
                founder=founder
            )
            _create_queues.append(founders)    
        Founders.objects.bulk_create(_create_queues)
    print(
        'Ruo already imported. For start rewriting RUO to the DB run > RuoConverter().process()\n',
        'For clear RUO tables run > RuoConverter().clear_db()'
        )