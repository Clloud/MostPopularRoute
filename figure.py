import matplotlib.pyplot as plt


class Figure:
    face_color = (42/255, 50/255, 61/255)
    size = 2
    color = (253/255, 10/255, 0/255)
    edge_color = "none"

    @classmethod
    def scatter(cls, points):
        x_values = [point.longitude for point in points]
        y_values = [point.latitude for point in points]

        plt.figure(facecolor=cls.face_color, figsize=(8, 7))
        plt.title("Trajectory Points", fontsize=16, color="white")
        plt.xlabel("latitude", fontsize=11, color="white")
        plt.ylabel("longitude", fontsize=11, color="white")
        plt.tick_params(axis="both", which="major",
                        labelsize=8, labelcolor="white")
        plt.scatter(x_values, y_values,
                    c=cls.color, s=cls.size, edgecolor=cls.edge_color, alpha=0.8)
        plt.savefig('Trajectories.png',
                    facecolor=cls.face_color, transparent=True)
        plt.show()
