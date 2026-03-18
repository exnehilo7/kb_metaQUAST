# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import shutil

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.ReadsUtilsClient import ReadsUtils
from .Utils.run_metaQUAST import run_metaQUAST
from .Utils.createHtmlReport import HTMLReportCreator
from .Utils.upload_reads import upload_reads
#END_HEADER


class kb_metaQUAST:
    '''
    Module Name:
    kb_metaQUAST

    Module Description:
    A KBase module: kb_metaQUAST
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_kb_metaQUAST(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kb_metaQUAST
        logging.info('Running run_kb_metaQUAST with params=' + str(params))
        logging.info('Downloading reads from ' + params['input_reads_ref'])

        ru = ReadsUtils(self.callback_url)
        input_file_info = ru.download_reads({'read_libraries': [params['input_reads_ref']],
                                             'interleaved': 'true'})['files'][params['input_reads_ref']]
        logging.info('Downloaded reads from ' + str(input_file_info))

        output_reads_name = params['output_reads_name']
        output_reads_file = output_reads_name + ".fq"
        logging.info('Output reads name: ' + output_reads_file)

        #metaQUAST
        logging.info('Running metaQUAST')
        reportDirectory = os.path.join(self.shared_folder, 'Reports')
        reportFile = os.path.join(self.shared_folder, reportDirectory, 'index.html')
        resultsDirectory = os.path.join(self.shared_folder, 'Results')

        returned_dict = run_metaQUAST(resultsDirectory, reportFile)
        logging.info('Returned dictionary: ' + str(returned_dict))

        results_file_path = returned_dict['results_file_path']
        logging.info('Results file path: ' + results_file_path)

        # Rename output file via a copy
        output_reads_filepath = os.path.join(resultsDirectory, output_reads_file)
        shutil.copy(results_file_path, output_reads_filepath)

        mq_results = upload_reads(self.callback_url, output_reads_filepath, params['workspace_name'], output_reads_name, params['input_reads_ref'], isInterleaved)

        if os.path.exists(resultsDirectory):
            shutil.rmtree(resultsDirectory)

        objects_created = [{
                'ref': mq_results,
                'description': 'metaQuast results?'
            }]

        # Create a report
        report_creator = HTMLReportCreator(self.callback_url)
        output = report_creator.create_html_report(reportDirectory, params['workspace_name'], objects_created)
        logging.info ('HTML output report: ' + str(output))


        # OG code:
        # report = KBaseReport(self.callback_url)
        # report_info = report.create({'report': {'objects_created':[],
        #                                         'text_message': params['parameter_1']},
        #                                         'workspace_name': params['workspace_name']})
        # output = {
        #     'report_name': report_info['name'],
        #     'report_ref': report_info['ref'],
        # }
        #END run_kb_metaQUAST

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_kb_metaQUAST return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
