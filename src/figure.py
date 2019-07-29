import matplotlib.pyplot as plt


class Figure:
    def __init__(self, theme="light", width=15, height=7):
        if theme == "dark":
            # dark theme
            self.background = "#2A323D"
            self.dot_color = "#DC143C"
            self.font_color = "#ffffff"
        else:
            # light theme
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
        Draw points distribution graph.
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

    def network(self, network, color=""):
        """
        Draw transfer network graph.
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
                    markersize = self.default_markersize / len(network.nodes)
                    markersize = markersize if markersize < 6 else 6
                    markersize = markersize if markersize > 3 else 3
                    plt.plot([x1, x2], [y1, y2],
                        '-s',
                        color=color or self.dot_color,
                        linewidth=self.default_linewidth,
                        markersize=markersize)
        return self

    def scatter_and_network(self, points, network, cluster_points=[]):
        """
        Draw points distribution graph and transfer network graph on the 
        same figure.
        """
        plt.subplot(121, facecolor=self.background)
        plt.title("Trajectory Points", fontsize=16, color=self.font_color)
        self.scatter(points)
        self.scatter(cluster_points, color="red")

        plt.subplot(122, facecolor=self.background)
        plt.title("Transfer Network", fontsize=16, color=self.font_color)
        self.scatter(points, color="#238BC1")        
        self.network(network, color="#DC143C")

        return self

    def most_popular_route(self, points, network, route):
        plt.subplot(121, facecolor=self.background)
        plt.title("Transfer Network", fontsize=16, color=self.font_color)
        self.scatter(points, color="#238BC1")        
        self.network(network, color="#DC143C")

        plt.subplot(122, facecolor=self.background)
        plt.title("Most Popular Route", fontsize=16, color=self.font_color)
        self.scatter(points, color="#ffffff")
        self.network(network, color="#555555")
        for i in range(len(route) - 1):
            x1 = network.nodes[route[i]].longitude
            x2 = network.nodes[route[i+1]].longitude
            y1 = network.nodes[route[i]].latitude
            y2 = network.nodes[route[i+1]].latitude
            plt.plot([x1, x2], [y1, y2], '-s', color="#DC143C",
                linewidth=2.5, markersize=7)
        return self

    def show(self):
        plt.show()
        return self

    def save(self, output_path="out"):
        plt.savefig('{}\\analysis.png'.format(output_path),
            facecolor=self.background)
        return self