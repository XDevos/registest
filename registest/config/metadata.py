import os

from registest.utils.io_utils import load_json, save_json


class FileMetadata:
    def __init__(self, filepath: str, ref_path: str = ""):
        self.path = filepath
        self.reference_img: str = ref_path
        self.transformation = {"done": False, "xyz_values": None}
        self.registration = {"done": False, "method": None}
        self.shift = {"done": False, "xyz_values": None}
        self.similarity = {"SSIM": None, "NMSE": None}

    def get_metadata(self):
        return {
            "reference_img": self.reference_img,
            "transformation": self.transformation,
            "registration": self.registration,
            "shift": self.shift,
            "similarity": self.similarity,
        }


class MetadataManager:
    """Manage a metadata.json file."""

    def __init__(self, folder):
        self.folder = folder
        self.filepath = os.path.join(self.folder, "metadata.json")
        self.data = self._load_metadata()

    def _load_metadata(self):
        """Load JSON file if exist, or return an empty dict."""
        if os.path.exists(self.filepath):
            return load_json(self.filepath)
        return {}

    def save_metadata(self):
        """Save current metadata"""
        save_json(self.data, self.filepath)

    def add_file_metadata(self, file_metadata: FileMetadata):
        """Add metadata for a new file"""
        if file_metadata.path in self.data:
            raise ValueError(
                f"This key: '{file_metadata.path}' already exist inside '{self.filepath}'."
            )
        self.data[file_metadata.path] = file_metadata.get_metadata()
        self.save_metadata()
