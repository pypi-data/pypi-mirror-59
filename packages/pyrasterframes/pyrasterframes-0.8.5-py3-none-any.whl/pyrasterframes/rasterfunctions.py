#
# This software is licensed under the Apache 2 license, quoted below.
#
# Copyright 2019 Astraea, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# [http://www.apache.org/licenses/LICENSE-2.0]
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# SPDX-License-Identifier: Apache-2.0
#

"""
This module creates explicit Python functions that map back to the existing Scala
implementations. Most functions are standard Column functions, but those with unique
signatures are handled here as well.
"""
from __future__ import absolute_import
from pyspark.sql.column import Column, _to_java_column
from pyspark.sql.functions import lit
from .rf_context import RFContext
from .rf_types import CellType, Extent, CRS

THIS_MODULE = 'pyrasterframes'


def _context_call(name, *args):
    f = RFContext.active().lookup(name)
    return f(*args)


def _parse_cell_type(cell_type_arg):
    """ Convert the cell type representation to the expected JVM CellType object."""

    def to_jvm(ct):
        return _context_call('_parse_cell_type', ct)

    if isinstance(cell_type_arg, str):
        return to_jvm(cell_type_arg)
    elif isinstance(cell_type_arg, CellType):
        return to_jvm(cell_type_arg.cell_type_name)


def rf_cell_types():
    """Return a list of standard cell types"""
    return [CellType(str(ct)) for ct in _context_call('rf_cell_types')]


def rf_assemble_tile(col_index, row_index, cell_data_col, num_cols, num_rows, cell_type=None):
    """Create a Tile from  a column of cell data with location indices"""
    jfcn = RFContext.active().lookup('rf_assemble_tile')

    if isinstance(num_cols, Column):
        num_cols = _to_java_column(num_cols)

    if isinstance(num_rows, Column):
        num_rows = _to_java_column(num_rows)

    if cell_type is None:
        return Column(jfcn(
            _to_java_column(col_index), _to_java_column(row_index), _to_java_column(cell_data_col),
            num_cols, num_rows
        ))

    else:
        return Column(jfcn(
            _to_java_column(col_index), _to_java_column(row_index), _to_java_column(cell_data_col),
            num_cols, num_rows, _parse_cell_type(cell_type)
        ))

def rf_array_to_tile(array_col, num_cols, num_rows):
    """Convert array in `array_col` into a Tile of dimensions `num_cols` and `num_rows'"""
    jfcn = RFContext.active().lookup('rf_array_to_tile')
    return Column(jfcn(_to_java_column(array_col), num_cols, num_rows))


def rf_convert_cell_type(tile_col, cell_type):
    """Convert the numeric type of the Tiles in `tileCol`"""
    jfcn = RFContext.active().lookup('rf_convert_cell_type')
    return Column(jfcn(_to_java_column(tile_col), _parse_cell_type(cell_type)))

def rf_interpret_cell_type_as(tile_col, cell_type):
    """Change the interpretation of the tile_col's cell values according to specified cell_type"""
    jfcn = RFContext.active().lookup('rf_interpret_cell_type_as')
    return Column(jfcn(_to_java_column(tile_col), _parse_cell_type(cell_type)))


def rf_make_constant_tile(scalar_value, num_cols, num_rows, cell_type=CellType.float64()):
    """Constructor for constant tile column"""
    jfcn = RFContext.active().lookup('rf_make_constant_tile')
    return Column(jfcn(scalar_value, num_cols, num_rows, _parse_cell_type(cell_type)))


def rf_make_zeros_tile(num_cols, num_rows, cell_type=CellType.float64()):
    """Create column of constant tiles of zero"""
    jfcn = RFContext.active().lookup('rf_make_zeros_tile')
    return Column(jfcn(num_cols, num_rows, _parse_cell_type(cell_type)))


def rf_make_ones_tile(num_cols, num_rows, cell_type=CellType.float64()):
    """Create column of constant tiles of one"""
    jfcn = RFContext.active().lookup('rf_make_ones_tile')
    return Column(jfcn(num_cols, num_rows, _parse_cell_type(cell_type)))


def rf_rasterize(geometry_col, bounds_col, value_col, num_cols_col, num_rows_col):
    """Create a tile where cells in the grid defined by cols, rows, and bounds are filled with the given value."""
    jfcn = RFContext.active().lookup('rf_rasterize')
    return Column(jfcn(_to_java_column(geometry_col), _to_java_column(bounds_col),
                       _to_java_column(value_col), _to_java_column(num_cols_col),  _to_java_column(num_rows_col)))


def st_reproject(geometry_col, src_crs, dst_crs):
    """Reproject a column of geometry given the CRSs of the source and destination."""
    jfcn = RFContext.active().lookup('st_reproject')
    return Column(jfcn(_to_java_column(geometry_col), _to_java_column(src_crs), _to_java_column(dst_crs)))


def rf_explode_tiles(*tile_cols):
    """Create a row for each cell in Tile."""
    jfcn = RFContext.active().lookup('rf_explode_tiles')
    jcols = [_to_java_column(arg) for arg in tile_cols]
    return Column(jfcn(RFContext.active().list_to_seq(jcols)))


def rf_explode_tiles_sample(sample_frac, seed, *tile_cols):
    """Create a row for a sample of cells in Tile columns."""
    jfcn = RFContext.active().lookup('rf_explode_tiles_sample')
    jcols = [_to_java_column(arg) for arg in tile_cols]
    return Column(jfcn(sample_frac, seed, RFContext.active().list_to_seq(jcols)))


def _apply_scalar_to_tile(name, tile_col, scalar):
    jfcn = RFContext.active().lookup(name)
    return Column(jfcn(_to_java_column(tile_col), scalar))


def rf_with_no_data(tile_col, scalar):
    """Assign a `NoData` value to the Tiles in the given Column."""
    return _apply_scalar_to_tile('rf_with_no_data', tile_col, scalar)


def rf_local_add_double(tile_col, scalar):
    """Add a floating point scalar to a Tile"""
    return _apply_scalar_to_tile('rf_local_add_double', tile_col, scalar)


def rf_local_add_int(tile_col, scalar):
    """Add an integral scalar to a Tile"""
    return _apply_scalar_to_tile('rf_local_add_int', tile_col, scalar)


def rf_local_subtract_double(tile_col, scalar):
    """Subtract a floating point scalar from a Tile"""
    return _apply_scalar_to_tile('rf_local_subtract_double', tile_col, scalar)


def rf_local_subtract_int(tile_col, scalar):
    """Subtract an integral scalar from a Tile"""
    return _apply_scalar_to_tile('rf_local_subtract_int', tile_col, scalar)


def rf_local_multiply_double(tile_col, scalar):
    """Multiply a Tile by a float point scalar"""
    return _apply_scalar_to_tile('rf_local_multiply_double', tile_col, scalar)


def rf_local_multiply_int(tile_col, scalar):
    """Multiply a Tile by an integral scalar"""
    return _apply_scalar_to_tile('rf_local_multiply_int', tile_col, scalar)


def rf_local_divide_double(tile_col, scalar):
    """Divide a Tile by a floating point scalar"""
    return _apply_scalar_to_tile('rf_local_divide_double', tile_col, scalar)


def rf_local_divide_int(tile_col, scalar):
    """Divide a Tile by an integral scalar"""
    return _apply_scalar_to_tile('rf_local_divide_int', tile_col, scalar)


def rf_local_less_double(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is less than a scalar, otherwise 0"""
    return _apply_scalar_to_tile('foo', tile_col, scalar)


def rf_local_less_int(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is less than a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_less_double', tile_col, scalar)


def rf_local_less_equal_double(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is less than or equal to a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_less_equal_double', tile_col, scalar)


def rf_local_less_equal_int(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is less than or equal to a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_less_equal_int', tile_col, scalar)


def rf_local_greater_double(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is greater than a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_greater_double', tile_col, scalar)


def rf_local_greater_int(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is greater than a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_greater_int', tile_col, scalar)


def rf_local_greater_equal_double(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is greater than or equal to a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_greater_equal_double', tile_col, scalar)


def rf_local_greater_equal_int(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is greater than or equal to a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_greater_equal_int', tile_col, scalar)


def rf_local_equal_double(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is equal to a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_equal_double', tile_col, scalar)


def rf_local_equal_int(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is equal to a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_equal_int', tile_col, scalar)


def rf_local_unequal_double(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is not equal to a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_unequal_double', tile_col, scalar)


def rf_local_unequal_int(tile_col, scalar):
    """Return a Tile with values equal 1 if the cell is not equal to a scalar, otherwise 0"""
    return _apply_scalar_to_tile('rf_local_unequal_int', tile_col, scalar)


def rf_local_no_data(tile_col):
    """Return a tile with ones where the input is NoData, otherwise zero."""
    return _apply_column_function('rf_local_no_data', tile_col)


def rf_local_data(tile_col):
    """Return a tile with zeros where the input is NoData, otherwise one."""
    return _apply_column_function('rf_local_data', tile_col)


def rf_local_is_in(tile_col, array):
    """Return a tile with cell values of 1 where the `tile_col` cell is in the provided array."""
    from pyspark.sql.functions import array as sql_array
    if isinstance(array, list):
        array = sql_array([lit(v) for v in array])

    return _apply_column_function('rf_local_is_in', tile_col, array)


def _apply_column_function(name, *args):
    jfcn = RFContext.active().lookup(name)
    jcols = [_to_java_column(arg) for arg in args]
    return Column(jfcn(*jcols))


def rf_dimensions(tile_col):
    """Query the number of (cols, rows) in a Tile."""
    return _apply_column_function('rf_dimensions', tile_col)


def rf_tile_to_array_int(tile_col):
    """Flattens Tile into an array of integers."""
    return _apply_column_function('rf_tile_to_array_int', tile_col)


def rf_tile_to_array_double(tile_col):
    """Flattens Tile into an array of doubles."""
    return _apply_column_function('rf_tile_to_array_double', tile_col)


def rf_cell_type(tile_col):
    """Extract the Tile's cell type"""
    return _apply_column_function('rf_cell_type', tile_col)


def rf_is_no_data_tile(tile_col):
    """Report if the Tile is entirely NODDATA cells"""
    return _apply_column_function('rf_is_no_data_tile', tile_col)


def rf_exists(tile_col):
    """Returns true if any cells in the tile are true (non-zero and not NoData)"""
    return _apply_column_function('rf_exists', tile_col)


def rf_for_all(tile_col):
    """Returns true if all cells in the tile are true (non-zero and not NoData)."""
    return _apply_column_function('rf_for_all', tile_col)


def rf_agg_approx_histogram(tile_col):
    """Compute the full column aggregate floating point histogram"""
    return _apply_column_function('rf_agg_approx_histogram', tile_col)


def rf_agg_approx_quantiles(tile_col, probabilities, relative_error=0.00001):
    """
    Calculates the approximate quantiles of a tile column of a DataFrame.

    :param tile_col: column to extract cells from.
    :param probabilities: a list of quantile probabilities. Each number must belong to [0, 1].
            For example 0 is the minimum, 0.5 is the median, 1 is the maximum.
    :param relative_error: The relative target precision to achieve (greater than or equal to 0). Default is 0.00001
    :return: An array of values approximately at the specified `probabilities`
    """

    _jfn = RFContext.active().lookup('rf_agg_approx_quantiles')
    _tile_col = _to_java_column(tile_col)
    return Column(_jfn(_tile_col, probabilities, relative_error))


def rf_agg_stats(tile_col):
    """Compute the full column aggregate floating point statistics"""
    return _apply_column_function('rf_agg_stats', tile_col)


def rf_agg_mean(tile_col):
    """Computes the column aggregate mean"""
    return _apply_column_function('rf_agg_mean', tile_col)


def rf_agg_data_cells(tile_col):
    """Computes the number of non-NoData cells in a column"""
    return _apply_column_function('rf_agg_data_cells', tile_col)


def rf_agg_no_data_cells(tile_col):
    """Computes the number of NoData cells in a column"""
    return _apply_column_function('rf_agg_no_data_cells', tile_col)


def rf_agg_extent(extent_col):
    """Compute the aggregate extent over a column"""
    return _apply_column_function('rf_agg_extent', extent_col)


def rf_agg_reprojected_extent(extent_col, src_crs_col, dest_crs):
    """Compute the aggregate extent over a column, first projecting from the row CRS to the destination CRS. """
    return Column(RFContext.call('rf_agg_reprojected_extent', _to_java_column(extent_col), _to_java_column(src_crs_col), CRS(dest_crs).__jvm__))


def rf_agg_overview_raster(tile_col: Column, cols: int, rows: int, aoi: Extent,
                           tile_extent_col: Column = None, tile_crs_col: Column = None):
    """Construct an overview raster of size `cols`x`rows` where data in `proj_raster` intersects the
    `aoi` bound box in web-mercator. Uses bi-linear sampling method."""
    ctx = RFContext.active()
    jfcn = ctx.lookup("rf_agg_overview_raster")

    if tile_extent_col is None or tile_crs_col is None:
        return Column(jfcn(_to_java_column(tile_col), cols, rows, aoi.__jvm__))
    else:
        return Column(jfcn(
            _to_java_column(tile_col), _to_java_column(tile_extent_col), _to_java_column(tile_crs_col),
            cols, rows, aoi.__jvm__
        ))


def rf_tile_histogram(tile_col):
    """Compute the Tile-wise histogram"""
    return _apply_column_function('rf_tile_histogram', tile_col)


def rf_tile_mean(tile_col):
    """Compute the Tile-wise mean"""
    return _apply_column_function('rf_tile_mean', tile_col)


def rf_tile_sum(tile_col):
    """Compute the Tile-wise sum"""
    return _apply_column_function('rf_tile_sum', tile_col)


def rf_tile_min(tile_col):
    """Compute the Tile-wise minimum"""
    return _apply_column_function('rf_tile_min', tile_col)


def rf_tile_max(tile_col):
    """Compute the Tile-wise maximum"""
    return _apply_column_function('rf_tile_max', tile_col)


def rf_tile_stats(tile_col):
    """Compute the Tile-wise floating point statistics"""
    return _apply_column_function('rf_tile_stats', tile_col)


def rf_render_ascii(tile_col):
    """Render ASCII art of tile"""
    return _apply_column_function('rf_render_ascii', tile_col)


def rf_render_matrix(tile_col):
    """Render Tile cell values as numeric values, for debugging purposes"""
    return _apply_column_function('rf_render_matrix', tile_col)


def rf_render_png(red_tile_col, green_tile_col, blue_tile_col):
    """Converts columns of tiles representing RGB channels into a PNG encoded byte array."""
    return _apply_column_function('rf_render_png', red_tile_col, green_tile_col, blue_tile_col)


def rf_render_color_ramp_png(tile_col, color_ramp_name):
    """Converts columns of tiles representing RGB channels into a PNG encoded byte array."""
    return Column(RFContext.call('rf_render_png', _to_java_column(tile_col), color_ramp_name))


def rf_rgb_composite(red_tile_col, green_tile_col, blue_tile_col):
    """Converts columns of tiles representing RGB channels into a single RGB packaged tile."""
    return _apply_column_function('rf_rgb_composite', red_tile_col, green_tile_col, blue_tile_col)


def rf_no_data_cells(tile_col):
    """Count of NODATA cells"""
    return _apply_column_function('rf_no_data_cells', tile_col)


def rf_data_cells(tile_col):
    """Count of cells with valid data"""
    return _apply_column_function('rf_data_cells', tile_col)


def rf_local_add(left_tile_col, right_tile_col):
    """Add two Tiles"""
    return _apply_column_function('rf_local_add', left_tile_col, right_tile_col)


def rf_local_subtract(left_tile_col, right_tile_col):
    """Subtract two Tiles"""
    return _apply_column_function('rf_local_subtract', left_tile_col, right_tile_col)


def rf_local_multiply(left_tile_col, right_tile_col):
    """Multiply two Tiles"""
    return _apply_column_function('rf_local_multiply', left_tile_col, right_tile_col)


def rf_local_divide(left_tile_col, right_tile_col):
    """Divide two Tiles"""
    return _apply_column_function('rf_local_divide', left_tile_col, right_tile_col)


def rf_normalized_difference(left_tile_col, right_tile_col):
    """Compute the normalized difference of two tiles"""
    return _apply_column_function('rf_normalized_difference', left_tile_col, right_tile_col)


def rf_agg_local_max(tile_col):
    """Compute the cell-wise/local max operation between Tiles in a column."""
    return _apply_column_function('rf_agg_local_max', tile_col)


def rf_agg_local_min(tile_col):
    """Compute the cellwise/local min operation between Tiles in a column."""
    return _apply_column_function('rf_agg_local_min', tile_col)


def rf_agg_local_mean(tile_col):
    """Compute the cellwise/local mean operation between Tiles in a column."""
    return _apply_column_function('rf_agg_local_mean', tile_col)


def rf_agg_local_data_cells(tile_col):
    """Compute the cellwise/local count of non-NoData cells for all Tiles in a column."""
    return _apply_column_function('rf_agg_local_data_cells', tile_col)


def rf_agg_local_no_data_cells(tile_col):
    """Compute the cellwise/local count of NoData cells for all Tiles in a column."""
    return _apply_column_function('rf_agg_local_no_data_cells', tile_col)


def rf_agg_local_stats(tile_col):
    """Compute cell-local aggregate descriptive statistics for a column of Tiles."""
    return _apply_column_function('rf_agg_local_stats', tile_col)


def rf_mask(src_tile_col, mask_tile_col, inverse=False):
    """Where the rf_mask (second) tile contains NODATA, replace values in the source (first) tile with NODATA.
       If `inverse` is true, replaces values in the source tile with NODATA where the mask tile contains valid data.
    """
    if not inverse:
        return _apply_column_function('rf_mask', src_tile_col, mask_tile_col)
    else:
        rf_inverse_mask(src_tile_col, mask_tile_col)


def rf_inverse_mask(src_tile_col, mask_tile_col):
    """Where the rf_mask (second) tile DOES NOT contain NODATA, replace values in the source
       (first) tile with NODATA."""
    return _apply_column_function('rf_inverse_mask', src_tile_col, mask_tile_col)


def rf_mask_by_value(data_tile, mask_tile, mask_value, inverse=False):
    """Generate a tile with the values from the data tile, but where cells in the masking tile contain the masking
    value, replace the data value with NODATA. """
    if isinstance(mask_value, (int, float)):
        mask_value = lit(mask_value)
    jfcn = RFContext.active().lookup('rf_mask_by_value')

    return Column(jfcn(_to_java_column(data_tile), _to_java_column(mask_tile), _to_java_column(mask_value), inverse))


def rf_mask_by_values(data_tile, mask_tile, mask_values):
    """Generate a tile with the values from `data_tile`, but where cells in the `mask_tile` are in the `mask_values`
       list, replace the value with NODATA.
    """
    from pyspark.sql.functions import array as sql_array
    if isinstance(mask_values, list):
        mask_values = sql_array([lit(v) for v in mask_values])

    jfcn = RFContext.active().lookup('rf_mask_by_values')
    col_args = [_to_java_column(c) for c in [data_tile, mask_tile, mask_values]]
    return Column(jfcn(*col_args))


def rf_inverse_mask_by_value(data_tile, mask_tile, mask_value):
    """Generate a tile with the values from the data tile, but where cells in the masking tile do not contain the
    masking value, replace the data value with NODATA. """
    if isinstance(mask_value, (int, float)):
        mask_value = lit(mask_value)
    return _apply_column_function('rf_inverse_mask_by_value', data_tile, mask_tile, mask_value)


def rf_mask_by_bit(data_tile, mask_tile, bit_position, value_to_mask):
    """Applies a mask using bit values in the `mask_tile`. Working from the right, extract the bit at `bitPosition` from the `maskTile`. In all locations where these are equal to the `valueToMask`, the returned tile is set to NoData, else the original `dataTile` cell value."""
    if isinstance(bit_position, int):
        bit_position = lit(bit_position)
    if isinstance(value_to_mask, (int, float, bool)):
        value_to_mask = lit(bool(value_to_mask))
    return _apply_column_function('rf_mask_by_bit', data_tile, mask_tile, bit_position, value_to_mask)


def rf_mask_by_bits(data_tile, mask_tile, start_bit, num_bits, values_to_mask):
    """Applies a mask from blacklisted bit values in the `mask_tile`. Working from the right, the bits from `start_bit` to `start_bit + num_bits` are @ref:[extracted](reference.md#rf_local_extract_bits) from cell values of the `mask_tile`. In all locations where these are in the `mask_values`, the returned tile is set to NoData; otherwise the original `tile` cell value is returned."""
    if isinstance(start_bit, int):
        start_bit = lit(start_bit)
    if isinstance(num_bits, int):
        num_bits = lit(num_bits)
    if isinstance(values_to_mask, (tuple, list)):
        from pyspark.sql.functions import array
        values_to_mask = array([lit(v) for v in values_to_mask])

    return _apply_column_function('rf_mask_by_bits', data_tile, mask_tile, start_bit, num_bits, values_to_mask)


def rf_local_extract_bits(tile, start_bit, num_bits=1):
    """Extract value from specified bits of the cells' underlying binary data.
    * `startBit` is the first bit to consider, working from the right. It is zero indexed.
    * `numBits` is the number of bits to take moving further to the left. """
    if isinstance(start_bit, int):
        start_bit = lit(start_bit)
    if isinstance(num_bits, int):
        num_bits = lit(num_bits)
    return _apply_column_function('rf_local_extract_bits', tile, start_bit, num_bits)


def rf_local_less(left_tile_col, right_tile_col):
    """Cellwise less than comparison between two tiles"""
    return _apply_column_function('rf_local_less', left_tile_col, right_tile_col)


def rf_local_less_equal(left_tile_col, right_tile_col):
    """Cellwise less than or equal to comparison between two tiles"""
    return _apply_column_function('rf_local_less_equal', left_tile_col, right_tile_col)


def rf_local_greater(left_tile_col, right_tile_col):
    """Cellwise greater than comparison between two tiles"""
    return _apply_column_function('rf_local_greater', left_tile_col, right_tile_col)


def rf_local_greater_equal(left_tile_col, right_tile_col):
    """Cellwise greater than or equal to comparison between two tiles"""
    return _apply_column_function('rf_local_greater_equal', left_tile_col, right_tile_col)


def rf_local_equal(left_tile_col, right_tile_col):
    """Cellwise equality comparison between two tiles"""
    return _apply_column_function('rf_local_equal', left_tile_col, right_tile_col)


def rf_local_unequal(left_tile_col, right_tile_col):
    """Cellwise inequality comparison between two tiles"""
    return _apply_column_function('rf_local_unequal', left_tile_col, right_tile_col)


def rf_round(tile_col):
    """Round cell values to the nearest integer without changing the cell type"""
    return _apply_column_function('rf_round', tile_col)


def rf_abs(tile_col):
    """Compute the absolute value of each cell"""
    return _apply_column_function('rf_abs', tile_col)


def rf_log(tile_col):
    """Performs cell-wise natural logarithm"""
    return _apply_column_function('rf_log', tile_col)


def rf_log10(tile_col):
    """Performs cell-wise logartithm with base 10"""
    return _apply_column_function('rf_log10', tile_col)


def rf_log2(tile_col):
    """Performs cell-wise logartithm with base 2"""
    return _apply_column_function('rf_log2', tile_col)


def rf_log1p(tile_col):
    """Performs natural logarithm of cell values plus one"""
    return _apply_column_function('rf_log1p', tile_col)


def rf_exp(tile_col):
    """Performs cell-wise exponential"""
    return _apply_column_function('rf_exp', tile_col)


def rf_exp2(tile_col):
    """Compute 2 to the power of cell values"""
    return _apply_column_function('rf_exp2', tile_col)


def rf_exp10(tile_col):
    """Compute 10 to the power of cell values"""
    return _apply_column_function('rf_exp10', tile_col)


def rf_expm1(tile_col):
    """Performs cell-wise exponential, then subtract one"""
    return _apply_column_function('rf_expm1', tile_col)


def rf_identity(tile_col):
    """Pass tile through unchanged"""
    return _apply_column_function('rf_identity', tile_col)


def rf_resample(tile_col, scale_factor_col):
    """Resample tile to different size based on scalar factor or tile whose dimension to match
    Scalar less than one will downsample tile; greater than one will upsample. Uses nearest-neighbor."""
    return _apply_column_function('rf_resample', tile_col, scale_factor_col)


def rf_crs(tile_col):
    """Get the CRS of a RasterSource or ProjectedRasterTile"""
    return _apply_column_function('rf_crs', tile_col)


def rf_mk_crs(crs_text):
    """Resolve CRS from text identifier. Supported registries are EPSG, ESRI, WORLD, NAD83, & NAD27.
    An example of a valid CRS name is EPSG:3005."""
    return Column(_context_call('_make_crs_literal', crs_text))


def st_extent(geom_col):
    """Compute the extent/bbox of a Geometry (a tile with embedded extent and CRS)"""
    return _apply_column_function('st_extent', geom_col)


def rf_extent(proj_raster_col):
    """Get the extent of a RasterSource or ProjectedRasterTile (a tile with embedded extent and CRS)"""
    return _apply_column_function('rf_extent', proj_raster_col)


def rf_tile(proj_raster_col):
    """Extracts the Tile component of a ProjectedRasterTile (or Tile)."""
    return _apply_column_function('rf_tile', proj_raster_col)


def rf_proj_raster(tile, extent, crs):
    """
    Construct a `proj_raster` structure from individual CRS, Extent, and Tile columns
    """
    return _apply_column_function('rf_proj_raster', tile, extent, crs)

def st_geometry(geom_col):
    """Convert the given extent/bbox to a polygon"""
    return _apply_column_function('st_geometry', geom_col)


def rf_geometry(proj_raster_col):
    """Get the extent of a RasterSource or ProjectdRasterTile as a Geometry"""
    return _apply_column_function('rf_geometry', proj_raster_col)


def rf_xz2_index(geom_col, crs_col=None, index_resolution = 18):
    """Constructs a XZ2 index in WGS84 from either a Geometry, Extent, ProjectedRasterTile, or RasterSource and its CRS.
       For details: https://www.geomesa.org/documentation/user/datastores/index_overview.html """

    jfcn = RFContext.active().lookup('rf_xz2_index')

    if crs_col is not None:
        return Column(jfcn(_to_java_column(geom_col), _to_java_column(crs_col), index_resolution))
    else:
        return Column(jfcn(_to_java_column(geom_col), index_resolution))

def rf_z2_index(geom_col, crs_col=None, index_resolution = 18):
    """Constructs a Z2 index in WGS84 from either a Geometry, Extent, ProjectedRasterTile, or RasterSource and its CRS.
        First the native extent is extracted or computed, and then center is used as the indexing location.
        For details: https://www.geomesa.org/documentation/user/datastores/index_overview.html """

    jfcn = RFContext.active().lookup('rf_z2_index')

    if crs_col is not None:
        return Column(jfcn(_to_java_column(geom_col), _to_java_column(crs_col), index_resolution))
    else:
        return Column(jfcn(_to_java_column(geom_col), index_resolution))

# ------ GeoMesa Functions ------

def st_geomFromGeoHash(*args):
    """"""
    return _apply_column_function('st_geomFromGeoHash', *args)


def st_geomFromWKT(*args):
    """"""
    return _apply_column_function('st_geomFromWKT', *args)


def st_geomFromWKB(*args):
    """"""
    return _apply_column_function('st_geomFromWKB', *args)


def st_lineFromText(*args):
    """"""
    return _apply_column_function('st_lineFromText', *args)


def st_makeBox2D(*args):
    """"""
    return _apply_column_function('st_makeBox2D', *args)


def st_makeBBox(*args):
    """"""
    return _apply_column_function('st_makeBBox', *args)


def st_makePolygon(*args):
    """"""
    return _apply_column_function('st_makePolygon', *args)


def st_makePoint(*args):
    """"""
    return _apply_column_function('st_makePoint', *args)


def st_makeLine(*args):
    """"""
    return _apply_column_function('st_makeLine', *args)


def st_makePointM(*args):
    """"""
    return _apply_column_function('st_makePointM', *args)


def st_mLineFromText(*args):
    """"""
    return _apply_column_function('st_mLineFromText', *args)


def st_mPointFromText(*args):
    """"""
    return _apply_column_function('st_mPointFromText', *args)


def st_mPolyFromText(*args):
    """"""
    return _apply_column_function('st_mPolyFromText', *args)


def st_point(*args):
    """"""
    return _apply_column_function('st_point', *args)


def st_pointFromGeoHash(*args):
    """"""
    return _apply_column_function('st_pointFromGeoHash', *args)


def st_pointFromText(*args):
    """"""
    return _apply_column_function('st_pointFromText', *args)


def st_pointFromWKB(*args):
    """"""
    return _apply_column_function('st_pointFromWKB', *args)


def st_polygon(*args):
    """"""
    return _apply_column_function('st_polygon', *args)


def st_polygonFromText(*args):
    """"""
    return _apply_column_function('st_polygonFromText', *args)


def st_castToPoint(*args):
    """"""
    return _apply_column_function('st_castToPoint', *args)


def st_castToPolygon(*args):
    """"""
    return _apply_column_function('st_castToPolygon', *args)


def st_castToLineString(*args):
    """"""
    return _apply_column_function('st_castToLineString', *args)


def st_byteArray(*args):
    """"""
    return _apply_column_function('st_byteArray', *args)


def st_boundary(*args):
    """"""
    return _apply_column_function('st_boundary', *args)


def st_coordDim(*args):
    """"""
    return _apply_column_function('st_coordDim', *args)


def st_dimension(*args):
    """"""
    return _apply_column_function('st_dimension', *args)


def st_envelope(*args):
    """"""
    return _apply_column_function('st_envelope', *args)


def st_exteriorRing(*args):
    """"""
    return _apply_column_function('st_exteriorRing', *args)


def st_geometryN(*args):
    """"""
    return _apply_column_function('st_geometryN', *args)


def st_geometryType(*args):
    """"""
    return _apply_column_function('st_geometryType', *args)


def st_interiorRingN(*args):
    """"""
    return _apply_column_function('st_interiorRingN', *args)


def st_isClosed(*args):
    """"""
    return _apply_column_function('st_isClosed', *args)


def st_isCollection(*args):
    """"""
    return _apply_column_function('st_isCollection', *args)


def st_isEmpty(*args):
    """"""
    return _apply_column_function('st_isEmpty', *args)


def st_isRing(*args):
    """"""
    return _apply_column_function('st_isRing', *args)


def st_isSimple(*args):
    """"""
    return _apply_column_function('st_isSimple', *args)


def st_isValid(*args):
    """"""
    return _apply_column_function('st_isValid', *args)


def st_numGeometries(*args):
    """"""
    return _apply_column_function('st_numGeometries', *args)


def st_numPoints(*args):
    """"""
    return _apply_column_function('st_numPoints', *args)


def st_pointN(*args):
    """"""
    return _apply_column_function('st_pointN', *args)


def st_x(*args):
    """"""
    return _apply_column_function('st_x', *args)


def st_y(*args):
    """"""
    return _apply_column_function('st_y', *args)


def st_asBinary(*args):
    """"""
    return _apply_column_function('st_asBinary', *args)


def st_asGeoJSON(*args):
    """"""
    return _apply_column_function('st_asGeoJSON', *args)


def st_asLatLonText(*args):
    """"""
    return _apply_column_function('st_asLatLonText', *args)


def st_asText(*args):
    """"""
    return _apply_column_function('st_asText', *args)


def st_geoHash(*args):
    """"""
    return _apply_column_function('st_geoHash', *args)


def st_bufferPoint(*args):
    """"""
    return _apply_column_function('st_bufferPoint', *args)


def st_antimeridianSafeGeom(*args):
    """"""
    return _apply_column_function('st_antimeridianSafeGeom', *args)


def st_translate(*args):
    """"""
    return _apply_column_function('st_translate', *args)


def st_contains(*args):
    """"""
    return _apply_column_function('st_contains', *args)


def st_covers(*args):
    """"""
    return _apply_column_function('st_covers', *args)


def st_crosses(*args):
    """"""
    return _apply_column_function('st_crosses', *args)


def st_disjoint(*args):
    """"""
    return _apply_column_function('st_disjoint', *args)


def st_equals(*args):
    """"""
    return _apply_column_function('st_equals', *args)


def st_intersects(*args):
    """"""
    return _apply_column_function('st_intersects', *args)


def st_overlaps(*args):
    """"""
    return _apply_column_function('st_overlaps', *args)


def st_touches(*args):
    """"""
    return _apply_column_function('st_touches', *args)


def st_within(*args):
    """"""
    return _apply_column_function('st_within', *args)


def st_relate(*args):
    """"""
    return _apply_column_function('st_relate', *args)


def st_relateBool(*args):
    """"""
    return _apply_column_function('st_relateBool', *args)


def st_area(*args):
    """"""
    return _apply_column_function('st_area', *args)


def st_closestPoint(*args):
    """"""
    return _apply_column_function('st_closestPoint', *args)


def st_centroid(*args):
    """"""
    return _apply_column_function('st_centroid', *args)


def st_distance(*args):
    """"""
    return _apply_column_function('st_distance', *args)


def st_distanceSphere(*args):
    """"""
    return _apply_column_function('st_distanceSphere', *args)


def st_length(*args):
    """"""
    return _apply_column_function('st_length', *args)


def st_aggregateDistanceSphere(*args):
    """"""
    return _apply_column_function('st_aggregateDistanceSphere', *args)


def st_lengthSphere(*args):
    """"""
    return _apply_column_function('st_lengthSphere', *args)
