from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES

class Graph(object):
	def __init__(self, script, div, plot_resources):
		self.script = script
		self.div = div
		self.plot_resources = plot_resources

def plot_weight(animal, weights=None, start_date=None, end_date=None):
	if weights is None:
		weights = animal.weights.all()
	if start_date is None:
		start_date = min([i.date for i in weights])
	if end_date is None:
		end_date = max([i.date for i in weights])

	# X Coordinates are the dates in our range, Y coordinates are the corresponding weights
	x = []
	y = []
	# Sort the weights so the graph comes out correct
	weights.sort(key=lambda z: z.date)
	for weight in weights:
		if weight.date >= start_date and weight.date <= end_date:
			x.append(weight.date)
			y.append(weight.weight)

	fig = figure(title="%s's Weight" % animal.name, x_axis_label='Date',
				 y_axis_label='Weight (%s)' % animal.weight_units,
				 x_axis_type='datetime')
	fig.below[0].formatter.formats = dict(years=['%Y'], months=['%m/%y'], days=['%m/%d/%y'])
	fig.circle(x, y)
	fig.line(x, y)

	# Configure resources to include BokehJS inline in the document
	plot_resources = RESOURCES.render(js_raw=INLINE.js_raw, css_raw=INLINE.css_raw,
									  js_files=INLINE.js_files, css_files=INLINE.css_files)

	script, div = components(fig, INLINE)
	graph = Graph(script, div, plot_resources)
	return graph
