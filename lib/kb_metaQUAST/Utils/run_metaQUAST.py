import subprocess
import os
# from installed_clients.readsutilsClient import ReadsUtils
# from installed_clients.DataFileUtilClient import DataFileUtil

def run_metaQUAST(result_dir, report_file):
    try:
        command = [
            'python3', '/usr/local/bin/quast-5.3.0/quast.py',
            '/usr/local/bin/quast-5.3.0/test_data/contigs_1.fasta',
               '/usr/local/bin/quast-5.3.0/test_data/contigs_2.fasta',
               '-r', '/usr/local/bin/quast-5.3.0/test_data/reference.fasta.gz',
               '-g', '/usr/local/bin/quast-5.3.0/test_data/genes.gff',
               '--no-plots', '--no-krona', '--no-icarus', '--no-snps', '--no-sv', '--no-read-stats',
               '-o', result_dir
        ]
        # command = [
        #     'ls', '/usr/local/bin'
        # ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # print(result)

        # Create a directory for report_file if it doesn't exist
        if not os.path.exists(os.path.dirname(report_file)):
            os.makedirs(os.path.dirname(report_file))

        # Create a directory for result_dir if it doesn't exist
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        # Write the output to the specified HTML-formatted file
        with open(report_file, 'w') as f:
            f.write("<html><body><pre>")
            f.write(result.stderr)
            f.write("</pre></body></html>")
            
        print(f"metaQUAST command executed successfully. Report output saved to {report_file}\n")

        # Get the file name's prefix to the left of the . from input_file. Ignore the path.
        # prefix = input_file.split('/')[-1].split('.')[0]

        # Return in a dictionary the file names found in the result_dir folder
        return {
            # 'console_report_file': report_file, # No need to return - input parameter is not altered.
            # 'results_file_path': result_dir  + '/' + [f for f in os.listdir(result_dir) if prefix in f][0]
            'results_file_path': result_dir  + '/report.html'
        }

        # return { 'results_file_path': 'chikin' }
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running metaQUAST: {e}")