from tinydb import TinyDB

class AnalyseDatabase(TinyDB):
    def __init__(self, db_path='db.json'):
        super().__init__(db_path) # Inicializindo o objeto principal da classe no caso TinyDB
        self.jobs = self.table('jobs')
        self.resums = self.table('resums')
        self.analysis = self.table('analysis')
        self.files = self.table('files')