from datetime import datetime

class LabResult:
    def __init__(self, pcr, vsg, fr, ana):
        self.pcr = pcr
        self.vsg = vsg
        self.fr = fr
        self.ana = ana
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            'pcr': self.pcr,
            'vsg': self.vsg,
            'fr': self.fr,
            'ana': self.ana,
            'timestamp': self.timestamp.isoformat()
        }

class Analysis:
    def __init__(self, lab_result, interpretation):
        self.lab_result = lab_result
        self.interpretation = interpretation
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            'lab_result': self.lab_result.to_dict(),
            'interpretation': self.interpretation,
            'timestamp': self.timestamp.isoformat()
        }