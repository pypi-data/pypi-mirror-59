# -*- coding: utf-8 -*-
import ipywidgets as widgets
import traitlets
import numpy as np
import threading

from ..models import JobComputeError
from ..types import Image

from .map_ import Map
from .layer import WorkflowsLayer


initial_width = widgets.Layout(width="initial")
scale_width = widgets.Layout(min_width="1.3em", max_width="4em", width="initial")
button_layout = widgets.Layout(width="initial", overflow="visible")


class CText(widgets.Text):
    value = traitlets.CUnicode(help="String value", allow_none=True).tag(sync=True)


class LayerControllerRow(widgets.Box):
    """
    Widget for the controls of a single `WorkflowsLayer` on a single `Map`.

    Provides controls for visbility, opacity, scales, colormaps, autoscaling,
    and order/deletion on the map.

    Attributes
    ----------
    map: Map
        The map on which `layer` is displayed.
    layer: WorkflowsLayer
        The layer this widget is controlling.
    scaleable: Bool, default True
        Whether to show controls for scaling
    autoscaleable: Bool, default True
        Whether to show the button for autoscaling
    colormappable: Bool, default True
        Whether to show controls for selecting the colormap
    checkerboardable: Bool, default True
        Whether to show controls for toggling checkerboards for transparent/missing data
    """

    map = traitlets.Instance(Map)
    layer = traitlets.Instance(WorkflowsLayer)

    scaleable = traitlets.Bool(True)
    autoscaleable = traitlets.Bool(True)
    colormappable = traitlets.Bool(True)
    checkerboardable = traitlets.Bool(True)

    _colormap_legends = {}  # cache of pre-rendered colormap legends

    def __init__(self, layer, map):
        if layer.error_output is None:
            layer.error_output = map.error_log

        self.layer = layer
        self.map = map
        self._widgets = {}

        visible = widgets.Checkbox(
            value=layer.visible, layout=initial_width, indent=False
        )
        widgets.jslink((visible, "value"), (layer, "visible"))
        self._widgets["visible"] = visible

        opacity = widgets.FloatSlider(
            value=layer.opacity,
            min=0,
            max=1,
            step=0.01,
            continuous_update=True,
            readout=False,
            layout=widgets.Layout(max_width="50px", min_width="20px"),
        )
        widgets.jslink((opacity, "value"), (layer, "opacity"))
        self._widgets["opacity"] = opacity

        name = widgets.Text(
            value=layer.name,
            placeholder="Layer name",
            layout=widgets.Layout(min_width="4em", max_width="12em"),
        )
        widgets.jslink((name, "value"), (layer, "name"))
        self._widgets["name"] = name

        r_min = CText(placeholder="r min", value=layer.r_min, layout=scale_width)
        widgets.link((r_min, "value"), (layer, "r_min"))
        r_max = CText(placeholder="r max", value=layer.r_max, layout=scale_width)
        widgets.link((r_max, "value"), (layer, "r_max"))
        g_min = CText(placeholder="g min", value=layer.g_min, layout=scale_width)
        widgets.link((g_min, "value"), (layer, "g_min"))
        g_max = CText(placeholder="g max", value=layer.g_max, layout=scale_width)
        widgets.link((g_max, "value"), (layer, "g_max"))
        b_min = CText(placeholder="b min", value=layer.b_min, layout=scale_width)
        widgets.link((b_min, "value"), (layer, "b_min"))
        b_max = CText(placeholder="b max", value=layer.b_max, layout=scale_width)
        widgets.link((b_max, "value"), (layer, "b_max"))

        self._widgets["scales"] = [r_min, r_max, g_min, g_max, b_min, b_max]

        colormap = widgets.Dropdown(
            options=[None] + Image._colormaps,
            value=layer.colormap,
            layout=widgets.Layout(width="initial", max_width="10.6em"),
        )
        widgets.link((colormap, "value"), (layer, "colormap"))
        colormap.observe(self._observe_supported_controls, names="value")
        # ^ if colormap is set/unset from None, we need to re-render controls
        self._widgets["colormap"] = colormap

        # when using a colormap display 'min' and 'max' placeholders but link
        # to r_min and r_max
        cmap_min = CText(placeholder="min", value=layer.r_min, layout=scale_width)
        widgets.link((cmap_min, "value"), (layer, "r_min"))
        cmap_max = CText(placeholder="max", value=layer.r_max, layout=scale_width)
        widgets.link((cmap_max, "value"), (layer, "r_max"))

        if get_matplotlib() is not None:
            legend = widgets.Image(
                format="png",
                layout=widgets.Layout(
                    display="none",
                    height="var(--jp-widgets-inline-height)",
                    max_width="8.3em",  # ~width of 2 input boxes
                ),
            )
            self._widgets["cmap_legend"] = legend
            self._widgets["cmap_scales"] = [cmap_min, legend, cmap_max]

            colormap.observe(
                self._observe_colormap_make_legend, names="value", type="change"
            )
            self._observe_colormap_make_legend({})  # initialize colormap
        else:
            self._widgets["cmap_scales"] = [cmap_min, cmap_max]

        checkerboard = widgets.ToggleButton(
            value=layer.checkerboard,
            description="",
            tooltip="Checkerboard missing data",
            icon="th",
            layout=button_layout,
        )
        widgets.link((checkerboard, "value"), (layer, "checkerboard"))
        self._widgets["checkerboard"] = checkerboard

        autoscale = widgets.Button(
            description="", tooltip="Autoscale", icon="magic", layout=button_layout
        )
        autoscale.on_click(self.autoscale)
        self._widgets["autoscale"] = autoscale

        move_up = widgets.Button(
            description=u"↑", tooltip="Move layer up", layout=button_layout
        )
        move_up.on_click(self.move_up)
        self._widgets["move_up"] = move_up

        move_down = widgets.Button(
            description=u"↓", tooltip="Move layer down", layout=button_layout
        )
        move_down.on_click(self.move_down)
        self._widgets["move_down"] = move_down

        remove = widgets.Button(
            description=u"✖︎", tooltip="Remove layer", layout=button_layout
        )
        remove.on_click(self.remove)
        self._widgets["remove"] = remove

        super(LayerControllerRow, self).__init__(self._make_children())

        self.layout.overflow = "initial"

    def _scale_observer(self, scale):
        def _observer(change):
            try:
                setattr(self.layer, scale, float(change["new"]))
            except ValueError:
                pass

        return _observer

    def _make_children(self):
        widgets = self._widgets
        children = [widgets["visible"], widgets["opacity"], widgets["name"]]

        if self.scaleable:
            if self.layer.colormap is None:
                children.extend(widgets["scales"])
            else:
                children.extend(widgets["cmap_scales"])
        if self.colormappable:
            children.append(widgets["colormap"])
            widgets["colormap"].layout.width = (
                "2.1em" if self.layer.colormap is None else ""
            )
        if self.checkerboardable:
            children.append(widgets["checkerboard"])
        if self.autoscaleable:
            children.append(widgets["autoscale"])

        children += [widgets["move_up"], widgets["move_down"], widgets["remove"]]

        return children

    @traitlets.observe(
        "autoscaleable", "colormappable", "scaleable", "checkerboardable"
    )
    def _observe_supported_controls(self, change):
        self.children = self._make_children()

    def _observe_colormap_make_legend(self, change):
        "use matplotlib (if available) to render a colorbar for the current colormap"
        colormap = self.layer.colormap
        legend = self._widgets["cmap_legend"]
        if colormap is None:
            png = b""
        else:
            try:
                png = self._colormap_legends[colormap]
            except KeyError:
                png = colorbar_png(colormap)
                if png is None:
                    png = b""
                self._colormap_legends[colormap] = png

        legend.layout.display = "none" if len(png) == 0 else ""
        legend.value = png

    def _autoscale(self, widget):
        old_icon = widget.icon
        widget.icon = "spinner"
        widget.disabled = True

        ctx = self.map.geocontext()
        try:
            params = self.layer.parameters.to_dict()
        except AttributeError:
            # technically, parameters is allowed to be None
            params = {}

        try:
            # clear any existing outputs (e.g. from a previous failed autoscale)
            if self.layer.autoscale_progress.outputs:
                self.layer.autoscale_progress.set_output(())

            result = self.layer.image.compute(
                ctx, progress_bar=self.layer.autoscale_progress, **params
            )

        except JobComputeError as e:
            self.layer.autoscale_progress.append_stdout("\n" + e.message)
        else:
            # clear the output widget if the job succeeded
            self.layer.autoscale_progress.set_output(())

            arr = result.ndarray

            scales_attrs = [("r_min", "r_max"), ("g_min", "g_max"), ("b_min", "b_max")]

            with self.layer.hold_trait_notifications():
                # for a single-band array, only set r_min and r_max
                for band, (scale_min, scale_max) in zip(arr, scales_attrs):
                    if isinstance(band, np.ma.MaskedArray):
                        data = band.compressed()  # drop masked data
                    min, max = np.percentile(data, [2, 98])

                    setattr(self.layer, scale_min, min)
                    setattr(self.layer, scale_max, max)
        finally:
            widget.icon = old_icon
            widget.disabled = False

    def autoscale(self, widget):
        "``on_click`` handler to perform autoscaling."
        thread = threading.Thread(target=self._autoscale, args=(widget,), daemon=True)
        thread.start()

    def move_up(self, _):
        "``on_click`` handler to move ``self.layer`` up on ``self.map``"
        self.map.move_layer_up(self.layer)

    def move_down(self, _):
        "``on_click`` handler to move ``self.layer`` down on ``self.map``"
        self.map.move_layer_down(self.layer)

    def remove(self, _):
        "``on_click`` handler to remove ``self.layer`` from ``self.map``"
        if self.layer.error_output is self.map.error_log:
            # stops the error listener
            self.layer.error_output = None
        self.map.remove_layer(self.layer)


def get_matplotlib():
    try:
        import matplotlib.pyplot

        return matplotlib
    except Exception:
        return None


def colorbar_png(colormap_name, figsize=(2.5, 0.5)):
    """
    Render a matplotlib colorbar for the named colormap

    Returns a PNG as bytes, or None if matplotlib or the colormap is unavailable.
    """
    matplotlib = get_matplotlib()
    if matplotlib is None:
        return None

    fig = matplotlib.figure.Figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    try:
        cmap = matplotlib.cm.get_cmap(colormap_name)
    except ValueError:
        return None

    matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, orientation="horizontal")

    # we use the matplotlib's object-oriented API instead of pyplot,
    # and manually connect the `agg` backend, in order to not mess
    # with any configuration a user might have made
    matplotlib.backends.backend_agg.FigureCanvasAgg(fig)

    import io

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")

    return buffer.getvalue()
