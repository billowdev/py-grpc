from concurrent import futures
import time

import grpc
import greet_pb2
import greet_pb2_grpc

class GreeterServicer(greet_pb2_grpc.GreeterServicer):
	def SayHello(self, request, ctx):
		print("SayHello Request Made:")
		print(request)
		hello_reply = greet_pb2.HelloReply()
		hello_reply.message = f"{request.greeting} {request.name}"

		return hello_reply

	def ParrotSaysHello(self, request, ctx):
		print("ParrotSayHello Request Made:")
		print(request)
		for i in range(3):
			hello_reply = greet_pb2.HelloReply()
			hello_reply.message = f"{request.greeting} {request.name} {i + 1}"
			yield hello_reply
			time.sleep(3)
		# return super().ParrotSayHello(request, ctx)

	def ChattyClientSaysHello(self, request_iterator, ctx):
		delayed_reply = greet_pb2.DelayedReply()
		for request in request_iterator:
			print("ChattyClientSayHello Request Made:")
			print(request)
			delayed_reply.message = f"You have send {len(delayed_reply.request)} message. Please expected a delayed response."
		return delayed_reply
		# return super().ChattyClientSaysHello(request_iterator, ctx)

	def InteractingHello(self, request_iterator, ctx):
		for request in request_iterator:
			print("InteractingHello Request Made:")
			print(request)
			hello_reply = greet_pb2.HelloReply()
			hello_reply.message = f"{request.greeting} {request.name}"

			yield hello_reply
		# return super().IteractingHello(request_iterator, ctx)

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
	server.add_insecure_port("localhost:5000")
	server.start()
	server.wait_for_termination()
 
if __name__ == "__main__":
	print("Starting gRPC server...")
	serve()


