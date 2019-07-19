import matplotlib.pyplot as plt


class Figure:
    face_color = (42/255, 50/255, 61/255)
    size = 10
    color = (253/255, 10/255, 0/255)
    edge_color = "none"

    def scatter(self, points):
        x_values = [point.longitude for point in points]
        y_values = [point.latitude for point in points]

        plt.figure(facecolor=self.face_color, figsize=(8, 7))
        plt.title("Trajectory Points", fontsize=16, color="white")
        plt.xlabel("longitude", fontsize=11, color="white")
        plt.ylabel("latitude", fontsize=11, color="white")
        plt.tick_params(axis="both", which="major",
                        labelsize=8, labelcolor="white")
        plt.scatter(x_values, y_values,
                    c=self.color, s=self.size, edgecolor=self.edge_color, alpha=0.8)
        return self

    def transfer_network(self, points, network):
        return self

    def show(self):
        plt.savefig('Trajectories.png',
            facecolor=self.face_color, transparent=True)
        plt.show()
