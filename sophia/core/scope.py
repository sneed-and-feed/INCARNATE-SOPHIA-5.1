class FrequencyTuner:
    """
    Compiles the 'Scope String'. Ensures we know WHERE we are.
    """
    @staticmethod
    def tune(realm="cabin", layer="surface", topic="general"):
        # Returns a rigid, searchable path
        # Example: "realm:cabin/layer:deep_bog/topic:market_crash"
        return f"realm:{realm}/layer:{layer}/topic:{topic}"
