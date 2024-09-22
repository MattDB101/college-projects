import grpc

# import the generated classes
import spellingGame_pb2
import spellingGame_pb2_grpc


def run():
    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:50055')

    # create a stub (client)
    stub = spellingGame_pb2_grpc.spellingGameStub(channel)
    game = stub.StartGame(spellingGame_pb2.startRequest(matchtype="double"))  # Client 2 uses double point factory pattern.

    totScore = 0
    print("Spelling Bee!")

    while True:
        print("Client received: " + game.letters)
        usrInput = input("\nEnter a word >>> ")
        response = stub.CheckWord(spellingGame_pb2.CheckRequest(word=usrInput, score=totScore))
        totScore+= response.score
        print("\n" + response.msg + f" \nThat word scored: {str(response.score)} points." + f" \nYour total score is: {str(totScore)} points.")


if __name__ == '__main__':
    run()
