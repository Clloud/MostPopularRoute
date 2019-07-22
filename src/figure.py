import matplotlib.pyplot as plt


class Figure:
    def __init__(self, theme="light"):
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
        plt.figure(facecolor=self.background, figsize=(15, 7))

    def scatter(self, points, color='', marker='o', alpha=1):
        # draw points distribution graph
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
        # draw transfer network graph
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
        # draw points distribution graph and transfer network graph on the same figure
        plt.subplot(121, facecolor=self.background)
        plt.title("Trajectory Points", fontsize=16, color=self.font_color)
        self.scatter(points)
        self.scatter(cluster_points, color="red")

        plt.subplot(122, facecolor=self.background)
        plt.title("Transfer Network", fontsize=16, color=self.font_color)
        self.scatter(points, color="#238BC1")        
        self.network(network, color="#DC143C")

        return self

    def show(self):
        plt.show()
        return self

    def save(self, output_path="out"):
        plt.savefig('{}\\analysis.png'.format(output_path),
            facecolor=self.background)
        return self