from django.shortcuts import redirect

def redirect_actions(request):
	return redirect('action_url', permanent=True)
