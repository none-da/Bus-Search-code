from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.view import view_config
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from sqlalchemy import create_engine
from busroutes import BusRoute
from busroutes import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config
from server import get_session

@view_config(route_name='home', renderer='templates.pt')
def home_view(request):
    return Response('<h1><p>Welcome</p></h1>')

@view_config(route_name='bus')
def form_view(request):
	result = render('templates.pt',
	                {'start_point':'Majestic','end_point':'Uttarahalli','route':'Chamrajpet Lalbagh'},
	                request=request)
	response = Response(result)
	return response

@view_config(route_name='response', renderer='templates.pt')
def fetch_bus_info(request):
	bus_no = request.params.get('bus_no','')
	assert bus_no, 'Keyword expected as bus_no. Got nothing instead'
	engine = create_engine('sqlite:///buses.db', echo=True)
	Session = get_session(engine)
	results = Session.query(BusRoute).filter(BusRoute.bus_no==bus_no)
	if results.count():
		bus_route = results.one()
		return Response("Starting:{0}<br/>Ending:{1}<br/>Route Info:{2}".format(bus_route.start_point, bus_route.end_point, bus_route.route))
	return Response("Invalid Bus No:%s" % bus_no)
