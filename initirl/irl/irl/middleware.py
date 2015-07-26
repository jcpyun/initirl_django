class ReferMiddleware():
	def process_request(self,request):
		ref_id = request.GET.get("ref")
		print ref_id