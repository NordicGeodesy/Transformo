"""
Transformo operator classes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Union

import transformo
from transformo._typing import CoordinateMatrix
from transformo.core import Operator
from transformo.datatypes import Parameter

# TODO: how to make the awk-script part of the installation?
# Not all users have transformo installed like this
AWK_SCRIPT = "C:/Transformo/test/data/gravsoft_data/gravsoft2xyz.awk"

FITGEOID1_OUTPUT_FILES = [
    "fitgeoid_dif.gri",
    "fitgeoid_dif.err",
    "fitgeoid_dif.dat",
    "fitgeoid_dif2.dat",
]


class GravsoftOperator(Operator):
    """
    This Operator is a wrapper for Gravsoft.

    It assumes that gdal_translate, as well as the Gravsoft program package, are
    installed and present in the PATH!
    """

    type: Literal["gravsoft_operator"] = "gravsoft_operator"

    # define settings for gravsofts "fitgeoid1" program
    gravimetric_geoid_file: Union[str, Path] = None
    gnsslevelling_file: Union[str, Path] = None
    transformed_geoid_file: Union[str, Path] = None
    x_half: float = None
    stddev_minimum: float = None
    grid_extent: str = None

    # or the user can just provide the raw input string
    fitgeoid_input_string: str = None

    # Directory to save all the various output files from gravsoft
    outdir: str = None

    def _parameter_list(self) -> list[Parameter]:
        return []

    def _proj_name(self) -> str:
        return "noop"

    def estimate(
        self,
        source_coordinates: CoordinateMatrix,
        target_coordinates: CoordinateMatrix,
        source_weights: CoordinateMatrix,
        target_weights: CoordinateMatrix,
    ) -> None:
        """
        Run Gravsoft's fitgeoid1 program and convert output files to more common formats
        """

        # if raw input string is given, we have to parse out the name of fitted geoid.
        # this should always be the third line
        if self.fitgeoid_input_string is not None:
            self.transformed_geoid_file = self.fitgeoid_input_string.split("\n")[2]
        else:
            # Construct input file and assume all necessary params are given
            self.fitgeoid_input_string = self.construct_input_file(
                self.gravimetric_geoid_file,
                self.gnsslevelling_file,
                self.transformed_geoid_file,
                self.x_half,
                self.stddev_minimum,
                self.grid_extent,
            )


        # show the input string passed to gravsoft in debug info
        transformo.logger.debug(f"\nPassing input string to fitgeoid1:")
        transformo.logger.debug(f"{self.fitgeoid_input_string}\n")

        # Call gravsoft's fitgeoid1.
        command = "fitgeoid1"
        transformo.run_command_with_input(command, input_text=self.fitgeoid_input_string)

        # fitgeoid1 produces a number of files in current dir, so we move the files to a designated out-dir
        self.outdir = "gravsoft_out" if self.outdir is None else self.outdir
        self.move_output_files(outdir=self.outdir)

        # Convert the somewhat esoteric file formats to more well-known formats
        # grid data: .gri -> .xyz (point data format) -> .tif (geotiff)
        grid_file = Path(self.outdir)/Path(self.transformed_geoid_file)
        self.gravsoft_gri_to_tif(grid_file)

        diff_file = Path(self.outdir)/Path("fitgeoid_dif.gri")
        self.gravsoft_gri_to_tif(diff_file)


    def construct_input_file(
        self,
        gravimetric_geoid_file: Union[str, Path],
        gnsslevelling_file: Union[str, Path],
        transformed_geoid_file: Union[str, Path],
        x_half: float,
        stddev_minimum: float,
        grid_extent: str
    ) -> str:
        """Constructs an input file to be used by "fitgeoid1"

        A sample file looks like this:

            gravgeoid2023.gri
            input_gnss_levelling_dataset.n
            output_fitted_geoid.gri
            25 1 1 t
            60 0.005
            53.5000 58.00 7.0000 17.000020  0.010 0.0166667

        See the Gravsoft manual for documentation of the format.
        """
        fitgeoid_input_string = "\n".join((
            f"{str(gravimetric_geoid_file)}",
            f"{str(gnsslevelling_file)}",
            f"{str(transformed_geoid_file)}",
            f"25 1 1 t",
            f"{str(x_half)} {str(stddev_minimum)}",
            f"{grid_extent}",
        ))

        return fitgeoid_input_string

    def move_output_files(self, outdir: str):
        """
        Move Gravsoft output files into ``outdir``
        """

        all_output_files = FITGEOID1_OUTPUT_FILES + [self.transformed_geoid_file]

        # does not raise error if outdir exists
        Path.mkdir(Path(outdir), parents=True, exist_ok=True)

        for f in all_output_files:
            Path.replace(f, Path(outdir)/Path(f).name)

    def gravsoft_gri_to_tif(self, grid_file: Path):
        """Convert a gravsoft .gri file to .tif"""
        xyz_file = self.grid2xyz(grid_file)
        self.xyz2tif(xyz_file)

        # remove the intermediate xyz-file
        xyz_file.unlink()


    def grid2xyz(self, grid_file: Path) -> Path:
        """
        Convert a gravsoft .gri file to .xyz

        Uses the GNU Awk (gawk) program. The parsing of the .gri
        file is defined in the input script "gravsoft2xyz.awk"
        """
        command = f"gawk -f {AWK_SCRIPT} {grid_file}"

        output_file=f"{grid_file.with_suffix('.xyz')}"

        transformo.run_command_with_output(command, output_file=output_file)

        return Path(output_file)

    def xyz2tif(self, xyz_file: Path):
        """
        Convert from the list-based xyz-format back to a gridded tif-file using gdal_translate
        """
        command = f"gdal_translate -of GTiff -a_srs EPSG:4326 {xyz_file} {xyz_file.with_suffix('.tif')}"

        transformo.run_command(command)

    def forward(self, coordinates: CoordinateMatrix) -> CoordinateMatrix:
        """
        Forward method of the Gravsoft wrapper.

        The current implementation does not use the source- nor target-coordinates for anything!
        """
        return coordinates
