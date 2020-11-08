import datetime as dt
import logging
from math import cos, pi, sin

import cairo
from numpy.random import default_rng

from genart.cairo_util import operator, source
from genart.color import Color, LinearGradient, RadialGradient
from genart.geom import points_along_arc
from genart.util import parse_size

log = logging.getLogger(__name__)


def register_parser(subparsers):
    parser = subparsers.add_parser("selene", help="O Chaire Selene")

    parser.add_argument("-s", "--size", default="500x500")
    parser.add_argument("--seed", type=int)

    parser.set_defaults(func=main)


def main(args, config):
    width, height = parse_size(args.size)
    rng = default_rng(args.seed)

    out_file = config["output_dir"] / f"selene_{dt.datetime.now().isoformat()}.svg"
    surface = cairo.SVGSurface(str(out_file), width, height)
    ctx = cairo.Context(surface)

    bg = RadialGradient([Color(0.7, 0.7, 0.7), Color(0.2, 0.2, 0.2)])
    with source(ctx, bg.to_pattern(width / 2, height / 2, width / 2)):
        ctx.paint()

    draw_crown(ctx, width / 2, height / 3, width / 10)

    n_moons = rng.integers(6, 12)
    for i, (x, y) in enumerate(
        points_along_arc(width / 2, height / 2, width / 2.8, 0, 2 * pi, n_moons)
    ):
        pct_done = i / n_moons
        eclipse_pct = (pct_done * 2.0) - 1.0
        draw_moon(ctx, x, y, width / (1.2 * n_moons), eclipse_pct)

    draw_circular_calendar(ctx, width / 2, height / 2, width / 4)

    surface.finish()


def draw_moon(
    ctx: cairo.Context,
    pos_x: float,
    pos_y: float,
    radius: float,
    eclipse_pct: float = -1.0,
):
    moon_color = LinearGradient([Color(0.2, 0.2, 0.2), Color(0.7, 0.7, 0.7)])
    with source(
        ctx, moon_color.to_pattern(pos_x - radius, pos_y + radius, pos_x, pos_y)
    ):
        ctx.arc(pos_x, pos_y, radius, 0, 2 * pi)
        ctx.fill_preserve()
        ctx.clip()

    # crater_color = RadialGradient([Color(0.7, 0.7, 0.7), Color(0.2, 0.2, 0.2)])
    # crater_radius = radius / 10.0
    # with source(
    #     ctx,
    #     crater_color.to_pattern(pos_x, pos_y, crater_radius, crater_radius * 0.7),
    # ), operator(ctx, cairo.Operator.DARKEN):
    #     ctx.arc(pos_x, pos_y, crater_radius, 0, 2 * pi)
    #     ctx.fill()

    with source(ctx, Color(0.0, 0.0, 0.0).to_pattern()):
        eclipse_cx = pos_x + eclipse_pct * 2.0 * radius
        ctx.arc(eclipse_cx, pos_y, radius, 0, 2 * pi)
        ctx.fill()
        ctx.reset_clip()


def draw_crown(ctx: cairo.Context, pos_x: float, pos_y: float, radius: float):
    ctx.arc(pos_x, pos_y, radius, 0, 2 * pi)
    ctx.stroke_preserve()
    ctx.clip()

    crown_eclipse = -0.2

    eclipse_cy = pos_y + crown_eclipse * 2.0 * radius
    ctx.arc(pos_x, eclipse_cy, radius, 0, 2 * pi)
    ctx.fill()
    ctx.reset_clip()


def draw_circular_calendar(
    ctx: cairo.Context, pos_x: float, pos_y: float, radius: float, chunks: int = 12
):
    ctx.arc(pos_x, pos_y, radius, 0, 2 * pi)
    ctx.stroke_preserve()

    ctx.arc(pos_x, pos_y, 0.9 * radius, 0, 2 * pi)
    ctx.stroke()

    for (start_x, start_y), (end_x, end_y) in zip(
        points_along_arc(pos_x, pos_y, 0.9 * radius, 0, 2 * pi, chunks),
        points_along_arc(pos_x, pos_y, radius, 0, 2 * pi, chunks),
    ):
        ctx.move_to(start_x, start_y)
        ctx.line_to(end_x, end_y)
        ctx.stroke()
