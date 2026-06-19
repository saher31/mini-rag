from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATED_SUCCESSFULLY = "file_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOADED_SUCCESSFULLY = "file_uploaded_successfully"
    FILE_UPLOADED_FAILED = "file_uploaded_failed"
    PROCESSING_FAILED = "processing_failed"
    PROCESSING_SUCCESSFULLY = "processing_successfully"
    NO_FILES_ERROR = "no_found_files"
    FILE_ID_ERROR = "no_file_found_with_this_id"
    