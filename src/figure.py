import matplotlib.pyplot as plt


class Figure:
    def __init__(self, width=15, height=7):
        self.background = "#ffffff"
        self.dot_color = "#238BC1"
        self.font_color = "#000000"

        self.default_linewidth = 1
        self.default_size = 150
        self.default_markersize = 150
        self.edge_color = "none"
        plt.figure(facecolor=self.background, figsize=(width, height))

    def scatter(self, points, color='', marker='o', alpha=1):
        """
        Draw the distribution of points.
        
        :param Points points
        :param str color
        :param str marker
        :param float alpha: 0 <= alpha <= 1
        """
        plt.xlabel("longitude", fontsize=11, color=self.font_color)
        plt.ylabel("latitude", fontsize=11, color=self.font_color)
        plt.tick_params(axis="both", which="major",
            labelsize=8, labelcolor=self.font_color)

        x_values = []
        y_values = []
        for point in points:
            x_values.append(point.longitude)
            y_values.append(point.latitude)
        plt.scatter(x_values, y_values,
                    c=color or self.dot_color,
                    s=self.default_size / (len(points) ** 0.5),
                    edgecolor=self.edge_color,
                    alpha=alpha,
                    marker=marker)
        return self

    def network(self, network, markersize, color=""):
        """
        Draw transfer network graph.
        
        :param TransferNetwork network
        :param function markersize
        :param str color
        """
        plt.xlabel("longitude", fontsize=11, color=self.font_color)
        plt.ylabel("latitude", fontsize=11, color=self.font_color)
        plt.tick_params(axis="both", which="major",
            labelsize=8, labelcolor=self.font_color)

        for i in range(len(network.edges)):
            for j in range(len(network.edges)):
                if network.edges[i][j] != -1:
                    x1, x2 = network.nodes[i].longitude, network.nodes[j].longitude
                    y1, y2 = network.nodes[i].latitude, network.nodes[j].latitude
                    plt.plot([x1, x2], [y1, y2], '-s',
                        color=color or self.dot_color,
                        linewidth=self.default_linewidth,
                        markersize=markersize(network))
        return self

    def scatter_and_network(self, points, network, cluster_points=[]):
        """
        Draw points distribution graph and transfer network graph on the 
        same figure.

        :param Points points
        :param TransferNetwork network
        :param list cluster_points
        """
        plt.subplot(121, facecolor=self.background)
        plt.title("Trajectory Points", fontsize=16, color=self.font_color)
        self.scatter(points)
        self.scatter(cluster_points, color="red")

        plt.subplot(122, facecolor=self.background)
        plt.title("Transfer Network", fontsize=16, color=self.font_color)
        self.scatter(points, color="#238BC1")        
        self.network(network, markersize=self.__markersize, color="#DC143C")

        return self

    def transfer_probability(self, network, d):
        """
        Draw the distribution of transfer probability with respect to
        the given destination.

        The transfer node size on the figure is positively related to 
        its transfer probability to destination node d.

        :param TransferNetwork network
        :param int d: destination node index
        """
        plt.title("Distribution of Transfer Probability", fontsize=16, color=self.font_color)
        self.network(network, markersize=lambda x: 1)

        vector = network.nodes[d].vector
        for index, node in enumerate(network.nodes):
            if index == d:
                color = "#DC143C"
                size = 1
            else:
                color = self.dot_color
                size = vector[index] if index < d else vector[index - 1]
            plt.scatter(node.longitude, node.latitude, c=color,
                edgecolor=self.edge_color, alpha=1, marker='s', s=size * 100)
        return self

    def most_popular_route(self, points, network, route):
        """
        Draw the most popular route.

        :param Points points
        :param TransferNetwork network
        :param list route
        """
        plt.subplot(121, facecolor=self.background)
        plt.title("Transfer Network", fontsize=16, color=self.font_color)
        self.scatter(points, color="#238BC1")        
        self.network(network, markersize=self.__markersize, color="#DC143C")

        plt.subplot(122, facecolor=self.background)
        plt.title("Most Popular Route", fontsize=16, color=self.font_color)
        self.scatter(points, color="#ffffff")
        self.network(network, markersize=self.__markersize, color="#555555")
        for i in range(len(route) - 1):
            x1 = network.nodes[route[i]].longitude
            x2 = network.nodes[route[i+1]].longitude
            y1 = network.nodes[route[i]].latitude
            y2 = network.nodes[route[i+1]].latitude
            plt.plot([x1, x2], [y1, y2], '-s', color="#DC143C",
                linewidth=2.5, markersize=7)
        return self

    def show(self):
        """
        Show figure on screen.
        """
        plt.show()
        return self

    def save(self, output_path="out"):
        """
        Save figure to the given output path.
        """
        plt.savefig('{}\\analysis.png'.format(output_path),
            facecolor=self.background)
        return self

    def __markersize(self, network):
        """
        Calculate the marker size.
        """
        markersize = self.default_markersize / len(network.nodes)
        markersize = markersize if markersize < 6 else 6
        markersize = markersize if markersize > 3 else 3
        return markersize
