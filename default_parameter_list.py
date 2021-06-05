# default parameter list is working unexpectedly !!!!
class AnalyzeResult:
    # !!! don't do that, don't set default parameter list  !!!!
    def __init__(self, delete: bool, product_type: str = "variant", product_id: int = 0, variant_ids: List = list()):
        self._delete = delete
        self._product_type = product_type
        self._product_id = product_id
        self._variant_ids = variant_ids


class AnalyzeResult:
    def __init__(self, delete: bool, product_type: str = "variant", product_id: int = 0, variant_ids: List = None):
        self._delete = delete
        self._product_type = product_type
        self._product_id = product_id
        self._variant_ids = variant_ids if variant_ids is not None else list()

