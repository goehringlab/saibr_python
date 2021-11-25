import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from .funcs import spline_roi

"""
This no longer works with multiple channels - intensity ranges
Need a version that works in notebooks
Ability to specify a directory and open all channels. Or an nd file

"""


class ROI:
    """
    Instructions:
    - click to lay down points
    - backspace at any time to remove last point
    - press enter to select area (if spline=True will fit spline to points, otherwise will fit straight lines)
    - at this point can press backspace to go back to laying points
    - press enter again to close and return ROI

    :param img: input image
    :param spline: if true, fits spline to inputted coordinates
    :return: cell boundary coordinates
    """

    def __init__(self, img, spline=True, start_frame=0, end_frame=None, periodic=True, show_fit=True):

        # Detect if single frame or stack
        if type(img) is list:
            self.stack = True
            self.images = img

        elif len(img.shape) == 3:
            self.stack = True
            self.images = list(img)
        else:
            self.stack = False
            self.images = [img, ]

        # Params
        self.spline = spline
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.periodic = periodic
        self.show_fit = show_fit

        # Internal
        self._current_frame = self.start_frame
        self._current_image = 0
        self._point0 = None
        self._points = None
        self._line = None
        self._fitted = False

        # Specify vlim
        self.vmax = max([np.max(i) for i in self.images])
        self.vmin = min([np.min(i) for i in self.images])

        # Outputs
        self.xpoints = []
        self.ypoints = []
        self.roi = None

    def run(self):
        # Set up figure
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.fig.canvas.mpl_connect('button_press_event', self.button_press_callback)
        self.fig.canvas.mpl_connect('key_press_event', self.key_press_callback)

        # Stack
        if self.stack:
            plt.subplots_adjust(left=0.25, bottom=0.25)
            self.axframe = plt.axes([0.25, 0.1, 0.65, 0.03])
            if self.end_frame is None:
                self.end_frame = len(self.images)
            self.sframe = Slider(self.axframe, 'Frame', self.start_frame, self.end_frame, valinit=self.start_frame,
                                 valfmt='%d')
            self.sframe.on_changed(self.draw_frame)

        self.draw_frame(self.start_frame)

        # Show figure
        self.fig.canvas.set_window_title('Specify ROI')
        self.fig.canvas.mpl_connect('close_event', lambda event: self.fig.canvas.stop_event_loop())
        self.fig.canvas.start_event_loop(timeout=-1)

    def draw_frame(self, i):
        self._current_frame = i
        self.ax.clear()

        # Plot image
        self.ax.imshow(self.images[int(i)], cmap='gray', vmin=self.vmin, vmax=self.vmax)

        # Finalise figure
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.text(0.03, 0.97,
                     'Specify ROI clockwise (4 points minimum)'
                     '\nClick to lay points'
                     '\nBACKSPACE: undo'
                     '\nENTER: Save and continue',
                     color='white',
                     transform=self.ax.transAxes, fontsize=8, va='top', ha='left')
        self.display_points()
        self.fig.canvas.draw()

    def button_press_callback(self, event):
        if not self._fitted:
            if isinstance(event.inaxes, type(self.ax)):
                # Add points to list
                self.xpoints.extend([event.xdata])
                self.ypoints.extend([event.ydata])

                # Display points
                self.display_points()
                self.fig.canvas.draw()

    def key_press_callback(self, event):
        if event.key == 'backspace':
            if not self._fitted:
                # Remove last drawn point
                if len(self.xpoints) != 0:
                    self.xpoints = self.xpoints[:-1]
                    self.ypoints = self.ypoints[:-1]
                self.display_points()
                self.fig.canvas.draw()
            else:
                # Remove line
                self._fitted = False
                self._line.pop(0).remove()
                self.roi = None
                self.fig.canvas.draw()

        if event.key == 'enter':
            if len(self.xpoints) != 0:
                roi = np.vstack((self.xpoints, self.ypoints)).T

                # Spline
                if self.spline:
                    if not self._fitted:
                        self.roi = spline_roi(roi, periodic=self.periodic)
                        self._fitted = True

                        # Display line
                        if self.show_fit:
                            self._line = self.ax.plot(self.roi[:, 0], self.roi[:, 1], c='b')
                            self.fig.canvas.draw()
                        else:
                            plt.close(self.fig)
                    else:
                        plt.close(self.fig)
                else:
                    self.roi = roi
                    plt.close(self.fig)
            else:
                self.roi = []
                plt.close(self.fig)

        if event.key == ',':
            self._current_image = max(0, self._current_image - 1)
            self.draw_frame(self._current_frame)

        if event.key == '.':
            self._current_image = min(len(self.images) - 1, self._current_image + 1)
            self.draw_frame(self._current_frame)

    def display_points(self):
        # Remove existing points
        try:
            self._point0.remove()
            self._points.remove()
        except (ValueError, AttributeError) as error:
            pass

        # Plot all points
        if len(self.xpoints) != 0:
            self._points = self.ax.scatter(self.xpoints, self.ypoints, c='lime', s=10)
            self._point0 = self.ax.scatter(self.xpoints[0], self.ypoints[0], c='r', s=10)


def def_roi(stack, spline=True, start_frame=0, end_frame=None, periodic=True, show_fit=True):
    r = ROI(stack, spline=spline, start_frame=start_frame, end_frame=end_frame, periodic=periodic, show_fit=show_fit)
    r.run()
    return r.roi
