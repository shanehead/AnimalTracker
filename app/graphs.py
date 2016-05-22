import toyplot
import toyplot.html
import xml.etree.ElementTree

class Graph(object):
    def __init__(self, html):
        self.html = html

def plot_weight(animal, weights=None, start_date=None, end_date=None):
    if weights is None:
        weights = animal.weights.all()
    if start_date is None:
        start_date = min([i.date for i in weights])
    if end_date is None:
        end_date = max([i.date for i in weights])

    # X Coordinates are the dates in our range, Y coordinates are the corresponding weights
    x = []
    xlabels = []
    y = []
    # Sort the weights so the graph comes out correct
    weights.sort(key=lambda z: z.date)
    for weight in weights:
        if start_date <= weight.date <= end_date:
            x.append(int(weight.date.strftime('%s')))
            xlabels.append(weight.date.strftime('%m/%d/%y'))
            y.append(weight.weight)

    # TODO: Make canvas size relative to screen size or something
    canvas = toyplot.Canvas(width=400, height=600)
    axes = canvas.axes(label="%s's Weight" % animal.name, xlabel='Date',
                       ylabel='Weight (%s)' % animal.weight_units)
    axes.y.ticks.show = True
    axes.x.ticks.show = True
    axes.x.ticks.locator = toyplot.locator.Explicit(locations=x, labels=xlabels)

    axes.plot(x, y, marker='o', size=40, title='Weight')
    html = toyplot.html.render(canvas)

    graph = Graph(html=xml.etree.ElementTree.tostring(html, method='html'))
    return graph
