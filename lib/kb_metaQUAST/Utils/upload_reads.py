from installed_clients.ReadsUtilsClient import ReadsUtils
from installed_clients.DataFileUtilClient import DataFileUtil

def upload_reads(callback_url, reads_file, ws_name, reads_obj_name, source_reads_upa, isInterleaved):
    """
    callback_url = as usual.
    reads_file = full path to the reads file to upload
    ws_name = the workspace to use for uploading the reads file
    reads_obj_name = the name of the new reads object to save as
    source_reads = if not None, the source UPA for the original reads file.
    """
    # unfortunately, the ReadsUtils only accepts uncompressed fq files- this should
    # be fixed on the KBase side
    dfu = DataFileUtil(callback_url)
    reads_unpacked = dfu.unpack_file({'file_path': reads_file})['file_path']

    ru = ReadsUtils(callback_url)
    new_reads_upa = ru.upload_reads({
        'fwd_file': reads_unpacked,
        'interleaved': isInterleaved,
        'wsname': ws_name,
        'name': reads_obj_name,
        'source_reads_ref': source_reads_upa
    })['obj_ref']
    print('saved ' + str(reads_unpacked) + ' to ' + str(new_reads_upa))
    return new_reads_upa