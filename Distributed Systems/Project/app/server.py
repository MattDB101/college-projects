import grpc
from app.gameimpl import standardScoring
from app.gameimpl import doublePoints
from factories import objectFactory
from concurrent import futures

# import the generated classes
import spellingGame_pb2
import spellingGame_pb2_grpc

# import the original calculator.py
from app import dictionary

dict = dictionary.Dictionary()


# from pattern import object_factory

# create a class to define the server functions

class spellingGameServicer(spellingGame_pb2_grpc.spellingGameServicer):

    def __init__(self):
        self.factory = objectFactory.ObjectFactory()
        self.factory.register_builder("standard", standardScoring.StandardGameBuilder())
        self.factory.register_builder("double", doublePoints.DoubleGameBuilder())
        self.string = ' '.join(dict.getPangram())
        self.specialCharIndex = len(self.string) // 2
        self.string = self.string[:self.specialCharIndex] + '{' + self.string[
                                                                  self.specialCharIndex::self.specialCharIndex + 1] + '}' + self.string[
                                                                                                                            self.specialCharIndex + 1:]  # slicing to add the { } around special character.
        self.specialCharIndex += 1  # compensate for added "{" character
        self.multiplier = 0

    def StartGame(self, request, context):
        new_match = self.factory.create(request.matchtype)
        self.multiplier = new_match.getMultiplier()
        return spellingGame_pb2.startResponse(letters=self.string)

    def CheckWord(self, request, context):

        word = request.word.lower()
        totScore = request.score
        score = 0
        res = "Too short."

        if len(word) > 3:  # if the word is too short, don't do anything as variables are initialized to this by default

            for i in set(word):  # verify word only uses characters in string.
                if i not in self.string:
                    return spellingGame_pb2.CheckResponse(msg="Only use the characters provided!", score=score,
                                                          totScore=totScore)

            if self.string[
                self.specialCharIndex] not in word:  # if the special character isn't used, don't call checkWord
                res = f"Invalid word, missing centre letter {self.string[self.specialCharIndex]}."

            else:
                res = dict.checkWord(word)

                if res == "Pangram!":
                    score += len(word) + 7
                    totScore += score

                if res == "Valid word.":
                    if len(word) == 4:
                        score += 1
                    else:
                        score += len(word)
                    totScore += score

        score *= self.multiplier
        return spellingGame_pb2.CheckResponse(msg=res, score=score, totScore=totScore)


def serve():
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # use the generated function add_CalculatorServicer_to_server to add the defined class to the server
    spellingGame_pb2_grpc.add_spellingGameServicer_to_server(spellingGameServicer(), server)
    print('Starting server. Listening on port 50055.')
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
