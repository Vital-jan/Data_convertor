# import config
from ratu.models.rfop_models import Rfop, Staterfop
from ratu.models.ruo_models import Kved
from ratu.services.main import Converter

class RfopConverter(Converter):
    
    #paths for remote and local source files
    FILE_URL = " https://data.gov.ua/dataset/b244f35a-e50a-4a80-b704-032c42ba8142/resource/06bbccbd-e19c-40d5-9e18-447b110c0b4c/download/"
    ZIPFILE_NAME = "rfop_ua.zip"

    #list of models for clearing DB
    tables=[
        Kved,
        Rfop,
        Staterfop
    ]
    
    #format record's data
    record={
        'RECORD': '',
        'FIO': '',
        'ADDRESS': '',
        'KVED': '',
        'STAN': ''
    }
    
    #creating list for registration items that had writed to db
    state_list=[]
    kved_list=[]
    
    def rename_xml_files ():
        new_filename = ""
        if (file.upper().find('UO') >= 0): new_filename = 'uo.xml'
        if (file.upper().find('FOP') >= 0): new_filename = 'fop.xml'
        return new_filename


    def save_to_db(self, rec): # save to db by Vital
        
            state_id = None

            for key in self.fop_status_array:
                if (self.fop_status_array[key] == rec['STAN']):
                    # existing value of state
                    state_id = key

            if (state_id == None):
                    # new value of Rfop.state
                    fopst = Fop_states (state = rec['STAN'])
                    fopst.save()
                    state_id = fopst.id
                    self.fop_status_array.append({'id': state_id, 'state': rec['STAN']}) # add item to array

                
            # writing entry to Rfop tablefrom
            ref = Fop_states.objects.get(id=state_id)

            rfop = Rfop(
                fullname=rec['FIO'],
                address=rec['ADDRESS'],
                kved=rec['KVED'],
                state=ref
                )
            rfop.save()
    # ------------ end of save to db by Vital
        
    #writing entry to db 
    def save_to_db(self, record):
        state_rfop=self.save_to_state_rfop_table(record)
        kved=self.save_to_kved_table(record)
        self.save_to_rfop_table(record, state_rfop, kved)
        print('saved')
        
    #writing entry to state_rfop table       
    def save_to_state_rfop_table(self, record):
        if record['STAN']:
            state_name=record['STAN']
        else:
            state_name=Staterfop.EMPTY_FIELD
        if not state_name in self.state_list:
            state_rfop = Staterfop(
                name=state_name
                )
            state_rfop.save()
            self.state_list.insert(0, state_name)
        state_rfop=Staterfop.objects.get(
            name=state_name
            )
        return
    
    #writing entry to kved table       
    def save_to_kved_table(self, record):
        if record['KVED']:
            kved_name=record['KVED']
        else:
            kved_name=Kved.EMPTY_FIELD
        if not kved_name in self.kved_list:
            kved = Kved(
                name=kved_name
                )
            kved.save()
            self.kved_list.insert(0, kved_name)
        kved=Kved.objects.get(
            name=kved_name
            )
        return kved
    
    #writing entry to rfop table
    def save_to_rfop_table(self, record, state_rfop, kved):
        rfop = Rfop(
            state=state_rfop,
            kved=kved,
            fullname=record['FIO'],
            address=record['ADDRESS']
            )
        rfop.save()
    
    print(
        'Rfop_class already imported. For start rewriting RFOP to the DB run > RfopConverter().process()\n',
        'For clear RFOP tables run > RfopConverter().clear_db()'
        )