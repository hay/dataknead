class BaseLoader:
    def read(f):
        raise NotImplementedError("Reading is not implemented for this type")

    def write(f, data):
        raise NotImplementedError("Writing is not implemented for this type")