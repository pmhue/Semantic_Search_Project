import pydantic


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="allow", from_attributes=True)

    # Override to resolve deprecated
    def json(self, *args, **kwargs):
        return self.model_dump_json(*args, **kwargs)

        # Allow set like dict, dict["key"] = value

    def __setitem__(self, key, value):
        setattr(self, key, value)

        # Allow get like dict, value = dict["key"]

    def __getitem__(self, key):
        return getattr(self, key)
