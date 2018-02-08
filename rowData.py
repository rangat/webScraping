class rowData:
    numRows = 0
    def __init__(self, resNumber=0, year=0, medium="", publication="", sentence=""):
        self.resNumber = resNumber
        self.year = year
        self.medium = medium
        self.publication = publication
        self.sentence = sentence
        rowData.numRows += 1

    def __str__(self):
        return str(self.resNumber) + ', ' + str(self.year) + ', ' + self.medium + ', ' + self.publication + ', ' + self.sentence
