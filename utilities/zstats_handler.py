import subprocess
import arcpy
import os
import sys

def main_script(layer, raster):
    # add to this if i'm running average area of zstats
    final_aoi = layer.final_aoi

    start_id = 0

    end_id = int(arcpy.GetCount_management(final_aoi).getOutput(0))

    print("Number of features: {}".format(end_id))

    zstats_subprocess = os.path.join(layer.root_dir, "utilities", "zstats_subprocess.py")

    executable = sys.executable

    script_cmd = [executable, zstats_subprocess, raster.value,
                  raster.zone, layer.final_aoi, raster.cellsize, raster.analysis]

    expected_complete_total = len(list(range(start_id, end_id)))
    feature_status = {}

    while len(feature_status) < expected_complete_total:

        cmd = script_cmd + [str(start_id), str(end_id)]

        # this runs the analysis
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # for each line that comes back from the subprocess, if "succeeded" is in the line
        # increase counter by 1.
        # for line in iter(p.stdout.readline, b''):
        for line in iter(p.stdout.readline, b''):

            arcpy.AddMessage(line)

            # Each line that comes back from the subprocess represents 1 feature/ID
            # We need to keep track of this in case a feature fails so we can skip it

            if b'debug' in line:

                pass

            else:

                if b'process succeeded' in line:

                    feature_status[start_id] = True

                    start_id += 1

        p.wait()
        # Since no lines are returned from sub if it fails, add this: get the return code from the failure,
        # as long as it isn't 0, its a failure, and increment the counter by 1 so it starts on the next feautre

        if p.returncode != 0:
            print("failed")
            feature_status[start_id] = False
            start_id += 1
