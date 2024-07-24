import greet_pb2_grpc
import greet_pb2
import time
import grpc

def get_client_steam_requests():
	while True:
		name = input("Please enter a name (or nothing to stop chatting): " )
		if name == "":
			break
		
		hello_request = greet_pb2.HelloRequest(greeting = "Hello", name = name)
		yield hello_request
		time.sleep(1)

def run():
	with grpc.insecure_channel('localhost:5000') as channel:
		stub = greet_pb2_grpc.GreeterStub(channel)
		print("1. SayHello - Unary")
		print("2. ParrotSaysHello - Server Side steaming")
		print("3. ChattyClientSayHello - Client side Steaming")
		print("4. InteractingHello - Both Steaming")
		rpc_call = input("Which rpc would you like to make: ")
  
		if rpc_call == "1":
			hello_request = greet_pb2.HelloRequest(greeting  = "Bonjour", name = "YouTube")
			hello_reply = stub.SayHello(hello_request)
			print("SayHello Response Recieved:")
			print(hello_reply)
		elif rpc_call == "2":
			hello_request = greet_pb2.HelloRequest(greeting  = "Bonjour", name = "YouTube")
			hello_replies = stub.ParrotSaysHello(hello_request)

			for hello_reply in hello_replies:
				print("ParrotSaysHello Response Received:")
				print(hello_reply)

		elif rpc_call == "3":
			delayed_reply = stub.ChattyClientSaysHello(get_client_steam_requests())
			print("ChattyClientSaysHello Response Recieved:")
			print(delayed_reply)
		elif rpc_call == "4":
			responses = stub.InteractingHello(get_client_steam_requests())
			for response in responses:
				print("InteractingHello Response Recieved:")
				print(response)
			
			# print("Not Implemented")

if __name__ == '__main__':
	run()

