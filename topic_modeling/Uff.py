class TopicTraining():
    """ Klasse für das Erstellen von Katzen
    Hilfetext ideal bei mehreren Programmierern in
    einem Projekt oder bei schlechtem Gedächtnis """

    def __init__(self, data, topics, iterations):
        self.data = data
        self.topics = topics
        self.iterations = iterations


    def tut_miauen(self):
        miau = self.data*self.topics
        return miau

    def print_tops(self):
        return miau

trainingsset = TopicTraining("Ein Text", 5, 3)

print(trainingsset.tut_miauen())
trainingsset.print_tops()