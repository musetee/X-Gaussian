from eval_point_cloud_vis import readply
def scatter_plot3d(x, y, z, opacity):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    '''x = np.random.rand(100)
    y = np.random.rand(100)
    z = np.random.rand(100)
    opacity = np.random.rand(100)'''
    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot with opacity
    sc = ax.scatter(x, y, z, c=opacity, cmap='viridis', alpha=0.8)

    # Add a color bar to show opacity scale
    plt.colorbar(sc, label='Opacity')

    plt.show()

def scatter3d_plot():
    import plotly.graph_objs as go
    import numpy as np

    # Sample data
    x = np.random.rand(100)
    y = np.random.rand(100)
    z = np.random.rand(100)
    opacity = np.random.rand(100)

    # Creating the 3D scatter plot
    trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=5,
            color=opacity,   # Opacity determines color intensity
            colorscale='Viridis',
            opacity=0.8      # General opacity control
        )
    )

    data = [trace]
    layout = go.Layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()

def pythreejs_plot():
    import pythreejs as three
    import numpy as np
    import ipywidgets as widgets

    # Sample data
    x = np.random.rand(100)
    y = np.random.rand(100)
    z = np.random.rand(100)
    opacity = np.random.rand(100)

    # Create geometry and material
    geometry = three.BufferGeometry(
        attributes={
            'position': three.BufferAttribute(np.column_stack((x, y, z)), normalized=False),
            'color': three.BufferAttribute(np.random.rand(100, 3), normalized=True),
        }
    )

    material = three.PointsMaterial(size=5, vertexColors='VertexColors', transparent=True, opacity=0.8)

    # Create points
    points = three.Points(geometry=geometry, material=material)

    # Create scene, camera, and renderer
    camera = three.PerspectiveCamera(position=[1, 1, 1], aspect=800/600)
    scene = three.Scene(children=[points, camera])

    renderer = three.Renderer(camera=camera, scene=scene, controls=[three.OrbitControls(controlling=camera)], width=800, height=600)

    # Display the 3D plot
    widgets.VBox([renderer])

if __name__=='__main__':
    path = r'data/foot.ply'
    xyz, opacities,xyz_and_opacities=readply(path)
    x = xyz[:,0]
    y = xyz[:,1]
    z = xyz[:,2]
    scatter_plot3d(x,y,z,opacities)