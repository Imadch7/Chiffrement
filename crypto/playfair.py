def _build_diagram(self, key):
    if not key:
        return None
    
    
def process_text(self, input_text, key):
    if not input_text:
        raise ValueError(f"A proper input must be passed")
    
    idx = 1
    diagram = self._build_diagram(key)

    if not diagram:
        raise ValueError(f"A key must be provided")