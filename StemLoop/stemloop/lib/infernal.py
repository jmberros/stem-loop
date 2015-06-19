import subprocess
import os
import sys
import re
from glob import glob


class Infernal:
    @staticmethod
    def pretty_filename_for_search(cm_database, target_fasta):
        return "{}__in__{}".format(
            re.sub("(\.cm|\.c\.cm)", "", cm_database),
            re.sub("\.(fasta|fa|fna)", "", target_fasta)
        )

    def __init__(self):
        self.default_db_name = "minifam.c.cm"

    def cmpress(self, cmodel_list, output_filename=None):
        """Build a CM database with the CM files in the current dir"""

        output_filename = output_filename or self.default_db_name

        with open(output_filename, "w") as f:
            subprocess.Popen(["cat"] + cmodel_list, stdout=f)

        subprocess.call(["cmpress", "-F", output_filename])

        return output_filename

    def cmscan(self, cm_database=None, target_fasta=None, cpu=1):
        """Search all fastas in the current dir with the given cm database"""

        cm_database = cm_database or self.default_db_name
        fastas = glob("*.fa") + glob("*.fna") + glob("*.fasta")
        if target_fasta:
            fastas = [target_fasta]

        for fasta in fastas:
            out_filename = self.pretty_filename_for_search(cm_database, fasta)
            count_fastas_cmd = "grep '>' {} | wc -l".format(fasta)
            query_count = int(os.popen(count_fastas_cmd).read().strip())

            if os.path.isfile(cm_database):
                count_cm_command = "grep 'ACC' {} | awk '{{ print $2 }}' | "\
                                   "sort | uniq | wc -l".format(cm_database)
                db_size = int(os.popen(count_cm_command).read().strip())
                command_args = {
                    'cm_database': cm_database,
                    'query': fasta,
                    'cpu': cpu,
                    'tbl_file': out_filename + ".cmscan-tbl",
                    'out_file': out_filename + ".cmscan-output",
                    'cm_db_size': db_size,  # doesn't belong
                    'query_count': query_count  # doesn't belong
                }
                command = \
                    "cmscan --tblout {tbl_file} -o {out_file} --cpu {cpu} "\
                    "{cm_database} {query}".format(**command_args)
 
                print(command)
                print("\n [database]  {cm_database} ({cm_db_size} models)"
                      "\n [query]     {query} ({query_count} sequences)".format(**command_args))
                print("\n... please wait ...\n")
                subprocess.check_output(command.split())
                print("Result:\n * {tbl_file}\n * {out_file}".format(**command_args))

            else:
                error_msg = "[ERROR] No file named \"{}\". "\
                            "Aborting.".format(cm_database)
                sys.exit(error_msg)
